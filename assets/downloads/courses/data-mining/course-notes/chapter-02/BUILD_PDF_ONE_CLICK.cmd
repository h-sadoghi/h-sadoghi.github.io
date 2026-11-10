@echo off
setlocal
cd /d "%~dp0"
echo =================== Data Mining Chapter 02 PDF ===================
where xelatex >nul 2>nul
if errorlevel 1 (
  echo [STOP] XeLaTeX not found. Install MiKTeX or TeX Live with xepersian.
  pause
  exit /b 2
)
if not exist "..\images\fig02_01_granularity.png" (
  echo [STOP] Images not found. Keep downloads and images within the Chapter02 folder.
  pause
  exit /b 2
)
xelatex -halt-on-error -interaction=nonstopmode DataMining_Chapter02.tex
if errorlevel 1 goto fail
xelatex -halt-on-error -interaction=nonstopmode DataMining_Chapter02.tex
if errorlevel 1 goto fail
echo [SUCCESS] DataMining_Chapter02.pdf generated.
pause
exit /b 0
:fail
echo [ERROR] XeLaTeX failed. Check DataMining_Chapter02.log.
pause
exit /b 1
