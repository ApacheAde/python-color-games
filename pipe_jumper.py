#!/usr/bin/env python3
"""Pipe Jumper — colorful original platformer (not a Mario emulator)."""
import sys

import pygame

WIDTH, HEIGHT = 960, 540
GRAVITY = 0.55
JUMP = -12.2
SPEED = 5.4
SKY = (92, 178, 255)
GREEN = (46, 168, 62)
DIRT = (139, 90, 43)
GOLD = (255, 210, 50)
RED = (220, 50, 50)
NAVY = (28, 48, 92)
WHITE = (255, 255, 255)
HAT = (210, 40, 40)
SKIN = (255, 210, 160)
SHIRT = (40, 90, 220)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 40)
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.facing = 1

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        self.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -SPEED
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = SPEED
            self.facing = 1
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vy = JUMP
            self.on_ground = False

        self.vy += GRAVITY
        self.rect.x += int(self.vx)
        self._collide(platforms, dx=True)
        self.rect.y += int(self.vy)
        self.on_ground = False
        self._collide(platforms, dx=False)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def _collide(self, platforms, dx):
        for p in platforms:
            if self.rect.colliderect(p):
                if dx:
                    if self.vx > 0:
                        self.rect.right = p.left
                    elif self.vx < 0:
                        self.rect.left = p.right
                else:
                    if self.vy > 0:
                        self.rect.bottom = p.top
                        self.vy = 0
                        self.on_ground = True
                    elif self.vy < 0:
                        self.rect.top = p.bottom
                        self.vy = 0

    def draw(self, surf):
        r = self.rect
        pygame.draw.rect(surf, SHIRT, (r.x + 4, r.y + 16, 24, 18))
        pygame.draw.rect(surf, NAVY, (r.x + 6, r.y + 32, 8, 8))
        pygame.draw.rect(surf, NAVY, (r.x + 18, r.y + 32, 8, 8))
        pygame.draw.ellipse(surf, SKIN, (r.x + 6, r.y + 6, 20, 16))
        brim = r.x + 2 if self.facing < 0 else r.x + 8
        pygame.draw.rect(surf, HAT, (r.x + 4, r.y, 24, 10))
        pygame.draw.rect(surf, HAT, (brim, r.y + 8, 22, 4))


class Enemy:
    def __init__(self, x, y, left, right):
        self.rect = pygame.Rect(x, y, 28, 24)
        self.left = left
        self.right = right
        self.vx = 1.8

    def update(self):
        self.rect.x += int(self.vx)
        if self.rect.left <= self.left or self.rect.right >= self.right:
            self.vx *= -1

    def draw(self, surf):
        pygame.draw.ellipse(surf, (160, 80, 40), self.rect)
        pygame.draw.circle(surf, WHITE, (self.rect.x + 8, self.rect.y + 10), 4)
        pygame.draw.circle(surf, WHITE, (self.rect.x + 20, self.rect.y + 10), 4)
        pygame.draw.circle(surf, (20, 20, 20), (self.rect.x + 9, self.rect.y + 10), 2)
        pygame.draw.circle(surf, (20, 20, 20), (self.rect.x + 21, self.rect.y + 10), 2)


def make_level():
    ground = pygame.Rect(0, HEIGHT - 56, WIDTH, 56)
    plats = [
        ground,
        pygame.Rect(140, 400, 160, 18),
        pygame.Rect(380, 330, 150, 18),
        pygame.Rect(620, 270, 160, 18),
        pygame.Rect(780, 400, 140, 18),
        pygame.Rect(40, 250, 120, 18),
        pygame.Rect(300, 180, 130, 18),
    ]
    coins = [
        pygame.Rect(190, 360, 16, 16),
        pygame.Rect(430, 290, 16, 16),
        pygame.Rect(680, 230, 16, 16),
        pygame.Rect(830, 360, 16, 16),
        pygame.Rect(80, 210, 16, 16),
        pygame.Rect(350, 140, 16, 16),
        pygame.Rect(500, 480, 16, 16),
    ]
    enemies = [
        Enemy(160, HEIGHT - 56 - 24, 0, 360),
        Enemy(640, 270 - 24, 620, 780),
    ]
    flag = pygame.Rect(880, 160, 16, 110)
    return plats, coins, enemies, flag


def draw_world(surf, plats, coins, enemies, flag, player, score, lives, won, dead):
    surf.fill(SKY)
    for i in range(6):
        pygame.draw.ellipse(surf, (230, 240, 255), (60 + i * 160, 40 + (i % 2) * 20, 90, 36))
    for p in plats:
        pygame.draw.rect(surf, GREEN, p)
        pygame.draw.rect(surf, DIRT, (p.x, p.y + 8, p.w, max(0, p.h - 8)))
    pygame.draw.rect(surf, (30, 160, 70), flag)
    pygame.draw.polygon(surf, RED, [(flag.right, flag.y), (flag.right + 36, flag.y + 14), (flag.right, flag.y + 28)])
    for c in coins:
        pygame.draw.circle(surf, GOLD, c.center, 9)
        pygame.draw.circle(surf, (255, 240, 160), c.center, 5)
    for e in enemies:
        e.draw(surf)
    player.draw(surf)
    font = pygame.font.SysFont("arial", 24, bold=True)
    surf.blit(font.render(f"COINS {score}   LIVES {lives}", True, WHITE), (16, 12))
    big = pygame.font.SysFont("arial", 42, bold=True)
    if won:
        msg = big.render("YOU WIN!  R to replay", True, GOLD)
        surf.blit(msg, msg.get_rect(center=(WIDTH // 2, 80)))
    elif dead:
        msg = big.render("GAME OVER  R to retry", True, RED)
        surf.blit(msg, msg.get_rect(center=(WIDTH // 2, 80)))


def main():
    pygame.init()
    pygame.display.set_caption("Pipe Jumper — original platformer")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    def reset():
        plats, coins, enemies, flag = make_level()
        return Player(40, HEIGHT - 120), plats, coins, enemies, flag, 0, 3, False, False

    player, plats, coins, enemies, flag, score, lives, won, dead = reset()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                player, plats, coins, enemies, flag, score, lives, won, dead = reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)

        if not won and not dead:
            player.update(plats)
            for e in enemies:
                e.update()
            remaining = []
            for c in coins:
                if player.rect.colliderect(c):
                    score += 1
                else:
                    remaining.append(c)
            coins = remaining
            for e in enemies[:]:
                if player.rect.colliderect(e.rect):
                    if player.vy > 0 and player.rect.bottom - e.rect.top < 18:
                        enemies.remove(e)
                        player.vy = JUMP * 0.55
                        score += 2
                    else:
                        lives -= 1
                        player.rect.topleft = (40, HEIGHT - 120)
                        player.vy = 0
                        if lives <= 0:
                            dead = True
            if player.rect.top > HEIGHT:
                lives -= 1
                player.rect.topleft = (40, HEIGHT - 120)
                player.vy = 0
                if lives <= 0:
                    dead = True
            if player.rect.colliderect(flag):
                won = True

        draw_world(screen, plats, coins, enemies, flag, player, score, lives, won, dead)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
