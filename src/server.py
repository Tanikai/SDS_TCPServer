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
            if self.data == b"end":
                print("\nConnection closed\n")
                break
            if self.data == b"":
                print("\nConnection closed\n")
                break

class MyTCPServer(socketserver.ForkingTCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        super(MyTCPServer, self).__init__(server_address, RequestHandlerClass, False)
        # socketserver.ForkingTCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.load_cert_chain(PUBLIC_KEY_PATH, PRIVATE_KEY_PATH)

        self.socket = self.context.wrap_socket(self.socket, server_side=True)
        if bind_and_activate:
            self.server_bind()
            self.server_activate()

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    PUBLIC_KEY_PATH = "../certs/localhost/cert.pem"
    PRIVATE_KEY_PATH = "../certs/localhost/key.pem"

    # Create the server, binding to localhost on port 9999
    # False: bind_and_activate
    with MyTCPServer((HOST, PORT), MyTCPHandler, True) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        print("starting server")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nbye\n")
