from pathlib import Path

# 파일/경로
REF_AUDIO = Path("voxcpm_voice.wav")       # 참조 음성 (프로젝트 루트 기준)
FINAL_OUT = Path("out_final.wav")

# VoxCPM 추론 파라미터
CFG_VALUE = 1.75
STEPS     = 14
USE_DENOISE   = False      # 필요시 False
USE_NORMALIZE = False      # VoxCPM CLI의 --normalize

# 텍스트 전처리 옵션
USE_G2PK = False            # 한국어 발음 규칙 적용 (실험적)
USE_SENTENCE_SPLIT = True   # 문장 분할 활성화 (품질 향상!) ⭐

# 텍스트들 - 종합 테스트 (영어+숫자 혼합)
TTS_TEXT = """거실 조명 1번이 켜졌습니다.
거실에서 낙상감지가 감지되었습니다.
현재 시각은 오후 5시 34분입니다.
약을 복용할 시간입니다.
임베디드소프트웨어 경진대회 참가 중입니다.
이일환, 김성혁, 전예찬, 김우현, 김예지 이렇게 5명이서 참가하고 있습니다!
열심히 하고 있네요~
"""
PROMPT_TEXT = (
    """현관문을 열고 오늘도 집 밖으로 나가 아무 일 없듯이 
아니 어제와 같이 별다른 감흥도 없이 하루를 시작하고, 
또 하루는 그렇게 어느 때와 같이 평범하게 산다. 
그리고 집에 돌아오면 길었고 지루했던 하루에 치여 
오늘도 살아냈다고 생각하며 잠자리에 든다.
내일도 또 그럴 것이고 모레도 그럴 것이다.
지금 시간은 오후 9시 45분입니다."""
)
 


