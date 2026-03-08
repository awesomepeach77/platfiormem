import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill("blue")
        self.rect = self.image.get_rect(midbottom=(100, 500))
        self.speed_x = 0

    def update(self):
        keys = pygame.key.get_pressed()
        self.speed_x = 0
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
