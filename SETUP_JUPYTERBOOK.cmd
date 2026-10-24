@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
set "VENV=%CD%\.venv-jupyterbook"
set "PYTHON_EXE=%VENV%\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
  echo Creating the private Jupyter Book environment with Python 3.12...
  py -3.12 -m venv "%VENV%" || goto :error
)

"%PYTHON_EXE%" -c "import importlib.metadata as m; expected={'jupyter-book':'1.0.4.post1','Sphinx':'7.4.7','docutils':'0.21.2','myst-parser':'3.0.1','myst-nb':'1.1.2','sphinx-book-theme':'1.1.4','sphinx-design':'0.6.1','nbformat':'5.10.4','ipykernel':'6.29.5','nbconvert':'7.16.6','ruamel.yaml':'0.18.6','pytest':'8.3.5'}; assert all(m.version(k)==v for k,v in expected.items())" >nul 2>nul
if errorlevel 1 (
  echo Installing the pinned Jupyter Book dependencies. This can take several minutes...
  set "PIP_DEFAULT_TIMEOUT=300"
  set "PIP_RETRIES=10"
  "%PYTHON_EXE%" -m pip install --disable-pip-version-check --upgrade-strategy only-if-needed -r "tools\jupyterbook_manager\requirements-lock.txt" || goto :error
) else (
  echo The pinned dependencies are already installed.
)

"%PYTHON_EXE%" -m pip check || goto :error
"%VENV%\Scripts\jupyter-book.exe" --version || goto :error
echo.
echo Setup completed. Run RUN_JUPYTERBOOK_MANAGER.cmd.
exit /b 0

:error
echo.
echo Setup failed. No global Python package was changed.
exit /b 1
