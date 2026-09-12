#!/usr/bin/env python3
"""Color Wheel — simple 3-color roulette (play money)."""
import sys
import math
import random
import pygame

WIDTH, HEIGHT = 860, 620
BG = (16, 18, 32)
RED = (210, 36, 48)
BLACK = (22, 22, 28)
GREEN = (20, 150, 70)
GOLD = (255, 205, 70)
WHITE = (245, 245, 245)
CYAN = (80, 220, 255)

POCKETS = ["G"] + ["R", "B"] * 5 + ["R"]
COLORS = {"R": RED, "B": BLACK, "G": GREEN}
PAY = {"R": 2, "B": 2, "G": 12}


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Color Wheel")
    clock = pygame.time.Clock()
    title = pygame.font.SysFont("arial", 36, bold=True)
    ui = pygame.font.SysFont("arial", 24, bold=True)
    small = pygame.font.SysFont("arial", 18)

    bank = 150
    bet = 10
    choice = "R"
    angle = 0.0
    spin_v = 0.0
    spinning = False
    result = None
    message = "1 red  2 black  3 green   SPACE spin"

    cx, cy, radius = 430, 300, 170
    n = len(POCKETS)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if not spinning:
                    if event.key == pygame.K_1:
                        choice = "R"
                        message = "Bet on RED"
                    if event.key == pygame.K_2:
                        choice = "B"
                        message = "Bet on BLACK"
                    if event.key == pygame.K_3:
                        choice = "G"
                        message = "Bet on GREEN (12x)"
                    if event.key == pygame.K_SPACE and bank >= bet:
                        bank -= bet
                        spinning = True
                        result = None
                        spin_v = random.uniform(18, 28)
                        message = "Wheel spinning..."

        if spinning:
            angle = (angle + spin_v) % 360
            spin_v *= 0.985
            if spin_v < 0.15:
                spinning = False
                spin_v = 0
                pointer = (-angle) % 360
                idx = int(pointer / (360 / n)) % n
                result = POCKETS[idx]
                if result == choice:
                    win = bet * PAY[choice]
                    bank += win
                    message = f"Hit {result}! +${win}"
                else:
                    message = f"Landed {result}. No win."
                if bank < bet:
                    message += "  Bank empty."

        screen.fill(BG)
        screen.blit(title.render("COLOR WHEEL", True, GOLD), (280, 20))
        screen.blit(ui.render(f"Bank ${bank}   Bet ${bet}   On {choice}", True, CYAN), (40, 70))

        start = math.radians(angle)
        slice_deg = 360 / n
        for i, p in enumerate(POCKETS):
            a0 = start + math.radians(i * slice_deg)
            points = [(cx, cy)]
            for step in range(8):
                a = a0 + math.radians(slice_deg * step / 7)
                points.append((cx + radius * math.cos(a), cy + radius * math.sin(a)))
            pygame.draw.polygon(screen, COLORS[p], points)
        pygame.draw.circle(screen, GOLD, (cx, cy), radius, 4)
        pygame.draw.circle(screen, (40, 40, 50), (cx, cy), 28)
        pygame.draw.polygon(screen, GOLD, [(cx - 10, cy - radius - 18), (cx + 10, cy - radius - 18), (cx, cy - radius + 8)])

        screen.blit(ui.render(message, True, WHITE), (40, 500))
        screen.blit(small.render("Play money. 1/2/3 pick color, SPACE spin, Esc quit", True, WHITE), (40, 540))
        if result:
            blob = COLORS[result]
            pygame.draw.circle(screen, blob, (780, 90), 22)
            pygame.draw.circle(screen, WHITE, (780, 90), 22, 2)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
