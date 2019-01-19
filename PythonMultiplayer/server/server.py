from threading import Lock

from .tcp_server import TcpServer
from .udp_server import UdpServer


class Server:
    def __init__(self, tcp_port, udp_port):
        self.tcp_port = tcp_port
        self.udp_port = udp_port

        self.clients = {}
        self.udp_messages = []

    def start(self):
        """
        start udp and tcp server threads
        """
        lock = Lock()
        udp_server = UdpServer(self.udp_port, lock, self)
        tcp_server = TcpServer(self.tcp_port, lock, self)

        udp_server.start()
        tcp_server.start()

        is_running = True

        print("Game Server.")
        print("--------------------------------------")
        print("list : list connected users")
        print("user #user_id : print user information")
        print("quit : quit server")
        print("--------------------------------------")

        while is_running:
            cmd = input("> ")
            if cmd == "list":
                print(self.clients)
            elif cmd == "quit":
                print("Shutting down server...")
                udp_server.is_listening = False
                tcp_server.is_listening = False
                is_running = False

        udp_server.join()
        tcp_server.join()
