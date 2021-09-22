# Aufgetretene Probleme

## ForkingTCPServer

### Problem: ForkingTCPServer funktioniert nicht auf Windows

- Ursache: Windows unterstützt kein fork()
- Lösung: Linux verwenden

### Problem: Keine Rückgabe bei "hello"-Eingabe

- Ursache: String-Vergleich falsch implementiert
- Lösung: "hello" zu b"hello" ändern
