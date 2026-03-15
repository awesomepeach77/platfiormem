import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, image=None):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Используем изображение или создаем синий прямоугольник
        if image:
            self.image = image
        else:
            self.image = pygame.Surface((40, 40))
            self.image.fill('blue')

        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)

        self.speed = 5
        self.health = 100
        self.has_sword = False

    def update(self):
        keys = pygame.key.get_pressed()

        # Движение во все стороны
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1

        # Нормализация диагонального движения
        if dx != 0 and dy != 0:
            dx *= 0.7
            dy *= 0.7

        # Применяем движение
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # Границы экрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height
