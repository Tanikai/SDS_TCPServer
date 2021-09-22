# Aufgetretene Probleme

## ForkingTCPServer

### Problem: ForkingTCPServer funktioniert nicht auf Windows

- Ursache: Windows unterstützt kein fork()
- Lösung: Linux verwenden

### Problem: Keine Rückgabe bei "hello"-Eingabe

- Ursache: String-Vergleich falsch implementiert
- Lösung: "hello" zu b"hello" ändern

### Problem: Nach "hello" wird die Verbindung zum Server geschlossen

- Lösung: Eine while-Schleife verwenden

### Problem: Wie implementiert und testet man TLS?

- Lösung:
