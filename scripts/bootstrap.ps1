# scripts/bootstrap.ps1
param(
  [switch]$Run = $true,          # 기본 파이프라인 실행 (tts_pipeline.run)
  [switch]$Stay = $true,         # 실행 후 venv 열린 PowerShell 창 유지
  [switch]$StartServices = $false, # Wyoming 서버 + pull_saver + ngrok 동시 실행
  [int]$TtsPort = 20000,         # Wyoming TTS 서버 포트 (기본 20000)
  [int]$PullPort = 20001         # pull_saver Flask 포트 (기본 20001)
)

$ErrorActionPreference = "Stop"

# 0) 프로젝트 루트로 이동
Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path) | Out-Null
Set-Location ..  # scripts 상위(프로젝트 루트)

# 1) Python 3.11 확인/설치
$pyOk = $false
try { $v = & py -3.11 -V 2>$null; if ($LASTEXITCODE -eq 0) { $pyOk = $true } } catch {}
if (-not $pyOk) {
  Write-Host "Python 3.11 미발견 → winget으로 설치 시도..." -ForegroundColor Yellow
  winget install -e --id Python.Python.3.11 --source winget
}

# 2) venv 생성
if (-not (Test-Path ".\.venv")) {
  & py -3.11 -m venv .venv
}

# 3) venv 활성화(현재 세션)
# 주: 스크립트에서 실행해도 이 PS 세션의 환경 변수는 유지됩니다.
& .\.venv\Scripts\Activate.ps1

# 4) pip/wheel/setuptools 업그레이드
python -m pip install --upgrade pip setuptools wheel

# 5) 패키지 설치
if (Test-Path ".\requirements.lock.txt") {
  pip install -r .\requirements.lock.txt
} else {
  pip install -r .\requirements.txt
}

# 6) FFmpeg 확인/설치(+세션 PATH 반영)
function Ensure-FFmpeg {
  $ff = (Get-Command ffmpeg -ErrorAction SilentlyContinue)
  if ($ff) { return }
  Write-Host "FFmpeg 미발견 → winget으로 설치 시도..." -ForegroundColor Yellow
  winget install -e --id Gyan.FFmpeg --scope user
  $ffBin = Join-Path $env:LOCALAPPDATA "Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-full_build\bin"
  if (Test-Path $ffBin) {
    $env:Path = "$ffBin;$env:Path"
  }
}
Ensure-FFmpeg
ffmpeg -version | Out-Host

# 7) HuggingFace symlink 권한 이슈 회피(Windows)
$env:HF_HUB_DISABLE_SYMLINKS = "1"

# 8) 실행(선택)
if ($Run -and -not $StartServices) {
  python -m tts_pipeline.run
}

# 8-1) 서비스 일괄 실행(선택): Wyoming 서버 + pull_saver + ngrok
if ($StartServices) {
  Write-Host "Wyoming 서버/풀세이버/ngrok 일괄 실행을 시작합니다…" -ForegroundColor Cyan

  # venv 내 python 지정 (백그라운드 프로세스에도 확실히 적용)
  $pyExe = Join-Path $PWD ".\.venv\Scripts\python.exe"
  if (-not (Test-Path $pyExe)) { $pyExe = "python" }

  # 1) Wyoming TTS 서버 (tcp://0.0.0.0:$TtsPort)
  $serverArgs = @(
    "-m","tts_pipeline.server",
    "--uri","tcp://0.0.0.0:$TtsPort",
    "--voices-dir","./voices",
    "--default-speaker-name","korean_male",
    "--default-prompt-audio","./voices/korean_male/ref039.wav",
    "--default-prompt-text-file","./voices/korean_male/ref039.txt",
    "--frontend","ko"
  )
  $serverProc = Start-Process -FilePath $pyExe -ArgumentList $serverArgs -PassThru
  Write-Host ("[Wyoming] PID={0} URI=tcp://0.0.0.0:{1}" -f $serverProc.Id, $TtsPort) -ForegroundColor Green

  # 2) pull_saver (Flask) — 포트는 20001 (기본)로 고정 실행
  #    pull_saver.py는 하드코딩 포트(5055)이므로 flask CLI로 포트를 지정해 실행
  $pullArgs = @(
    "-m","flask","--app","tts_pipeline.pull_saver",
    "run","--host","0.0.0.0","--port",$PullPort
  )
  $pullProc = Start-Process -FilePath $pyExe -ArgumentList $pullArgs -PassThru
  Write-Host ("[pull_saver] PID={0} http://0.0.0.0:{1}/pull" -f $pullProc.Id, $PullPort) -ForegroundColor Green

  # 3) ngrok — pull_saver 포트에 터널 연결
  $ngrok = Get-Command ngrok -ErrorAction SilentlyContinue
  if ($ngrok) {
    $ngrokArgs = @("http", "$PullPort")
    $ngrokProc = Start-Process -FilePath $ngrok.Source -ArgumentList $ngrokArgs -PassThru
    Write-Host ("[ngrok] PID={0} → http {1}" -f $ngrokProc.Id, $PullPort) -ForegroundColor Green
  } else {
    Write-Warning "ngrok이 설치되어 있지 않습니다. 설치 후 'ngrok http $PullPort'를 별도로 실행하세요."
  }
}

# 9) venv 열린 PowerShell 창 유지(선택)
if ($Stay) {
  # 현재 디렉터리에서 venv 활성화된 새 PowerShell 창을 띄워둔다
  $cmd = ". .\.venv\Scripts\Activate.ps1; Set-Location -Path '$PWD'; Write-Host 'Venv 활성화됨: ' $env:VIRTUAL_ENV -ForegroundColor Green"
  Start-Process powershell -ArgumentList '-NoExit','-NoLogo','-Command', $cmd
}

Write-Host "`n✅ bootstrap 완료" -ForegroundColor Green
