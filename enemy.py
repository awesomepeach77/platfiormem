import pygame
import math
import random


class Goblin(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, image=None, player=None):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player = player

        # Используем изображение или создаем зеленый прямоугольник
        if image:
            self.image = image
        else:
            self.image = pygame.Surface((35, 35))
            self.image.fill('green')

        self.rect = self.image.get_rect()

        # Спавн в случайном месте у границ экрана
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            self.rect.centerx = random.randint(0, screen_width)
            self.rect.bottom = 0
        elif side == 'bottom':
            self.rect.centerx = random.randint(0, screen_width)
            self.rect.top = screen_height
        elif side == 'left':
            self.rect.right = 0
            self.rect.centery = random.randint(0, screen_height)
        else:  # right
            self.rect.left = screen_width
            self.rect.centery = random.randint(0, screen_height)

        self.speed = random.uniform(1.5, 2.5)

    def update(self):
        if self.player and self.player.alive():
            # Направление к игроку
            dx = self.player.rect.centerx - self.rect.centerx
            dy = self.player.rect.centery - self.rect.centery
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance > 0:
                # Движение к игроку
                self.rect.x += (dx / distance) * self.speed
                self.rect.y += (dy / distance) * self.speed
