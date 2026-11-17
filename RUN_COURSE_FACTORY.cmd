@echo off
setlocal EnableExtensions DisableDelayedExpansion
rem Course Factory stable Windows entry point; delegates all business logic to existing course_factory.py.
rem No new publisher and NO automatic Push.
set "ROOT=%~dp0"
set "PYTHON=py"
set "PYVER=-3.12"
set "FACTORY=%ROOT%tools\course_factory.py"
if not exist "%FACTORY%" goto :missing_tool
if "%~1"=="" goto :help
if /I "%~1"=="HELP" goto :help_ok
if /I "%~1"=="/?" goto :help_ok
if /I "%~1"=="NEW" goto :new
if /I "%~1"=="CHECK" goto :check
if /I "%~1"=="SELFTEST" goto :selftest
if /I "%~1"=="PUBLISH" goto :explicit_publish
rem Backward compatible primary interface: RUN_COURSE_FACTORY.cmd "C:\path\file.zip"
set "SOURCE=%~f1"
if not exist "%SOURCE%" goto :missing_input
call :python_ready
if errorlevel 1 goto :failed
"%PYTHON%" %PYVER% "%FACTORY%" publish --repo "%ROOT%" --source "%SOURCE%"
goto :finish
:explicit_publish
rem Optional explicit form PUBLISH "path" OR PUBLISH --source "path"
if /I "%~2"=="--source" (
  if "%~3"=="" goto :help
  set "SOURCE=%~f3"
) else (
  if "%~2"=="" goto :help
  set "SOURCE=%~f2"
)
if not exist "%SOURCE%" goto :missing_input
call :python_ready
if errorlevel 1 goto :failed
"%PYTHON%" %PYVER% "%FACTORY%" publish --repo "%ROOT%" --source "%SOURCE%"
goto :finish
:check
if "%~2"=="" goto :help
set "SOURCE=%~f2"
if not exist "%SOURCE%" goto :missing_input
call :python_ready
if errorlevel 1 goto :failed
"%PYTHON%" %PYVER% "%FACTORY%" check --repo "%ROOT%" --source "%SOURCE%"
goto :finish
:selftest
rem No staging/commit/push: validate the installed Python and a completed package.
if "%~2"=="" goto :help
set "SOURCE=%~f2"
if not exist "%SOURCE%" goto :missing_input
call :python_ready
if errorlevel 1 goto :failed
"%PYTHON%" %PYVER% "%FACTORY%" check --repo "%ROOT%" --source "%SOURCE%"
if errorlevel 1 goto :failed
echo [SELFTEST PASS] Existing course_factory.py accepted the package.
echo [SELFTEST PASS] No publish, Git stage, commit, or Push was requested.
exit /b 0
:new
if "%~4"=="" goto :help
call :python_ready
if errorlevel 1 goto :failed
"%PYTHON%" %PYVER% "%FACTORY%" new --repo "%ROOT%" --course "%~2" --number "%~3" --title "%~4"
goto :finish
:python_ready
"%PYTHON%" %PYVER% -c "import sys; assert sys.version_info[:2] == (3, 12)" >nul 2>&1
if errorlevel 1 (
  echo [STOP] Python 3.12 is not available via py -3.12.
  exit /b 2
)
exit /b 0
:finish
if errorlevel 1 goto :failed
echo [DONE] Command succeeded. Push only after COMMIT VERIFIED, via GitHub Desktop.
exit /b 0
:missing_tool
echo [STOP] Missing existing tool: "%FACTORY%"
exit /b 2
:missing_input
echo [STOP] Missing source file or directory: "%SOURCE%"
exit /b 2
:help
echo [USAGE] RUN_COURSE_FACTORY.cmd "C:\path\Chapter12.zip"
echo [USAGE] RUN_COURSE_FACTORY.cmd CHECK "C:\path\Chapter12.zip"
echo [USAGE] RUN_COURSE_FACTORY.cmd SELFTEST "C:\path\Chapter12.zip"
echo [USAGE] RUN_COURSE_FACTORY.cmd NEW data-mining 12 "Chapter title"
echo [USAGE] RUN_COURSE_FACTORY.cmd PUBLISH --source "C:\path\Chapter12.zip"
exit /b 2
:help_ok
echo [USAGE] RUN_COURSE_FACTORY.cmd "C:\path\Chapter12.zip"
echo [USAGE] RUN_COURSE_FACTORY.cmd CHECK "C:\path\Chapter12.zip"
echo [USAGE] RUN_COURSE_FACTORY.cmd SELFTEST "C:\path\Chapter12.zip"
echo [USAGE] RUN_COURSE_FACTORY.cmd NEW data-mining 12 "Chapter title"
exit /b 0
:failed
echo [STOP] Command failed. Do not Push.
exit /b 2
