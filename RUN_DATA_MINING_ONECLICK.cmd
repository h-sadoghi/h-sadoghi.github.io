@echo off
setlocal EnableExtensions DisableDelayedExpansion
REM Repository-owned Data Mining chapter publisher.
set "REPO=%~dp0"
set "TOOLS=%REPO%tools\data_mining_oneclick.py"
set "INBOX=%REPO%..\_COURSE_INBOX\COURSES\DATA_MINING\CHAPTERS"
set "PY=%REPO%.venv-jupyterbook\Scripts\python.exe"
set "PY_ARGS="
set "BUILD=--build"
if not exist "%TOOLS%" (
  echo [STOP] Publisher missing in repo: %TOOLS%
  goto FAIL
)
if not exist "%PY%" (
  set "PY=py"
  set "PY_ARGS=-3.12"
  set "BUILD="
  where py >nul 2>nul
  if errorlevel 1 (
    set "PY=python"
    set "PY_ARGS="
  )
  echo [NOTICE] Local Jupyter Book venv absent. GitHub CI will build the chapter.
)
if "%~1"=="" (
  echo [INFO] Scanning Inbox for first new/missing chapter.
  "%PY%" %PY_ARGS% "%TOOLS%" --repo "%REPO%" --inbox "%INBOX%" --commit %BUILD%
) else (
  echo [INFO] Chapter package: %~f1
  "%PY%" %PY_ARGS% "%TOOLS%" --repo "%REPO%" --source "%~f1" --commit %BUILD%
)
if errorlevel 1 goto FAIL
echo.
echo [DONE] Package processed. Push verified local commit with GitHub Desktop.
pause
exit /b 0
:FAIL
echo.
echo [STOP] Not published. Do not Push until this error is solved.
pause
exit /b 2
