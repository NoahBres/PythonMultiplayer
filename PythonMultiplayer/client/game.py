from sys import exit
import pygame
from pygame import locals

import json

from .client import Client
from .player import Player
from .network_entity import NetworkEntity

(width, height) = (400, 300)
background = (0, 0, 0)

clock = pygame.time.Clock()
ticks_per_second = 60


class Game:
    def __init__(self, tcp_port, udp_port, socket):
        self.player = None
        self.client = None
        self.running = None

        self.tcp_port = tcp_port
        self.udp_port = udp_port
        self.socket = socket

        self.clients = {}

    def run(self):
        self.connect()
        self.player = Player()

        pygame.init()

        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(
            f"Python Multiplayer Test - {self.client.identifier}"
        )

        self.running = True

        try:
            while self.running:
                clock.tick(ticks_per_second)

                self.poll_events()
                self.update()
                self.draw(screen)

            pygame.quit()
            exit(0)
        except SystemExit:
            pygame.quit()
            exit(0)

    def poll_events(self):
        events = pygame.event.get()
        keys = pygame.key.get_pressed()

        # Check for quit
        for event in events:
            if event.type == locals.QUIT:
                self.running = False
                return
            if event.type == locals.KEYDOWN:
                if event.key == locals.K_ESCAPE:
                    self.running = False
                    return

        if keys[locals.K_w]:
            self.player.move(0, -6)
        if keys[locals.K_a]:
            self.player.move(-6, 0)
        if keys[locals.K_s]:
            self.player.move(0, 6)
        if keys[locals.K_d]:
            self.player.move(6, 0)

    def update(self):
        self.player.update()

        for identifier, client in self.clients.items():
            client.update()

        player_updates = self.player.get_network_updates()
        if len(player_updates):
            self.client.send("update", player_updates)

        def remove_self(item):
            item = item.decode("utf-8")
            item = json.loads(item)

            return item["message"]["identifier"] != self.client.identifier

        messages = self.client.get_messages()
        messages = list(filter(remove_self, messages))
        if len(messages) != 0:
            # print(messages)
            for message in messages:
                message = message.decode("utf-8")
                message = json.loads(message)
                message = message["message"]
                if message["identifier"] == "server":
                    if message["payload"].get("client-list") is not None:
                        new_items = set(message["payload"]["client-list"]) - set(
                            self.clients.keys()
                        )

                        for item in new_items:
                            if item != self.client.identifier:
                                self.clients[item] = NetworkEntity(item)

                if message["identifier"] in self.clients.keys():
                    for m in message["message"]:
                        if m[0] == "move":
                            self.clients[message["identifier"]].move(m[1][0], m[1][1])

                print(message)

    def draw(self, screen):
        screen.fill(background)

        self.player.draw(screen)

        for identifier, client in self.clients.items():
            client.draw(screen)

        pygame.display.flip()

    def connect(self):
        self.client = Client("127.0.0.1", self.tcp_port, self.udp_port, self.socket)
        self.client.register()
