@echo off
setlocal
cd /d "%~dp0"
echo ================================================================
echo DATA MINING -- CHAPTER 02 -- REPRODUCIBLE EXAMPLES
echo Data files are synthetic; no network or pip installation needed.
echo ================================================================
where py >nul 2>nul
if not errorlevel 1 (
  py -3 chapter02_examples.py
) else (
  where python >nul 2>nul
  if errorlevel 1 (
    echo [STOP] Python not found. Install Python 3.10+ or run with your existing interpreter.
    pause
    exit /b 2
  )
  python chapter02_examples.py
)
set "EXITCODE=%ERRORLEVEL%"
echo.
if not "%EXITCODE%"=="0" echo [ERROR] The Python demonstration returned exit code %EXITCODE%.
if "%EXITCODE%"=="0" echo [SUCCESS] All demonstration calculations completed.
pause
exit /b %EXITCODE%
