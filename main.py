import pygame
import random
import math
from player import Player
from enemy import Goblin
from coin import Coin
from sword import Sword

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Воин против гоблинов")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (144, 238, 144)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
SKY_BLUE = (135, 206, 235)

# Шрифты
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)


# Загрузка изображений (если есть)
def load_image(path, size=None, default_color=None):
    try:
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except:
        print(f"Предупреждение: {path} не найден, используется цветной прямоугольник")
        return None


# Загружаем все изображения
warrior_img = load_image("warrior.png", (40, 40))
goblin_img = load_image("goblin.png", (35, 35))
coin_img = load_image("coin.png", (25, 25))
sword_img = load_image("sword.png", (30, 15))


# Создание фона
def create_background():
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Небо
    background.fill(SKY_BLUE)

    # Облака
    for i in range(5):
        cloud_x = random.randint(0, SCREEN_WIDTH)
        cloud_y = random.randint(20, 150)
        for j in range(5):
            pygame.draw.circle(background, WHITE,
                               (cloud_x + j * 25, cloud_y), 20)

    # Трава
    grass_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100)
    pygame.draw.rect(background, DARK_GREEN, grass_rect)

    # Текстура травы
    for _ in range(100):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(SCREEN_HEIGHT - 100, SCREEN_HEIGHT - 10)
        pygame.draw.circle(background, LIGHT_GREEN, (x, y), 3)

    return background


background = create_background()

# Группы спрайтов
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
swords = pygame.sprite.Group()

# Создание игрока
player = Player(SCREEN_WIDTH, SCREEN_HEIGHT, warrior_img)
all_sprites.add(player)

# Счет и состояние игрока
score = 0
sword_active = False
sword_timer = 0
SWORD_DURATION = 300  # Длительность действия меча (в кадрах, примерно 5 секунд при 60 FPS)

clock = pygame.time.Clock()

# Таймеры для спавна
ENEMY_SPAWN = pygame.USEREVENT + 1
COIN_SPAWN = pygame.USEREVENT + 2
SWORD_SPAWN = pygame.USEREVENT + 3
pygame.time.set_timer(ENEMY_SPAWN, 1500)  # Спавн гоблина каждые 1.5 секунды
pygame.time.set_timer(COIN_SPAWN, 2000)  # Спавн монеты каждые 2 секунды
pygame.time.set_timer(SWORD_SPAWN, 8000)  # Спавн меча каждые 8 секунд

running = True
game_over = False

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == ENEMY_SPAWN and not game_over:
            enemy = Goblin(SCREEN_WIDTH, SCREEN_HEIGHT, goblin_img, player)
            all_sprites.add(enemy)
            enemies.add(enemy)
        elif event.type == COIN_SPAWN and not game_over:
            coin = Coin(SCREEN_WIDTH, SCREEN_HEIGHT, coin_img)
            all_sprites.add(coin)
            coins.add(coin)
        elif event.type == SWORD_SPAWN and not game_over:
            sword = Sword(SCREEN_WIDTH, SCREEN_HEIGHT, sword_img)
            all_sprites.add(sword)
            swords.add(sword)

    if not game_over:
        # Обновление
        all_sprites.update()

        # Таймер меча
        if sword_active:
            sword_timer -= 1
            if sword_timer <= 0:
                sword_active = False
                player.has_sword = False

        # Проверка подбора меча
        sword_hits = pygame.sprite.spritecollide(player, swords, True)
        for sword in sword_hits:
            sword_active = True
            sword_timer = SWORD_DURATION
            player.has_sword = True

        # Проверка столкновений игрока с гоблинами
        enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
        for enemy in enemy_hits:
            if sword_active:
                # Убиваем гоблина мечом
                enemy.kill()
                score += 20  # Больше очков за убийство мечом
            else:
                # Обычное столкновение
                player.health -= 10
                # Эффект отбрасывания
                dx = player.rect.centerx - enemy.rect.centerx
                dy = player.rect.centery - enemy.rect.centery
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance > 0:
                    player.rect.x += (dx / distance) * 50
                    player.rect.y += (dy / distance) * 50

                if player.health <= 0:
                    game_over = True

        # Проверка столкновений игрока с монетами
        coin_hits = pygame.sprite.spritecollide(player, coins, True)
        for coin in coin_hits:
            score += 10

        # Отрисовка
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)

        # Отображение информации
        # Панель статистики
        pygame.draw.rect(screen, BLACK, (5, 5, 200, 80))
        pygame.draw.rect(screen, WHITE, (5, 5, 200, 80), 2)

        score_text = font.render(f"Монеты: {score}", True, YELLOW)
        screen.blit(score_text, (15, 10))

        health_text = font.render(f"Здоровье: {player.health}", True, RED)
        screen.blit(health_text, (15, 45))

        # Индикатор меча
        if sword_active:
            # Полоска времени меча
            bar_width = 200
            bar_height = 20
            bar_x = SCREEN_WIDTH - bar_width - 15
            bar_y = 15

            # Фон полоски
            pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

            # Заполнение полоски
            fill_width = int((sword_timer / SWORD_DURATION) * bar_width)
            pygame.draw.rect(screen, YELLOW, (bar_x, bar_y, fill_width, bar_height))

            # Текст
            sword_text = small_font.render("МЕЧ АКТИВИРОВАН", True, YELLOW)
            screen.blit(sword_text, (SCREEN_WIDTH - 190, bar_y + bar_height + 5))

        # Инструкция
        if not sword_active and not game_over:
            instr_text = small_font.render("Найди меч, чтобы убивать гоблинов!", True, BLACK)
            text_rect = instr_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
            # Белый фон для текста
            pygame.draw.rect(screen, WHITE, (text_rect.x - 5, text_rect.y - 5,
                                             text_rect.width + 10, text_rect.height + 10))
            pygame.draw.rect(screen, BLACK, (text_rect.x - 5, text_rect.y - 5,
                                             text_rect.width + 10, text_rect.height + 10), 2)
            screen.blit(instr_text, text_rect)

    else:
        # Экран Game Over
        screen.blit(background, (0, 0))

        # Затемнение
        dark = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        dark.set_alpha(200)
        dark.fill(BLACK)
        screen.blit(dark, (0, 0))

        game_over_text = font.render("ИГРА ОКОНЧЕНА", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

        score_text = font.render(f"Ваш счет: {score}", True, YELLOW)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))

        restart_text = small_font.render("Нажмите R для перезапуска или ESC для выхода", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50))

        # Обработка клавиш на экране Game Over
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Перезапуск игры
            game_over = False
            score = 0
            sword_active = False
            sword_timer = 0
            player.health = 100
            player.has_sword = False

            # Очистка всех спрайтов
            for sprite in all_sprites:
                sprite.kill()

            # Создание нового игрока
            player = Player(SCREEN_WIDTH, SCREEN_HEIGHT, warrior_img)
            all_sprites.add(player)

            # Пересоздание групп
            enemies.empty()
            coins.empty()
            swords.empty()

        if keys[pygame.K_ESCAPE]:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
