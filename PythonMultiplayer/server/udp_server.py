from threading import Thread
import socket
import json


class UdpServer(Thread):
    def __init__(self, udp_port, lock, main_server):
        Thread.__init__(self)
        self.lock = lock
        self.is_listening = True
        self.udp_port = int(udp_port)

        self.sock = None
        self.main_server = main_server

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", self.udp_port))
        self.sock.setblocking(False)
        self.sock.settimeout(5)

        while self.is_listening:
            try:
                data, addr = self.sock.recvfrom(1024)
            except socket.timeout:
                continue

            try:
                data = json.loads(data)

                identifier = data.get("identifier")
                payload = data.get("payload")
                action = data.get("action")

                try:
                    self.lock.acquire()

                    if action == "update":
                        client = self.main_server.clients[identifier]

                        for action in payload:
                            if action[0] == "move":
                                client.props["x"] = (
                                    client.props.get("x", 0) + action[1][0]
                                )
                                client.props["y"] = (
                                    client.props.get("y", 0) + action[1][0]
                                )
                        self.main_server.udp_messages.append(
                            {"identifier": identifier, "message": payload}
                        )

                    self.send_messages()
                finally:
                    self.lock.release()
            except KeyError:
                print(f"JSON from {addr}:{addr} is not valid")
            except ValueError:
                print(data)
                print(f"Message from {addr}:{addr} is not valid json string")

        self.stop()

    def stop(self):
        self.sock.close()

    def send_messages(self):
        for message in self.main_server.udp_messages:
            print(message)
            for identifier, client in self.main_server.clients.items():
                client.send_udp(message)
        self.main_server.udp_messages = []
