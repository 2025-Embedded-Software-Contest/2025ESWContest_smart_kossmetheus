from collections import defaultdict, deque
import json, asyncio
import numpy as np
import joblib
import tensorflow as tf
from tensorflow.keras.models import load_model

class FallRuntime:
    """
    - 디바이스별로 최근 seq_len 스텝 버퍼를 유지
    - presence, movement, moving_range, dwell_state 를 받아
      movement_diff, range_diff 를 실시간으로 생성
    - scaler로 스케일 후 LSTM 예측 확률 반환
    - 최근 k개 확률 스무딩 후 threshold로 최종 판정
    """

    def __init__(self, model_path:str, scaler_path:str, meta_path:str|None=None,
                 threshold:float|None=None, smooth_k:int=3, backend:str="keras"):
        self.backend = backend.lower()

        # --- 모델 로드 ---
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
        self.scaler = joblib.load(scaler_path)

        # --- 메타정보 로드 ---
        self.meta = {
            "features": ["presence","movement","moving_range","dwell_state","movement_diff","range_diff"],
            "seq_len": 20,
            "threshold": 0.5,
        }
        if meta_path:
            with open(meta_path, "r", encoding="utf-8") as f:
                self.meta.update(json.load(f))

        self.seq_len   = int(self.meta.get("seq_len", 20))
        self.features  = list(self.meta.get("features"))
        self.threshold = float(threshold if threshold is not None else self.meta.get("threshold", 0.5))
        self.smooth_k  = int(smooth_k)

        self._buffers   = defaultdict(lambda: deque(maxlen=self.seq_len))
        self._prob_hist = defaultdict(lambda: deque(maxlen=self.smooth_k))
        self._lock = asyncio.Lock()

    # --- 시퀀스 구성 ---
    def _build_sequence(self, buf:list[dict]) -> np.ndarray:
        arr = np.array([[b["presence"], b["movement"], b["moving_range"], b["dwell_state"]] for b in buf],
                       dtype=np.float32)
        movement_diff = np.diff(arr[:,1], prepend=arr[0,1])
        range_diff    = np.diff(arr[:,2], prepend=arr[0,2])
        feats = np.column_stack([arr, movement_diff, range_diff])
        feats = self.scaler.transform(feats)
        return feats

    # --- 추론 (백엔드별 분기) ---
    def _predict_prob(self, x_seq: np.ndarray) -> float:
        if self.backend == "keras":
            return float(self.model.predict(x_seq[np.newaxis, ...], verbose=0).ravel()[0])
        elif self.backend == "tflite":
            input_data = np.expand_dims(x_seq.astype(np.float32), axis=0)
            self.interpreter.set_tensor(self.input_details[0]["index"], input_data)
            self.interpreter.invoke()
            output_data = self.interpreter.get_tensor(self.output_details[0]["index"])
            return float(output_data.ravel()[0])

    # --- 메인 업데이트 & 추론 ---
    async def update_and_predict(self, device_id:str, presence:int, movement:int,
                                 moving_range:int, dwell_state:int) -> tuple[float|None, int|None]:
        async with self._lock:
            self._buffers[device_id].append({
                "presence": presence,
                "movement": movement,
                "moving_range": moving_range,
                "dwell_state": dwell_state,
            })
            buf = list(self._buffers[device_id])
            if len(buf) < self.seq_len:
                return None, None
            x_seq = self._build_sequence(buf)

        loop = asyncio.get_running_loop()
        prob = await loop.run_in_executor(None, lambda: self._predict_prob(x_seq))

        async with self._lock:
            self._prob_hist[device_id].append(prob)
            smoothed = float(np.mean(self._prob_hist[device_id]))

        pred = 1 if smoothed > self.threshold else 0
        return smoothed, pred
