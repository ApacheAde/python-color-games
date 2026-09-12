#!/usr/bin/env python3
"""Lucky Reels — colorful 3-reel slot machine (play money)."""
import sys
import random
import pygame

WIDTH, HEIGHT = 820, 560
BG = (18, 10, 36)
PINK = (255, 70, 160)
CYAN = (40, 230, 255)
GOLD = (255, 205, 60)
WHITE = (255, 255, 255)

SYMBOLS = [
    ("CHERRY", (220, 30, 70), 4),
    ("LEMON", (250, 220, 40), 5),
    ("GEM", (80, 200, 255), 8),
    ("STAR", (255, 210, 40), 12),
    ("SEVEN", (255, 40, 80), 20),
    ("BELL", (255, 170, 40), 10),
]


def pick():
    return random.choice(SYMBOLS)


def payout(reels, bet):
    names = [r[0] for r in reels]
    if names[0] == names[1] == names[2]:
        return bet * next(s[2] for s in SYMBOLS if s[0] == names[0])
    if names[0] == names[1] or names[1] == names[2] or names[0] == names[2]:
        return bet * 2
    return 0


def draw_symbol(surf, symbol, rect):
    name, color, _ = symbol
    pygame.draw.rect(surf, (30, 20, 50), rect, border_radius=16)
    pygame.draw.rect(surf, color, rect, 4, border_radius=16)
    font = pygame.font.SysFont("arial", 22, bold=True)
    label = font.render(name, True, color)
    surf.blit(label, label.get_rect(center=rect.center))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lucky Reels")
    clock = pygame.time.Clock()
    title = pygame.font.SysFont("arial", 40, bold=True)
    ui = pygame.font.SysFont("arial", 26, bold=True)
    small = pygame.font.SysFont("arial", 18)

    bank = 100
    bet = 5
    reels = [pick(), pick(), pick()]
    spinning = 0
    last_win = 0
    message = "SPACE to spin"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.key == pygame.K_SPACE and spinning == 0 and bank >= bet:
                    bank -= bet
                    spinning = 18
                    last_win = 0
                    message = "Spinning..."

        if spinning:
            reels = [pick(), pick(), pick()]
            spinning -= 1
            if spinning == 0:
                last_win = payout(reels, bet)
                bank += last_win
                message = f"WIN ${last_win}!" if last_win else "No win — spin again"
                if bank < bet:
                    message = "Bank empty. Esc to quit."

        screen.fill(BG)
        pygame.draw.rect(screen, (40, 16, 70), (50, 40, WIDTH - 100, HEIGHT - 80), border_radius=28)
        pygame.draw.rect(screen, PINK, (50, 40, WIDTH - 100, HEIGHT - 80), 3, border_radius=28)
        screen.blit(title.render("LUCKY REELS", True, GOLD), (240, 58))
        screen.blit(ui.render(f"Bank ${bank}   Bet ${bet}", True, CYAN), (80, 118))

        boxes = [pygame.Rect(90 + i * 220, 190, 200, 180) for i in range(3)]
        for i, box in enumerate(boxes):
            draw_symbol(screen, reels[i], box)

        color = GOLD if last_win else WHITE
        screen.blit(ui.render(message, True, color), (80, 400))
        screen.blit(small.render("Play money only. SPACE spin   Esc quit", True, WHITE), (80, 460))
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
