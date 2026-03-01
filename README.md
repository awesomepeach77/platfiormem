import pygame
import sys

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Hitbox:
    def __init__(self, x, y, w, h, color=GREEN, ox=0, oy=0):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.ox, self.oy = ox, oy
        self.active = True
    
    def update(self, x, y):
        self.rect.x, self.rect.y = x + self.ox, y + self.oy
    
    def draw(self, screen, cx=0, cy=0):
        if self.active:
            r = self.rect.copy()
            r.x -= cx
            r.y -= cy
            pygame.draw.rect(screen, self.color, r, 2)
    
    def collide(self, other):
        return self.rect.colliderect(other.rect)

class Entity:
    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.hitboxes = []
        self.vx = self.vy = 0
    
    def add_hitbox(self, w, h, ox=0, oy=0, color=GREEN):
        hb = Hitbox(self.x, self.y, w, h, color, ox, oy)
        self.hitboxes.append(hb)
        return hb
    
    def update(self):
        for hb in self.hitboxes:
            hb.update(self.x, self.y)
    
    def draw_hitboxes(self, screen, cx=0, cy=0):
        for hb in self.hitboxes:
            hb.draw(screen, cx, cy)

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 48)
        self.speed = 5
        self.jump = -15
        self.gravity = 0.8
        self.on_ground = False
        
        self.main_hb = self.add_hitbox(28, 44, 2, 2, BLUE)
        self.attack_hb = self.add_hitbox(40, 20, -4, 10, RED)
        self.attack_hb.active = False
        self.feet_hb = self.add_hitbox(20, 5, 6, 43, (255,255,0))
    
    def move(self, dir):
        self.vx = dir * self.speed
    
    def do_jump(self):
        if self.on_ground:
            self.vy = self.jump
            self.on_ground = False
    
    def attack(self, active):
        self.attack_hb.active = active
    
    def update(self, platforms):
        self.vy += self.gravity
        self.x += self.vx
        self.check_collisions_x(platforms)
        self.y += self.vy
        self.check_collisions_y(platforms)
        super().update()
        self.check_ground(platforms)
    
    def check_collisions_x(self, platforms):
        for p in platforms:
            if self.main_hb.collide(p.hb):
                if self.vx > 0:
                    self.x = p.hb.rect.left - self.main_hb.rect.width - self.main_hb.ox
                elif self.vx < 0:
                    self.x = p.hb.rect.right - self.main_hb.ox
                self.vx = 0
    
    def check_collisions_y(self, platforms):
        for p in platforms:
            if self.main_hb.collide(p.hb):
                if self.vy > 0:
                    self.y = p.hb.rect.top - self.main_hb.rect.height - self.main_hb.oy
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.y = p.hb.rect.bottom - self.main_hb.oy
                    self.vy = 0
    
    def check_ground(self, platforms):
        self.on_ground = False
        self.feet_hb.update(self.x, self.y)
        for p in platforms:
            if self.feet_hb.collide(p.hb) and self.vy >= 0:
                self.on_ground = True
                break

class Platform:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.hb = Hitbox(x, y, w, h, GREEN)
    
    def draw(self, screen, cx=0, cy=0):
        r = self.rect.copy()
        r.x -= cx
        r.y -= cy
        pygame.draw.rect(screen, (100,100,100), r)
        self.hb.draw(screen, cx, cy)

class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 32)
        self.main_hb = self.add_hitbox(30, 30, 1, 1, RED)
        self.damage_hb = self.add_hitbox(32, 32, 0, 0, (255,100,100))
        self.speed = 2
        self.dir = 1
    
    def update(self, platforms):
        self.x += self.speed * self.dir
        for p in platforms:
            if self.main_hb.collide(p.hb):
                self.dir *= -1
                break
        super().update()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Платформер")
        self.clock = pygame.time.Clock()
        self.running = True
        self.debug = True
        
        self.player = Player(100, 100)
        self.platforms = [
            Platform(0, 550, 800, 50),
            Platform(200, 450, 200, 20),
            Platform(500, 350, 150, 20),
        ]
        self.enemy = Enemy(400, 500)
        self.cx = self.cy = 0
    
    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.player.do_jump()
                elif e.key == pygame.K_f:
                    self.player.attack(True)
                elif e.key == pygame.K_d:
                    self.debug = not self.debug
            elif e.type == pygame.KEYUP and e.key == pygame.K_f:
                self.player.attack(False)
    
    def update(self):
        keys = pygame.key.get_pressed()
        dir = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dir = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dir = 1
        self.player.move(dir)
        
        self.player.update(self.platforms)
        self.enemy.update(self.platforms)
        
        if self.player.attack_hb.active and self.player.attack_hb.collide(self.enemy.main_hb):
            print("Попадание!")
        
        if self.player.main_hb.collide(self.enemy.damage_hb):
            print("Урон!")
        
        self.cx = self.player.x - SCREEN_WIDTH//2 + self.player.w//2
        self.cy = self.player.y - SCREEN_HEIGHT//2 + self.player.h//2
    
    def draw(self):
        self.screen.fill(WHITE)
        
        for p in self.platforms:
            p.draw(self.screen, self.cx, self.cy)
        
        # Враг
        r = pygame.Rect(self.enemy.x, self.enemy.y, self.enemy.w, self.enemy.h)
        r.x -= self.cx
        r.y -= self.cy
        pygame.draw.rect(self.screen, RED, r)
        if self.debug:
            self.enemy.draw_hitboxes(self.screen, self.cx, self.cy)
        
        # Игрок
        r = pygame.Rect(self.player.x, self.player.y, self.player.w, self.player.h)
        r.x -= self.cx
        r.y -= self.cy
        pygame.draw.rect(self.screen, BLUE, r)
        if self.debug:
            self.player.draw_hitboxes(self.screen, self.cx, self.cy)
        
        font = pygame.font.Font(None, 36)
        self.screen.blit(font.render(f"Debug: {'ON' if self.debug else 'OFF'} (D)", True, (0,0,0)), (10,10))
        self.screen.blit(font.render("A/D - движение, Space - прыжок, F - атака", True, (0,0,0)), (10,50))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().run()
