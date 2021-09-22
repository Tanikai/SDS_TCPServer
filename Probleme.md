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

### Problem: Wie implementiert man überhaupt das TLS?

- Erstmal ein Zertifikat erstellen: [Lets Encrypt](https://letsencrypt.org/docs/certificates-for-localhost/)
- Mithilfe der ssl-Library wrap_socket verwenden

Zweite Lösung:

- Minica klonen und bauen: [MiniCA github repo](https://github.com/jsha/minica)
- (Development) Zertifikat für localhost ausstellen lassen
- CA ist minica.pem

### Problem: Wie testet man die TLS-Verbindung?

- Lösung: openssl s_client -verify_return_error -connect localhost:8080

### Problem: Fehlermeldung "unable to verify the first certificate"

- Ursache: self-signed Zertifikat, welches von keiner CA unterschrieben wurde
- Lösung: Public Key des Servers mit angeben: openssl s_client -verify_return_error -connect localhost:8080 -CAfile minica.pem
- Bei der Lets Encrypt-Methode gabs keine CA, also mit MiniCA gemacht
