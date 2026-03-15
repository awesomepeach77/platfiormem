import pygame
import random


class Sword(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, image=None):
        super().__init__()

        # Используем изображение или создаем серый прямоугольник
        if image:
            self.image = image
        else:
            self.image = pygame.Surface((30, 15))
            self.image.fill((192, 192, 192))  # Серебристый цвет
            # Добавляем простые детали
            pygame.draw.rect(self.image, (139, 69, 19), (0, 5, 8, 5))  # Рукоятка
            pygame.draw.rect(self.image, (255, 215, 0), (8, 2, 20, 11))  # Лезвие

        self.rect = self.image.get_rect()

        # Случайная позиция
        self.rect.x = random.randint(30, screen_width - 30)
        self.rect.y = random.randint(30, screen_height - 30)
