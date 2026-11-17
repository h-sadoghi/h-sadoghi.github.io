@echo off
setlocal EnableExtensions DisableDelayedExpansion
rem STABLE INTERFACE - one CMD for all registered courses.
rem RUN_COURSE_FACTORY.cmd "FULL_PATH_TO_FINAL.zip"  -> check and commit.
rem RUN_COURSE_FACTORY.cmd "FULL_PATH_TO_DRAFT_FOLDER" -> compile PDF, ZIP, check, commit.
rem RUN_COURSE_FACTORY.cmd NEW data-mining 12 "Chapter title" -> new draft workspace.
set "ROOT=%~dp0"
if not exist "%ROOT%tools\course_factory.py" goto :missing_tool
if "%~1"=="" goto :help
if /I "%~1"=="NEW" goto :new
if /I "%~1"=="CHECK" goto :check
set "SOURCE=%~f1"
if not exist "%SOURCE%" goto :missing_input
py -3.12 "%ROOT%tools\course_factory.py" publish --repo "%ROOT%" --source "%SOURCE%"
goto :finish
:new
if "%~4"=="" goto :help
py -3.12 "%ROOT%tools\course_factory.py" new --repo "%ROOT%" --course "%~2" --number "%~3" --title "%~4"
goto :finish
:check
if "%~2"=="" goto :help
py -3.12 "%ROOT%tools\course_factory.py" check --repo "%ROOT%" --source "%~f2"
goto :finish
:finish
if errorlevel 1 goto :failed
echo [DONE] Review outputs; if COMMIT VERIFIED, use GitHub Desktop to Push origin.
exit /b 0
:missing_tool
echo [STOP] Tools not installed: tools\course_factory.py
exit /b 2
:missing_input
echo [STOP] Missing source file or directory: %SOURCE%
exit /b 2
:help
echo [USAGE] RUN_COURSE_FACTORY.cmd "C:\PATH\Chapter12.zip"
echo [USAGE] RUN_COURSE_FACTORY.cmd "C:\PATH\Chapter12_WORKSPACE"
echo [USAGE] RUN_COURSE_FACTORY.cmd NEW data-mining 12 "Chapter 12 title"
echo [USAGE] RUN_COURSE_FACTORY.cmd CHECK "C:\PATH\Chapter12.zip"
exit /b 2
:failed
echo [STOP] Not ready to Push. Read error above.
exit /b 2
