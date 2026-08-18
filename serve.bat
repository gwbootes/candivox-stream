@echo off
rem Serves this folder at http://localhost:8777 so OBS can load the viewer.
rem
rem Browsers refuse to fetch model files from a file:// page — the loaders use
rem the same machinery as a network request, and a file:// page counts as a
rem foreign origin, so the model comes back blocked while the page itself looks
rem fine. Serving over http sidesteps that entirely.
rem
rem Leave this window open while you stream. Close it to stop the server.
cd /D %~dp0
echo Candivox Model Stage — http://localhost:8777/index.html?model=models/test-cube.obj^&debug=1
echo Close this window to stop.
echo.
python -m http.server 8777 --bind 127.0.0.1
