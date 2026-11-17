@echo off
setlocal EnableExtensions DisableDelayedExpansion
rem Fixed universal course publisher: explicit --source and no parenthesized block around Python.
if "%~1"=="" goto :usage
set "ROOT=%~dp0"
if not exist "%~f1" goto :missing
if not exist "%ROOT%tools\universal_course_publisher.py" goto :missing_tool
if "%~2"=="" goto :zip
py -3.12 "%ROOT%tools\universal_course_publisher.py" --repo "%ROOT%" --source "%~f1" --course "%~2" --commit
goto :done
:zip
py -3.12 "%ROOT%tools\universal_course_publisher.py" --repo "%ROOT%" --source "%~f1" --commit
:done
if errorlevel 1 goto :failed
echo [COMMIT VERIFIED] Course files are in local Git HEAD. GitHub Desktop: Push origin.
exit /b 0
:usage
echo [USAGE] RUN_ANY_COURSE.cmd "C:\FULL\PATH\TO\CHAPTER.zip"
echo [USAGE] RUN_ANY_COURSE.cmd "C:\FULL\PATH\TO\lesson.md" image-processing
exit /b 2
:missing
echo [STOP] Input file does not exist: %~f1
exit /b 2
:missing_tool
echo [STOP] universal_course_publisher.py missing from the site repository.
exit /b 2
:failed
echo [STOP] No Push until this error is resolved.
exit /b 2
