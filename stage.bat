@echo off
rem Serves the page AND tells it where to look, on one port.
rem
rem Use this instead of serve.bat when you want follow=1, which is the only
rem way the camera can track anything inside OBS. OBS never hands a Browser
rem source your mouse, so the page has to go and ask for a position instead.
rem
rem Leave this window open while you stream. Close it to stop.
cd /D %~dp0
start /min "" cmd /c "python stage.py & pause"
echo Candivox stage started, minimised to your taskbar.
echo.
echo OBS Browser source URL:
echo   http://localhost:8777/index.html?gallery=1^&spin=15^&follow=1
echo.
echo Close the minimised "stage" window in your taskbar to stop it.
timeout /t 6 >nul
