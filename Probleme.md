# Aufgetretene Probleme

## ForkingTCPServer

### Problem: ForkingTCPServer funktioniert nicht auf Windows

- Ursache: Windows unterstützt kein fork()
- Lösung: Linux verwenden

### Problem: Keine Rückgabe bei "hello"-Eingabe

- Ursache: String-Vergleich falsch implementiert
- Lösung: "hello" zu b"hello" ändern

### Problem: Nach "hello" wird die Verbindung zum Server geschlossen

- Lösung: Eine while-Schleife im Handler verwenden

### Problem: Wie implementiert man überhaupt das TLS?

\(Erstmal ein Zertifikat erstellen: [Lets Encrypt](https://letsencrypt.org/docs/certificates-for-localhost/)\)

- Minica klonen und bauen: [MiniCA github repo](https://github.com/jsha/minica)
- (Development) Zertifikat für localhost ausstellen lassen
- CA ist minica.pem
- Mit der ssl-Library folgende Sachen machen:
  - SSL-Kontext erstellen und Public/Private Key von MiniCA laden
  - Den Socket von ForkingTCPServer mithilfe des SSL-Kontextes wrappen

### Problem: Wie testet man die TLS-Verbindung?

- Lösung: openssl s_client -verify_return_error -connect localhost:9999

### Problem: Fehlermeldung "unable to verify the first certificate"

- Ursache: self-signed Zertifikat, welches von keiner (bekannten) CA unterschrieben wurde
- Lösung: Public Key des Servers mit angeben: openssl s_client -verify_return_error -connect localhost:9999 -CAfile minica.pem
- Bei der Lets Encrypt-Methode gabs keine CA, also mit MiniCA gemacht
