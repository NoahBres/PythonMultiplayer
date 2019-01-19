import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--launch", "-l", help="Launch as client or server")

parser.add_argument("--socket", dest="socket", help="Socket of client", default="1235")
parser.add_argument(
    "--tcpport", dest="tcp_port", help="Listening tcp port", default="1234"
)
parser.add_argument(
    "--udpport", dest="udp_port", help="Listening udp port", default="1234"
)

args = parser.parse_args
if __name__ == "__main__":
    if args.launch == "client":
        pass
    elif args.launch == "server":
        pass
