@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (set "PY=py -3") else (set "PY=python")
echo Chapter 3: proximity measures - synthetic examples
%PY% chapter03_examples.py > chapter03_results.json
if errorlevel 1 (echo [ERROR] Calculation failed. & pause & exit /b 1)
%PY% -m unittest test_chapter03_examples.py -v
if errorlevel 1 (echo [ERROR] Unit tests failed. & pause & exit /b 1)
echo.
echo [SUCCESS] Tests passed; chapter03_results.json created.
pause
