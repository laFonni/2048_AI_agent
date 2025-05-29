# visualize.py

import pygame
import sys
import time
from agent import ExpectimaxAgent
from game2048 import Game2048

# Konfiguracja okna
TILE_SIZE = 100
GRID_SIZE = 4
MARGIN = 5
FONT_SIZE = 36
INFO_HEIGHT = 80

WINDOW_WIDTH  = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * MARGIN
WINDOW_HEIGHT = INFO_HEIGHT + GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * MARGIN

COLORS = {
    0    : (205, 193, 180),
    2    : (238, 228, 218),
    4    : (237, 224, 200),
    8    : (242, 177, 121),
    16   : (245, 149,  99),
    32   : (246, 124,  95),
    64   : (246,  94,  59),
    128  : (237, 207, 114),
    256  : (237, 204,  97),
    512  : (237, 200,  80),
    1024 : (237, 197,  63),
    2048 : (237, 194,  46),
}

def draw_board(screen, board, score, moves, font):
    screen.fill((187, 173, 160))
    # Info panel
    pygame.draw.rect(screen, (143, 122, 102), (0, 0, WINDOW_WIDTH, INFO_HEIGHT))
    score_surf = font.render(f"Score: {score}", True, (255,255,255))
    moves_surf = font.render(f"Moves: {moves}", True, (255,255,255))
    screen.blit(score_surf, (MARGIN, MARGIN))
    screen.blit(moves_surf, (MARGIN, MARGIN + FONT_SIZE + 5))

    # Tiles
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = board[i][j]
            color = COLORS.get(value, (60,58,50))
            x = MARGIN + j * (TILE_SIZE + MARGIN)
            y = INFO_HEIGHT + MARGIN + i * (TILE_SIZE + MARGIN)
            pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE), border_radius=8)
            if value:
                text = font.render(str(value), True, (0,0,0))
                rect = text.get_rect(center=(x+TILE_SIZE//2, y+TILE_SIZE//2))
                screen.blit(text, rect)

    pygame.display.flip()

def play_with_visual(agent_depth=3, fps=5):
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("2048 AI Visualization")
    font = pygame.font.SysFont("Arial", FONT_SIZE, bold=True)
    clock = pygame.time.Clock()

    game  = Game2048()
    agent = ExpectimaxAgent(max_depth=agent_depth)
    moves = 0

    running = True
    while running:
        # obsługa zdarzeń (moglibyśmy dodać pauzę / reset)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        if not game.is_game_over():
            move = agent.get_move(game)
            if move is None:
                running = False
                break
            game.move_with_cache(move)
            moves += 1
        # rysuj
        draw_board(screen, game.board, game.get_score(), moves, font)

        # ograniczenie fps
        clock.tick(fps)

        # gdy gra skończona – wyświetl komunikat
        if game.is_game_over():
            time.sleep(1)
            running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    play_with_visual(agent_depth=4, fps=8)
