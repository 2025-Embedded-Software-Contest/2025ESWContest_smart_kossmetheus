# CareDian-backend

CareDian-backend는 Home Assistant 기반 스마트홈 백엔드 설정 및 커스텀 컴포넌트 구성을 포함한 프로젝트입니다. 이 저장소에는 자동화(automations), 템플릿(templates), 커스텀 컴포넌트(custom_components), PyScript 스크립트(pyscript) 등이 포함되어 있습니다.

## How to Run

이 프로젝트는 Home Assistant 설정 리포지토리로, 일반적인 의미의 `main.py` 실행 스크립트는 포함되어 있지 않습니다. 사용자가 별도의 `main.py`를 추가해 실행하려는 경우 다음과 같이 실행할 수 있습니다:

```bash
python main.py
```

Home Assistant 환경을 실행/적용하려면 다음을 참고하세요:
- Supervisor 또는 Docker에서 Home Assistant 컨테이너를 실행/재시작합니다
- 설정 변경 후 Home Assistant UI에서 Server Controls > Check configuration, Reload YAML을 수행합니다

## How to Test

`pytest` 기반의 단위 테스트를 사용하는 경우(예: `test_main.py`가 존재하는 경우) 다음과 같이 실행할 수 있습니다:

```bash
pytest test_main.py
```

현재 리포지토리에는 `test_main.py`가 존재하지 않을 수 있습니다. PyScript 또는 커스텀 컴포넌트 단위 테스트를 추가하려면 다음을 참고하세요:
- Python 가상환경 생성 후 개발 의존성 설치
- 테스트 파일(`tests/` 디렉터리 또는 `test_*.py`) 작성
- `pytest -q`로 실행
