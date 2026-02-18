@echo off
setlocal enabledelayedexpansion

REM Der Pfad des Ordners, den du daraufgezogen hast
set "targetDir=%~1"
set "folderName=%~n1"

if "%targetDir%"=="" (
    echo BITTE EINEN ORDNER AUF DIESE DATEI ZIEHEN!
    pause
    exit /b
)

echo Verarbeite Ordner: "%targetDir%"
cd /d "%targetDir%"

if exist "esptool.exe" (
    echo Entferne veraltetes esptool.exe ...
    del /f /q "esptool.exe"
)

REM Wir bauen den Befehl zusammen. 
REM Wir nutzen die Pfade aus deinem Original-Script.

if /I "%folderName%"=="M5UpdatePlus2" (
    echo *** M5StickPlus2 ***
	set image=LNFP_M5Stick_Plus2_Update.bin
	
	esptool --chip esp32 merge-bin ^
	  -o LNFP_M5Stick_Plus2_Update.bin ^
	  --target-offset 0x10000 ^
	  --flash-mode dio ^
	  --flash-freq 80m ^
	  --flash-size 8MB ^
	  0x10000 LNFP_M5Stick.ino.bin ^
	  0x670000 LNFP_M5Stick.spiffs.bin
) else (
    echo *** M5Stick ***
    set image=LNFP_M5Stick_Update.bin
	
    esptool --chip esp32 merge-bin ^
      -o LNFP_M5Stick_Update.bin ^
	  --target-offset 0x10000 ^
      --flash-mode dio ^
      --flash-freq 80m ^
      --flash-size 4MB ^
      0x10000 LNFP_M5Stick.ino.bin ^
      0x210000 LNFP_M5Stick.spiffs.bin
)

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ERFOLG! Die Datei "%image%" wurde im Ordner erstellt.
) else (
    echo.
    echo FEHLER! Irgendwas hat nicht geklappt. Stimmen die Unterordner?
)

echo.
echo press any key
pause > nul
