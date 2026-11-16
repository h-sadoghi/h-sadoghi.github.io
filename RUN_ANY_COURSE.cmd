@echo off
setlocal EnableExtensions
if "%~1"=="" (
  echo [USAGE] RUN_ANY_COURSE.cmd "FULL_PATH_TO_CHAPTER.zip"
  echo [USAGE] RUN_ANY_COURSE.cmd "FULL_PATH_TO_NOTE.md" course-id
  echo Registered course ids are in tools\jupyterbook_manager\books.yml
  exit /b 2
)
set "SRC=%~f1"
set "COURSE=%~2"
set "ROOT=%~dp0"
if not exist "%ROOT%tools\universal_course_publisher.py" (
  echo [STOP] General publisher was not installed in this Git repository.
  exit /b 2
)
if "%COURSE%"=="" (
  py -3.12 "%ROOT%tools\universal_course_publisher.py" --repo "%ROOT%" --source "%SRC%" --commit
) else (
  py -3.12 "%ROOT%tools\universal_course_publisher.py" --repo "%ROOT%" --source "%SRC%" --course "%COURSE%" --commit
)
if errorlevel 1 (
  echo [STOP] NOT ready for GitHub Desktop Push.
  exit /b 2
)
echo [DONE] Local Git commit verified. GitHub Desktop: Push origin.
exit /b 0
