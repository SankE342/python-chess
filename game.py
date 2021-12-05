import pygame
import chess
import os

DIMENSIONS = WIDTH, HEIGHT = 600, 800
ORIGIN = X0, Y0 = 60, 60

WINDOW = pygame.display.set_mode(DIMENSIONS)
pygame.display.set_caption('Python Chess -by SankE')

WHITE = 255, 255, 255

FPS_CAP = 30

DIR = './assets/'

chess.start_game()

if True:
    BOARD = pygame.image.load(DIR + 'board.png')

    PAWN_W      = pygame.image.load(DIR + 'pW.png')
    ROOK_W      = pygame.image.load(DIR + 'rW.png')
    KNIGHT_W    = pygame.image.load(DIR + 'nW.png')
    BISHOP_W    = pygame.image.load(DIR + 'bW.png')
    QUEEN_W     = pygame.image.load(DIR + 'qW.png')
    KING_W      = pygame.image.load(DIR + 'kW.png')

    PAWN_B      = pygame.image.load(DIR + 'pB.png')
    ROOK_B      = pygame.image.load(DIR + 'rB.png')
    KNIGHT_B    = pygame.image.load(DIR + 'nB.png')
    BISHOP_B    = pygame.image.load(DIR + 'bB.png')
    QUEEN_B     = pygame.image.load(DIR + 'qB.png')
    KING_B      = pygame.image.load(DIR + 'kB.png')

    dct_images = {
        'White': {
            'Pawn'  : PAWN_W    , 'Rook'    : ROOK_W    , 'Knight'  : KNIGHT_W,
            'Bishop': BISHOP_W  , 'Queen'   : QUEEN_W   , 'King'    : KING_W
        },
        'Black': {
            'Pawn'  : PAWN_B    , 'Rook'    : ROOK_B    , 'Knight'  : KNIGHT_B,
            'Bishop': BISHOP_B  , 'Queen'   : QUEEN_B   , 'King'    : KING_B
        }
    }

def pos_pixels(x1, x2, reverse=False):
    # Converts pixel position in board to index in array
    if reverse: return x2//60 - 1, x1//60 - 1

    # Converts index in array to pixel position in board
    return 60*(x2 + 1), 60*(x1 + 1)

def draw_pieces():
    for row, _ in enumerate(chess.board.state):
        for col, piece in enumerate(_):
            if piece.status == 'empty': continue
            
            WINDOW.blit(
                dct_images[piece.color][piece.name], pos_pixels(row, col)
            )

def draw_board():
    WINDOW.fill(WHITE)
    WINDOW.blit(BOARD, (0, 0))

def draw():
    draw_board()
    draw_pieces()
    pygame.display.update()

def main():
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS_CAP)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
        
        draw()
        
    pygame.quit()

if __name__ == '__main__': main()