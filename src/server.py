import socketserver
import ssl

"""
This Python3 module contains MyTCPServer, a ForkingTCPServer with TLS support.
When MyTCPHandler is started, "world" is returned when "hello" is sent over the
TCP connection.
The main function contains an example for using MyTCPServer with MyTCPHandler.
"""


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    Contains the request handler method for the hello world example.
    """

    def handle(self):
        """
        Is called for every incoming connection.
            Input "hello": Output "world"
            Input "end": connection is closed
            Input "": connection is closed
        """
        while True:
            self.data = self.request.recv(1024).strip()  # Retrieve data
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
    """
    TCP server class with TLS. Stop the server with Ctrl+C.
    """

    def __init__(self, server_address, cert, RequestHandlerClass, bind_and_activate=True):
        """
        Constructor. May be extended, do not override.

            Parameters:
                server_address (str, int): Hostname and Port of the Server
                cert (str, str): Paths to Public (index 0) and Private (index 1) key for the server.
                RequestHandlerClass (socketserver.BaseRequestHandler): Handler class for requests.
                bind_and_activate (bool): When false, server_bind() and server_activate() has to be called later
        """
        super(MyTCPServer, self).__init__(
            server_address, RequestHandlerClass, False)

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        # Load Public and Private key into SSL context
        self.context.load_cert_chain(cert[0], cert[1])
        self.socket = self.context.wrap_socket(
            self.socket, server_side=True)  # Add SSL to socket

        if bind_and_activate:
            self.server_bind()
            self.server_activate()


if __name__ == "__main__":
    # Example usage of the server
    HOST, PORT = "localhost", 9999
    PUB_KEY = "../certs/localhost/cert.pem"
    PRI_KEY = "../certs/localhost/key.pem"

    with MyTCPServer((HOST, PORT), (PUB_KEY, PRI_KEY), MyTCPHandler) as server:
        print("starting server")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nbye\n")
