@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
if not exist ".venv-jupyterbook\Scripts\python.exe" call SETUP_JUPYTERBOOK.cmd
if errorlevel 1 exit /b 1
".venv-jupyterbook\Scripts\python.exe" -m tools.jupyterbook_manager --repo "%CD%" build --book image-processing --clean
if errorlevel 1 exit /b 1
echo Book created in courses\image-processing\book\_build\html
exit /b 0
