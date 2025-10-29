"""
모듈: services/fall_runtime.py
역할:
  - 실시간 낙상 판별을 위한 **온라인 추론 러너**.
  - 디바이스별로 최근 관측값 시퀀스를 유지하고, 전처리(파생 피처 + 스케일링) 후
    LSTM(또는 TFLite) 모델로 확률을 추정하며, 최근 k개 확률의 평균으로 스무딩하여 최종 판정을 돕는다.

핵심 특징:
  • 디바이스별 고정 길이 버퍼(최근 seq_len 단계)를 유지
  • 파생 피처 생성: movement_diff, range_diff (1차 차분)
  • 표준화/정규화를 위해 사전 학습된 scaler(pickle)를 적용
  • 케라스 또는 TFLite 백엔드 선택 가능(배포 환경 유연성)
  • 최근 k개 확률을 평균하여 노이즈 완화(smooth_k)
  • asyncio.Lock를 사용해 동시 업데이트 안전성 확보

주의사항:
  - 멀티 프로세스(예: gunicorn 워커 여러 개)에서는 내부 버퍼(_buffers/_prob_hist)가 워커 간 **공유되지 않음**.
  - 모델/스케일러/메타 파일 경로 및 임계값(threshold)은 settings에서 주입.
"""

from collections import defaultdict, deque
import json, asyncio
import numpy as np
import joblib
import tensorflow as tf
from tensorflow.keras.models import load_model


class FallRuntime:
    """
    실시간 낙상 추론 런타임

    입력 스트림(feature):
      - presence, movement, moving_range, dwell_state (각 타임스텝별 정수/실수)

    파생 피처:
      - movement_diff = movement의 1차 차분
      - range_diff    = moving_range의 1차 차분

    파이프라인:
      1) 디바이스별 버퍼에 최신 관측값을 push (최대 seq_len 유지)
      2) 버퍼 길이가 seq_len에 도달하면 시퀀스 구성 및 scaler.transform 적용
      3) 모델로 확률 추정(prob)
      4) 최근 k개(prob_hist)의 평균을 smoothed 확률로 사용
      5) smoothed > threshold → pred=1(낙상 의심), else pred=0
    """

    def __init__(self, model_path: str, scaler_path: str, meta_path: str | None = None,
                 threshold: float | None = None, smooth_k: int = 3, backend: str = "keras"):
        # 백엔드 종류(keras/tflite)
        self.backend = backend.lower()

        # --- 모델 로드 ---
        #  - 케라스: load_model(compile=False)로 추론만 수행
        #  - TFLite : Interpreter 초기화 후 텐서 인덱스 캐시
        if self.backend == "keras":
            self.model = load_model(model_path, compile=False)
        elif self.backend == "tflite":
            self.interpreter = tf.lite.Interpreter(model_path=model_path)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
        else:
            raise ValueError(f"Unsupported backend: {backend}")

        # --- 스케일러 로드 ---
        #  - 학습 시 저장된 전처리기(예: StandardScaler/MinMaxScaler)를 joblib로 로드
        self.scaler = joblib.load(scaler_path)

        # --- 메타정보 로드 ---
        #  - 기본값(dict) 위에 meta_path가 제공되면 파일의 내용을 merge(update)
        #  - features 순서, seq_len, threshold 등을 외부 설정으로 덮어쓸 수 있음
        self.meta = {
            "features": [
                "presence", "movement", "moving_range", "dwell_state",
                "movement_diff", "range_diff"
            ],
            "seq_len": 20,
            "threshold": 0.5,
        }
        if meta_path:
            with open(meta_path, "r", encoding="utf-8") as f:
                self.meta.update(json.load(f))

        # --- 운영 파라미터 확정 ---
        self.seq_len   = int(self.meta.get("seq_len", 20))                   # 입력 시퀀스 길이
        self.features  = list(self.meta.get("features"))                      # 피처 목록(순서 중요)
        self.threshold = float(threshold if threshold is not None else self.meta.get("threshold", 0.5))
        self.smooth_k  = int(smooth_k)                                         # 확률 스무딩 윈도 크기

        # 디바이스별 시퀀스 버퍼 & 확률 히스토리 (최대길이: seq_len / smooth_k)
        self._buffers   = defaultdict(lambda: deque(maxlen=self.seq_len))
        self._prob_hist = defaultdict(lambda: deque(maxlen=self.smooth_k))

        # 동시 접근 제어: 다중 코루틴에서 같은 디바이스 버퍼를 안전하게 업데이트
        self._lock = asyncio.Lock()

    # --- 시퀀스 구성 ---
    def _build_sequence(self, buf: list[dict]) -> np.ndarray:
        """
        버퍼(list[dict]) → (seq_len, n_features) 배열 구성 및 스케일링.

        1) 원시 피처 행렬 구성: [presence, movement, moving_range, dwell_state]
        2) 1차 차분 파생 피처 추가: movement_diff, range_diff
           - np.diff(..., prepend=첫값) 으로 길이 보존
        3) 학습 시점과 동일 스케일로 정규화: scaler.transform
        """
        # (seq_len, 4) 원시 피처 배열
        arr = np.array([
            [b["presence"], b["movement"], b["moving_range"], b["dwell_state"]]
            for b in buf
        ], dtype=np.float32)

        # 길이 보존 차분: 첫 원소와 동일 값을 prepend하여 diff 길이를 seq_len으로 유지
        movement_diff = np.diff(arr[:, 1], prepend=arr[0, 1])
        range_diff    = np.diff(arr[:, 2], prepend=arr[0, 2])

        # 피처 결합 후 스케일링 적용
        feats = np.column_stack([arr, movement_diff, range_diff])
        feats = self.scaler.transform(feats)
        return feats

    # --- 백엔드별 추론 ---
    def _predict_prob(self, x_seq: np.ndarray) -> float:
        """
        모델 입력: (seq_len, n_features)
        모델 출력: 확률(float)

        케라스: model.predict(batch=1) → (1, 1) 또는 (1,) → float
        TFLite : set_tensor + invoke + get_tensor → float
        """
        if self.backend == "keras":
            # 배치 차원을 추가하여 (1, seq_len, n_features) 형태로 예측
            return float(self.model.predict(x_seq[np.newaxis, ...], verbose=0).ravel()[0])
        elif self.backend == "tflite":
            input_data = np.expand_dims(x_seq.astype(np.float32), axis=0)
            self.interpreter.set_tensor(self.input_details[0]["index"], input_data)
            self.interpreter.invoke()
            output_data = self.interpreter.get_tensor(self.output_details[0]["index"])
            return float(output_data.ravel()[0])

    # --- 메인 업데이트 & 추론 ---
    async def update_and_predict(self, device_id: str, presence: int, movement: int,
                                 moving_range: int, dwell_state: int) -> tuple[float | None, int | None]:
        """
        최신 관측치를 버퍼에 추가하고, 충분한 길이에 도달하면 추론을 수행한다.

        반환:
          - (smoothed_prob, pred)
            • smoothed_prob: 최근 smooth_k개 확률의 평균(없으면 None)
            • pred: 임계값 초과(1) / 이하(0), 충분한 길이 미만이면 None
        """
        # 동일 객체에 대한 경쟁 상태를 피하기 위해 락으로 보호
        async with self._lock:
            # 디바이스별 버퍼에 관측값 추가 (deque: 최대 길이 seq_len 유지)
            self._buffers[device_id].append({
                "presence": presence,
                "movement": movement,
                "moving_range": moving_range,
                "dwell_state": dwell_state,
            })
            buf = list(self._buffers[device_id])

            # 시퀀스 길이가 아직 부족하면 추론하지 않고 종료
            if len(buf) < self.seq_len:
                return None, None

            # 모델 입력 시퀀스 구성(스케일링 포함)
            x_seq = self._build_sequence(buf)

        # CPU 바운드(모델 추론)를 이벤트 루프 밖에서 실행 → 메인 루프 블로킹 방지
        loop = asyncio.get_running_loop()
        prob = await loop.run_in_executor(None, lambda: self._predict_prob(x_seq))

        # 확률 히스토리에 추가 후 스무딩 확률 계산
        async with self._lock:
            self._prob_hist[device_id].append(prob)
            smoothed = float(np.mean(self._prob_hist[device_id]))

        # 스무딩 확률로 최종 판정(임계값 초과 시 1, 아니면 0)
        pred = 1 if smoothed > self.threshold else 0
        return smoothed, pred
