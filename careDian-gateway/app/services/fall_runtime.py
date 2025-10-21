# app/services/fall_runtime.py
from collections import defaultdict, deque
import json, asyncio
import numpy as np
import joblib
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
                 threshold:float|None=None, smooth_k:int=3):
        # 학습 시 custom loss로 저장했더라도 inference만이면 compile=False 로 OK
        self.model = load_model(model_path, compile=False)
        self.scaler = joblib.load(scaler_path)

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

        self._buffers   = defaultdict(lambda: deque(maxlen=self.seq_len))  # per device samples
        self._prob_hist = defaultdict(lambda: deque(maxlen=self.smooth_k)) # per device probs
        self._lock = asyncio.Lock()

    def _build_sequence(self, buf:list[dict]) -> np.ndarray:
        # buf -> (T, 4) raw
        arr = np.array([[b["presence"], b["movement"], b["moving_range"], b["dwell_state"]] for b in buf],
                       dtype=np.float32)  # shape (T,4)
        # diffs
        movement_diff = np.diff(arr[:,1], prepend=arr[0,1])
        range_diff    = np.diff(arr[:,2], prepend=arr[0,2])
        feats = np.column_stack([arr, movement_diff, range_diff])  # (T,6) in feature order
        # scale
        feats = self.scaler.transform(feats)
        return feats

    async def update_and_predict(self, device_id:str, presence:int, movement:int,
                                 moving_range:int, dwell_state:int) -> tuple[float|None, int|None]:
        """
        버퍼 업데이트 후 확률/라벨 반환.
        버퍼가 아직 seq_len 미만이면 (None, None) 반환.
        """
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

        # 예측은 이벤트 루프 블로킹 피하려고 스레드풀로
        loop = asyncio.get_running_loop()
        prob = await loop.run_in_executor(
            None,
            lambda: float(self.model.predict(x_seq[np.newaxis, ...], verbose=0).ravel()[0])
        )

        async with self._lock:
            self._prob_hist[device_id].append(prob)
            smoothed = float(np.mean(self._prob_hist[device_id]))

        pred = 1 if smoothed > self.threshold else 0
        return smoothed, pred
