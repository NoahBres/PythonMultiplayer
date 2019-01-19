import pygame


class NetworkEntity(pygame.sprite.Sprite):
    def __init__(self, identifier):
        super(NetworkEntity, self).__init__()
        self.identifier = identifier

        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 100, 100))
        self.rect = self.surf.get_rect()

        self.x = 0
        self.y = 0

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.surf, (self.x, self.y))

    def move(self, x, y):
        self.x += x
        self.y += y
