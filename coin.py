import pygame
import random


class Coin(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, image=None):
        super().__init__()

        # Используем изображение или создаем желтый прямоугольник
        if image:
            self.image = image
        else:
            self.image = pygame.Surface((25, 25))
            self.image.fill('yellow')

        self.rect = self.image.get_rect()

        # Случайная позиция
        self.rect.x = random.randint(30, screen_width - 30)
        self.rect.y = random.randint(30, screen_height - 30)
