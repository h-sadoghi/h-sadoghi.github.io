@echo off
setlocal
cd /d "%~dp0"
set "VENV=%CD%\.site-manager-venv"
set "PYTHON_EXE=%VENV%\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
  echo Creating the local Python environment...
  py -3 -m venv "%VENV%" || goto :error
)

"%PYTHON_EXE%" -c "import flask, markdown, ruamel.yaml, pybtex" >nul 2>nul
if errorlevel 1 (
  echo Installing Site Manager dependencies. This is needed only once...
  "%PYTHON_EXE%" -m pip install --disable-pip-version-check -r "tools\site_manager\requirements.txt" || goto :error
)

echo Opening http://127.0.0.1:8765
"%PYTHON_EXE%" -m tools.site_manager --repo "%CD%"
goto :end

:error
echo.
echo Site Manager could not start. Read tools\site_manager\README_FA.md.
pause
exit /b 1

:end
endlocal
