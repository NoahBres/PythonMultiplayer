import uuid
import json
import socket


class Client:
    def __init__(self, addr, udp_port):
        self.identifier = str(uuid.uuid4())
        self.addr = addr
        self.udp_addr = (addr[0], int(udp_port))

        self.props = {}

    def send_tcp(self, success, data, sock):
        success_string = "True" if success else "False"
        message = json.dumps({"success": success_string, "message": data})
        sock.send(str.encode(message))

    def send_udp(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = str.encode(json.dumps({"message": message}))
        sock.sendto(message, self.udp_addr)
