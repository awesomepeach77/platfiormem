import pygame
from player import Player

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

player = Player()
all_sprites = pygame.sprite.Group(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    screen.fill("black")
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
