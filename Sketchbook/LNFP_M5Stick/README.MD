# IoTTStick Flash Tool

NEU: Das FlashTool kann den IoTTStick komplett neu flashen, updaten oder die Original Firmware wieder herstellen.
Das gesamte Tool kann in den GitHub Pages installiert werden.
Der Verweis ist aktuell in diesem Branch auf docs

### <a href="https://franzihh.github.io/IoTTStick" target="_blank">IoTTStick Flash Tool</a>

# vsCode / PlatformIO

Der IoTTStick kann ab sofort bequem mit vsCode bearbeitet und erstellt werden.
Die Ausgabe wird in den Ordner build_output kopiert.
Um ein Full Image für den ersten Flash zu erzeugen muss vor dem Build das Filesystem Image erzeugt werden.
Bei einer neuen Initialisierung (auch Neustart von vsCode wird das Build Verzeichnis und damit auch das Filesystem Image gelöscht).


#### ESP Tool not found

Wenn in den Python Scripts das ESPTool nicht gefunden wird, kann man es nachinstallieren
```%USERPROFILE%\.platformio\penv\Scripts\python.exe -m pip install esptool```

#### NTP Settings Deutsch

Server: ``de.pool.ntp.org``
Zeitzone: ``CET-1CEST,M3.5.0,M10.5.0/3``

