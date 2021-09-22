import socketserver
import ssl

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        while True:
            self.data = self.request.recv(1024).strip()
            print("{} wrote:".format(self.client_address[0]))
            print(self.data)

            result = "\n"
            if self.data == b"hello":
                result = "world\n"
                self.request.sendall(bytes(result, "utf-8"))
            if self.data ==b"end":
                break
            if self.data ==b"":
                break

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    PUBLIC_KEY_PATH = "../certs/localhost/cert.pem"
    PRIVATE_KEY_PATH = "../certs/localhost/key.pem"

    # Create the server, binding to localhost on port 9999
    # False: bind_and_activate
    with socketserver.ForkingTCPServer((HOST, PORT), MyTCPHandler, False) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(PUBLIC_KEY_PATH, PRIVATE_KEY_PATH)

        server.socket = context.wrap_socket(server.socket, server_side=True)
        server.server_bind()
        server.server_activate()
        print("starting server")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nbye\n")
