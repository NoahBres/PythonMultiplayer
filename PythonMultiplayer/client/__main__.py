import argparse
from .game import Game

parser = argparse.ArgumentParser()

parser.add_argument("--socket", dest="socket", help="Listening socket", default="1235")
parser.add_argument(
    "--tcpport", dest="tcp_port", help="Listening tcp port", default="1234"
)
parser.add_argument(
    "--udpport", dest="udp_port", help="Listening udp port", default="1234"
)

args = parser.parse_args()

if __name__ == "__main__":
    game = Game(args.tcp_port, args.udp_port, args.socket)
    game.run()
