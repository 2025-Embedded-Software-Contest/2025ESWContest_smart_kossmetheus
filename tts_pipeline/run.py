# 실행: python -m tts_pipeline.run  (프로젝트 루트에서)
from pathlib import Path
from . import config as C
from .text_frontend import ko_text_frontend
from .synth_voxcpm import synth

def main():
    if not C.REF_AUDIO.exists():
        raise FileNotFoundError(f"참조 음성 없음: {C.REF_AUDIO}")

    # 1) 전처리 (config 옵션 적용)
    text_for_tts = ko_text_frontend(
        C.TTS_TEXT,
        use_g2pk=C.USE_G2PK,
        use_sentence_split=C.USE_SENTENCE_SPLIT,
    )

    # 2) 합성 → 최종(후보정 없음, 단일 산출물)
    out_path = C.FINAL_OUT
    synth(
        text_for_tts,
        C.PROMPT_TEXT,
        C.REF_AUDIO,
        out_path,
        C.CFG_VALUE,
        C.STEPS,
        C.USE_DENOISE,
        C.USE_NORMALIZE,
    )

    print(f"✅ 완료: {out_path}")

if __name__ == "__main__":
    main()
