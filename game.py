# %%

import numpy as np
import pygame
import chess
import os

pygame.init()

DIMENSIONS = WIDTH, HEIGHT = 600, 800
ORIGIN = X0, Y0 = 60, 60

WINDOW = pygame.display.set_mode(DIMENSIONS)
pygame.display.set_caption('Python Chess -by SankE')

BLACK   = 0, 0, 0
RED     = 255, 0, 0
GREEN   = 0, 255, 0
BLUE    = 0, 0, 255
WHITE   = 255, 255, 255

FONT = pygame.font.SysFont('Comic Sans MS', 16)

FPS_CAP = 30

DIR = './assets/'

game, board = chess.Game().new_game()

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

    images = {
        'White': {
            'Pawn'  : PAWN_W    , 'Rook'    : ROOK_W    , 'Knight'  : KNIGHT_W,
            'Bishop': BISHOP_W  , 'Queen'   : QUEEN_W   , 'King'    : KING_W
        },
        'Black': {
            'Pawn'  : PAWN_B    , 'Rook'    : ROOK_B    , 'Knight'  : KNIGHT_B,
            'Bishop': BISHOP_B  , 'Queen'   : QUEEN_B   , 'King'    : KING_B
        }
    }

def pixel_index(x1, x2, reverse=True):
    # Converts pixel position in board to index in array
    if reverse: return x2//60 - 1, x1//60 - 1

    # Converts index in array to pixel position in board
    return 60*(x2 + 1), 60*(x1 + 1)

def draw_board():
    WINDOW.fill(WHITE)
    WINDOW.blit(BOARD, (0, 0))

def draw_pieces():
    for indices, piece in np.ndenumerate(board.state):
        if piece.status == 'empty': continue
        
        WINDOW.blit(
            images[piece.color][piece.name],
            pixel_index(*indices, reverse=False)
        )

def draw_text(message, output):
    mes = FONT.render(message, True, BLUE)
    out = FONT.render(output, True, GREEN)

    WINDOW.blit(mes, (100, 600))
    WINDOW.blit(out, (100, 700))

def draw():
    draw_board()
    draw_pieces()
    draw_text('aver', 'será')
    pygame.display.update()

def main():
    
    clock = pygame.time.Clock()

    run = True
    first_click = True
    
    while run:
        clock.tick(FPS_CAP)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT: run = False

            if event.type != pygame.MOUSEBUTTONUP: continue
            
            dum = pygame.mouse.get_pos()

            if (
                (dum[0] < 60 or 540 < dum[0]) or
                (dum[1] < 60 or 540 < dum[1])
            ): continue

            if first_click:
                row, col = pixel_index(*dum)
                piece = board.state[row, col]
                
                if piece.status != 'empty': first_click = False
            else:
                target = pixel_index(*dum)
                piece.move(chess.convert(target))
                
                first_click = True


        draw()
        
    pygame.quit()

if __name__ == '__main__': main()

# %%
