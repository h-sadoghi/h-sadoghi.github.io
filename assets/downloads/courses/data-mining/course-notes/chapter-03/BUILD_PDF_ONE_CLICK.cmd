@echo off
setlocal
cd /d "%~dp0"
where xelatex >nul 2>nul
if errorlevel 1 (
  echo [ERROR] XeLaTeX is not on PATH. Install MiKTeX or TeX Live.
  pause
  exit /b 1
)
if not exist "..\images\fig03_01.png" (
  echo [ERROR] Chapter03\images not found next to downloads.
  pause
  exit /b 1
)
echo Building Chapter 3 Persian PDF (XeLaTeX)...
xelatex -interaction=nonstopmode -halt-on-error DataMining_Chapter03.tex > build_chapter03.log 2>&1
if errorlevel 1 (
  echo [ERROR] See build_chapter03.log
  pause
  exit /b 1
)
xelatex -interaction=nonstopmode -halt-on-error DataMining_Chapter03.tex >> build_chapter03.log 2>&1
if errorlevel 1 (echo [ERROR] Second pass failed. & pause & exit /b 1)
echo [SUCCESS] DataMining_Chapter03.pdf built.
pause
