#!/usr/bin/env python3
"""Neon Blackjack — colorful 21 against the dealer."""
import sys
import random
import pygame

WIDTH, HEIGHT = 900, 600
GREEN_FELT = (12, 92, 52)
NEON = (40, 255, 180)
GOLD = (255, 210, 70)
WHITE = (250, 250, 250)
RED = (220, 40, 60)
NAVY = (18, 28, 70)
PURPLE = (90, 40, 140)

SUITS = ["♥", "♦", "♣", "♠"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


def value_of(card):
    rank = card[0]
    if rank in ("J", "Q", "K"):
        return 10
    if rank == "A":
        return 11
    return int(rank)


def hand_total(hand):
    total = sum(value_of(c) for c in hand)
    aces = sum(1 for c in hand if c[0] == "A")
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def new_deck():
    deck = [(r, s) for s in SUITS for r in RANKS]
    random.shuffle(deck)
    return deck


def draw_card(surf, card, x, y, hidden=False):
    w, h = 78, 110
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surf, WHITE, rect, border_radius=8)
    pygame.draw.rect(surf, (30, 30, 40), rect, 2, border_radius=8)
    if hidden:
        pygame.draw.rect(surf, PURPLE, rect.inflate(-10, -10), border_radius=6)
        pygame.draw.rect(surf, NEON, rect.inflate(-10, -10), 2, border_radius=6)
        return
    rank, suit = card
    color = RED if suit in ("♥", "♦") else NAVY
    font = pygame.font.SysFont("arial", 22, bold=True)
    big = pygame.font.SysFont("arial", 36, bold=True)
    surf.blit(font.render(rank, True, color), (x + 8, y + 6))
    surf.blit(big.render(suit, True, color), (x + 24, y + 38))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neon Blackjack")
    clock = pygame.time.Clock()
    title = pygame.font.SysFont("arial", 36, bold=True)
    ui = pygame.font.SysFont("arial", 24, bold=True)
    small = pygame.font.SysFont("arial", 18)

    bank = 200
    bet = 10
    deck = new_deck()
    player = []
    dealer = []
    state = "idle"
    message = "Press N to deal  |  H hit   S stand"

    def deal():
        nonlocal deck, player, dealer, state, bank, bet, message
        if bank < bet:
            message = "Bank empty — game over. Esc to quit."
            return
        if len(deck) < 15:
            deck = new_deck()
        bank -= bet
        player = [deck.pop(), deck.pop()]
        dealer = [deck.pop(), deck.pop()]
        state = "player"
        if hand_total(player) == 21:
            settle()
        else:
            message = "Hit (H) or Stand (S)"

    def settle():
        nonlocal state, bank, message, dealer, deck
        while hand_total(dealer) < 17:
            dealer.append(deck.pop())
        pt, dt = hand_total(player), hand_total(dealer)
        if pt > 21:
            message = "Bust! Dealer wins."
        elif dt > 21 or pt > dt:
            win = bet * 2
            if pt == 21 and len(player) == 2:
                win = int(bet * 2.5)
                message = f"Blackjack! +{win}"
            else:
                message = f"You win +{win}"
            bank += win
        elif pt == dt:
            bank += bet
            message = "Push. Bet returned."
        else:
            message = "Dealer wins."
        state = "idle"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.key == pygame.K_n and state == "idle":
                    deal()
                if event.key == pygame.K_h and state == "player":
                    player.append(deck.pop())
                    if hand_total(player) >= 21:
                        settle()
                if event.key == pygame.K_s and state == "player":
                    settle()

        screen.fill(GREEN_FELT)
        pygame.draw.rect(screen, (8, 60, 34), (40, 30, WIDTH - 80, HEIGHT - 60), border_radius=24)
        pygame.draw.rect(screen, NEON, (40, 30, WIDTH - 80, HEIGHT - 60), 3, border_radius=24)
        screen.blit(title.render("NEON BLACKJACK", True, GOLD), (280, 44))
        screen.blit(ui.render(f"Bank ${bank}   Bet ${bet}", True, WHITE), (60, 96))
        screen.blit(small.render(message, True, NEON), (60, 130))

        screen.blit(ui.render("DEALER", True, WHITE), (60, 170))
        hide = state == "player"
        for i, c in enumerate(dealer):
            draw_card(screen, c, 60 + i * 88, 205, hidden=(hide and i == 1))
        if state != "player" and dealer:
            screen.blit(small.render(str(hand_total(dealer)), True, GOLD), (60, 322))

        screen.blit(ui.render("YOU", True, WHITE), (60, 360))
        for i, c in enumerate(player):
            draw_card(screen, c, 60 + i * 88, 395)
        if player:
            screen.blit(small.render(str(hand_total(player)), True, GOLD), (60, 512))

        screen.blit(small.render("N deal   H hit   S stand   Esc quit", True, WHITE), (560, 540))
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
