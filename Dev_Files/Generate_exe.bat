 ```batch
 @echo off
 echo ==============================
 echo Cleaning old build files...
 echo ==============================

 rmdir /s /q build 2>nul
 rmdir /s /q dist 2>nul
 del /q *.spec 2>nul

 echo.
 echo ==============================
 echo Activating virtual environment...
 echo ==============================

 call .venv\Scripts\activate

 echo.
 echo ==============================
 echo Building EXE with PyInstaller...
 echo ==============================

pyinstaller --noconsole --icon=assets/icon.ico --paths src --collect-all openpyxl --collect-all pandas --distpath .. --name Excel_Mgr src/main.py

 echo.
 echo ==============================
 echo Build finished.
 echo Output: dist\Excel_Mgr  <-- Note: It's a directory now
 echo ==============================

 REM pause
 ```

 Users will then run the `Excel_Mgr.exe` inside the `dist\Excel_Mgr` directory.
