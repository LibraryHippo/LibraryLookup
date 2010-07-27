@echo off
setlocal
set PYTHONPATH=%PYTHONPATH%;%~dp0\App
py.test.exe --looponfail %*
