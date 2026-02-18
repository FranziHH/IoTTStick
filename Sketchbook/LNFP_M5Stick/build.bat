@echo off
set PIO_EXE=%USERPROFILE%\.platformio\penv\Scripts\platformio.exe
set ENV_NAME=unknown

IF /I "%1"=="PLUS" set ENV_NAME=m5stickc
IF /I "%1"=="PLUS2" set ENV_NAME=m5stickc_plus2

IF "%ENV_NAME%"=="unknown" (
    echo ==========================================
    echo ERROR: ENV nicht gefunden
    echo ==========================================
    echo PLUS    m5stickc
    echo PLUS2   m5stickc_plus2
    echo ==========================================
    exit /b 1
)

echo ==========================================
echo STARTE BUILD PROZESS FUER: %ENV_NAME%
echo ==========================================

:: 1. CLEAN
echo [1/3] Bereinige Build-Ordner (Clean)...
"%PIO_EXE%" run -e %ENV_NAME% --target clean
if %errorlevel% neq 0 goto error

:: 2. BUILD FILESYSTEM (SPIFFS/LittleFS)
echo [2/3] Baue Dateisystem (BuildFS)...
"%PIO_EXE%" run -e %ENV_NAME% --target buildfs
if %errorlevel% neq 0 goto error

:: 3. BUILD FIRMWARE
echo [3/3] Kompiliere Firmware (Build)...
"%PIO_EXE%" run -e %ENV_NAME%
if %errorlevel% neq 0 goto error

echo ==========================================
echo BUILD ERFOLGREICH ABGESCHLOSSEN!
echo Dein Python-Release-Script wurde ausgefuehrt.
echo ==========================================
:: pause
exit /b 0

:error
echo.
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo FEHLER BEIM BUILD PROZESS!
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
:: pause
exit /b 1