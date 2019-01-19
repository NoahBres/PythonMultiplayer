from threading import Thread
import socket
import json

from .client import Client


class TcpServer(Thread):
    def __init__(self, tcp_port, lock, main_server):
        Thread.__init__(self)
        self.lock = lock
        self.tcp_port = int(tcp_port)
        self.is_listening = True

        self.sock = None
        self.main_server = main_server

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("0.0.0.0", self.tcp_port))
        self.sock.setblocking(False)
        self.sock.settimeout(5)

        self.sock.listen(1)

        while self.is_listening:
            try:
                conn, addr = self.sock.accept()
            except socket.timeout:
                continue

            data = conn.recv(1024)
            print(data)

            try:
                print(data)
                data = json.loads(data)

                # identifier = data.get("identifier")
                payload = data.get("payload")
                action = data.get("action")

                try:
                    self.lock.acquire()

                    if action == "register":
                        client = None

                        for registered_client in self.main_server.clients.values():
                            ip, udp_addr = registered_client.udp_addr
                            if udp_addr == payload:
                                client = registered_client
                                # client.udp_addr((addr[0], int(payload)))
                                return

                        if client is None:
                            client = Client(addr, int(payload))

                        message = json.dumps(
                            {"success": "True", "message": client.identifier}
                        )

                        # for identifier, client in self.main_server.clients.items():
                        # client.send_tcp(True, {"message": "test thing"}, conn)

                        self.main_server.clients[client.identifier] = client
                        # conn.send(
                        #     str.encode(
                        #         json.dumps(
                        #             {"success": "True", "message": "testtesttesttest"}
                        #         )
                        #     )
                        # )
                        conn.send(str.encode(message))

                        message = {
                            "identifier": "server",
                            "payload": {
                                "client-list": list(self.main_server.clients.keys())
                            },
                        }
                        for identifier, client in self.main_server.clients.items():
                            client.send_udp(message)
                finally:
                    self.lock.release()
            except KeyError:
                print("Json from {}:{} is not valid".format(addr, addr))
                conn.send(str.encode("Json is not valid"))
            except ValueError:
                print(data)
                print("Message from {}:{} is not valid json string".format(addr, addr))
                conn.send(str.encode("Message is not a valid json string"))

            conn.close()

        self.stop()

    def stop(self):
        self.sock.close()
