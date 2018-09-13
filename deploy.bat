@ECHO OFF

call check_python.bat 

IF %ERRORLEVEL% NEQ 0 GOTO FLAKE_ERRORS

gcloud app deploy --quiet App

GOTO END

:FLAKE_ERRORS

  ECHO.
  ECHO.
  ECHO Flake errors. Not deploying.
  ECHO.

:END
