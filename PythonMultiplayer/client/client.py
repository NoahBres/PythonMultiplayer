import json
import threading
import socket


class Client:
    def __init__(
        self,
        server_host,
        server_port_tcp=1234,
        server_port_udp=1234,
        client_port_udp=1235,
    ):
        self.identifier = None
        self.server_message = []
        self.client_udp = ("0.0.0.0", int(client_port_udp))
        self.lock = threading.Lock()
        self.server_listener = SocketThread(self.client_udp, self, self.lock)
        self.server_listener.start()
        self.server_udp = (server_host, int(server_port_udp))
        self.server_tcp = (server_host, int(server_port_tcp))

        # self.register()

    def send(self, action, message):
        message = json.dumps(
            {"action": action, "payload": message, "identifier": self.identifier}
        )
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(str.encode(message), self.server_udp)

    def register(self):
        message = json.dumps({"action": "register", "payload": self.client_udp[1]})
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tcp.connect(self.server_tcp)
        self.sock_tcp.send(str.encode(message))

        data = self.sock_tcp.recv(1024)
        self.sock_tcp.close()
        message = self.parse_data(data)
        self.identifier = message
        print(data)

    def parse_data(self, data):
        try:
            data = json.loads(data)
            if data["success"] == "True":
                return data["message"]
            else:
                raise Exception(data["message"])
        except ValueError:
            print(data)

    def get_messages(self):
        message = self.server_message
        self.server_message = []
        return set(message)


class SocketThread(threading.Thread):
    def __init__(self, addr, client, lock):
        """
        Client udp connection
        """
        threading.Thread.__init__(self)
        self.client = client
        self.lock = lock
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(addr)

    def run(self):
        """
        Get responses from server
        """
        while True:
            data, addr = self.sock.recvfrom(1024)
            self.lock.acquire()
            try:
                self.client.server_message.append(data)
            finally:
                self.lock.release()

    def stop(self):
        """
        Stop thread
        """
        self.sock.close()
