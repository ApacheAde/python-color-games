#!/usr/bin/env python3
"""Memory Flip — colorful matching pairs."""
import random
import sys

import pygame

WIDTH, HEIGHT = 760, 640
BG = (24, 28, 56)
BACK = (70, 90, 200)
WHITE = (250, 250, 250)
GOLD = (255, 210, 70)

PALETTE = [
    (239, 71, 111),
    (255, 209, 102),
    (6, 214, 160),
    (17, 138, 178),
    (7, 59, 76),
    (131, 56, 236),
    (255, 0, 110),
    (0, 245, 212),
]
SHAPES = ["●", "■", "▲", "◆", "★", "✚", "♥", "☀"]


def new_board():
    pairs = list(range(8)) * 2
    random.shuffle(pairs)
    return pairs


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Memory Flip")
    clock = pygame.time.Clock()
    title = pygame.font.SysFont("arial", 32, bold=True)
    glyph = pygame.font.SysFont("dejavusans", 36, bold=True)
    ui = pygame.font.SysFont("arial", 20, bold=True)

    board = new_board()
    revealed = [False] * 16
    matched = [False] * 16
    selected = []
    freeze = 0
    moves = 0
    won = False

    cols, rows = 4, 4
    margin_x, margin_y = 80, 110
    gap = 16
    cw = (WIDTH - margin_x * 2 - gap * (cols - 1)) // cols
    ch = (HEIGHT - margin_y - 80 - gap * (rows - 1)) // rows

    def cell_rect(i):
        r, c = divmod(i, cols)
        return pygame.Rect(margin_x + c * (cw + gap), margin_y + r * (ch + gap), cw, ch)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.key == pygame.K_r:
                    board = new_board()
                    revealed = [False] * 16
                    matched = [False] * 16
                    selected = []
                    freeze = 0
                    moves = 0
                    won = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and freeze == 0 and not won:
                pos = event.pos
                for i in range(16):
                    if cell_rect(i).collidepoint(pos) and not revealed[i] and not matched[i]:
                        revealed[i] = True
                        selected.append(i)
                        if len(selected) == 2:
                            moves += 1
                            a, b = selected
                            if board[a] == board[b]:
                                matched[a] = matched[b] = True
                                selected = []
                                if all(matched):
                                    won = True
                            else:
                                freeze = 35
                        break

        if freeze:
            freeze -= 1
            if freeze == 0:
                for i in selected:
                    revealed[i] = False
                selected = []

        screen.fill(BG)
        screen.blit(title.render("MEMORY FLIP", True, GOLD), (250, 24))
        screen.blit(ui.render(f"Moves {moves}    R new game    click two cards", True, WHITE), (80, 70))
        if won:
            screen.blit(title.render("CLEAR!", True, GOLD), (310, 580))

        for i in range(16):
            rect = cell_rect(i)
            pid = board[i]
            if revealed[i] or matched[i]:
                pygame.draw.rect(screen, PALETTE[pid], rect, border_radius=12)
                mark = glyph.render(SHAPES[pid], True, WHITE)
                screen.blit(mark, mark.get_rect(center=rect.center))
            else:
                pygame.draw.rect(screen, BACK, rect, border_radius=12)
                pygame.draw.rect(screen, (160, 180, 255), rect, 3, border_radius=12)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
