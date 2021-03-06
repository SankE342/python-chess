# %%

from lib2to3.pytree import convert
import pygame


pygame.init()
pygame.display.set_caption('Python Chess -by SankE')

DIMENSIONS = WIDTH, HEIGHT = 600, 800
ORIGIN = X0, Y0 = 60, 60

WINDOW = pygame.display.set_mode(DIMENSIONS)

BLACK   = 0, 0, 0
GRAY    = 128, 128, 128
RED     = 255, 0, 0
GREEN   = 0, 255, 0
BLUE    = 0, 0, 255
YELLOW  = 255, 255, 0
WHITE   = 255, 255, 255

FONT_SIZE = 32
FONT_TYPE = 'Cascadia Code'
FONT = pygame.font.SysFont(FONT_TYPE, FONT_SIZE)

FPS_CAP = 30

DIR = './assets/'

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

IMAGES = {
    'White': {
        'Pawn'  : PAWN_W    , 'Rook'    : ROOK_W    , 'Knight'  : KNIGHT_W,
        'Bishop': BISHOP_W  , 'Queen'   : QUEEN_W   , 'King'    : KING_W
    },
    'Black': {
        'Pawn'  : PAWN_B    , 'Rook'    : ROOK_B    , 'Knight'  : KNIGHT_B,
        'Bishop': BISHOP_B  , 'Queen'   : QUEEN_B   , 'King'    : KING_B
    }
}


def promotion_prompt(color):
    WINDOW.blit(IMAGES[color]['Queen']  , (180, 0))
    WINDOW.blit(IMAGES[color]['Rook']   , (240, 0))
    WINDOW.blit(IMAGES[color]['Bishop'] , (300, 0))
    WINDOW.blit(IMAGES[color]['Knight'] , (360, 0))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()

            if event.type != pygame.MOUSEBUTTONUP: continue
            
            dum = pygame.mouse.get_pos()

            if (
                (dum[0] < 180 or 420 < dum[0]) or
                (dum[1] < 0 or 60 < dum[1])
            ): continue

            if dum[0] <= 240: return 'q'
            if dum[0] <= 300: return 'r'
            if dum[0] <= 360: return 'b'
            if dum[0] <= 420: return 'n'

def pix_to_idx(x1, x2, reverse=False):
    # Converts index in array to pixel position in board
    if reverse: return 60*(x2 + 1), 60*(x1 + 1)

    # Converts pixel position in board to index in array
    return x2//60 - 1, x1//60 - 1

def main():
    
    import chess    
    from numpy import ndenumerate


    game, board = chess.Game().new_game(console=False)
    # game, board = chess.Game().new_game(console=False, layout='promote')
    clock = pygame.time.Clock()


    def draw_board():
        WINDOW.fill(GRAY)
        WINDOW.blit(BOARD, (0, 0))
    
    def draw_highlights(pos, check=False):
        if pos:
            color = BLUE if game.wTurn else RED
            pygame.draw.rect(WINDOW, color, pygame.Rect(*pos, 60, 60))

        if check:
            king = board.kW1 if game.wTurn else board.kB1
            king_pos = pix_to_idx(*chess.convert(king.pos), reverse=True)

            pygame.draw.rect(WINDOW, YELLOW, pygame.Rect(*king_pos, 60, 60))

    def draw_pieces():
        for indices, piece in ndenumerate(board.state):
            if piece.status == 'empty': continue
            
            WINDOW.blit(
                IMAGES[piece.color][piece.name],
                pix_to_idx(*indices, reverse=True)
            )

    def draw_multilines(text, x=0, y=0, font_size=FONT_SIZE, color=BLACK):
        lines = text.split('\n')
        for i, line in enumerate(lines):
            t = FONT.render(line, True, color)
            WINDOW.blit(t, (x, y + font_size*i))

    def draw_text(message, output):
        draw_multilines(message, *(30, 600), color=GREEN)
        draw_multilines(output, *(30, 700), color=BLUE)

    def draw(message, output, hl_pos=None, check=False):
        draw_board()
        draw_highlights(hl_pos, check)
        draw_pieces()
        draw_text(message, output)
        pygame.display.update()


    turn = "White" if game.wTurn else "Black"
    message = f'Make a move. {turn} plays.'
    output = ':D'
    hl_pos = None
    check = False


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
                row, col = pix_to_idx(*dum)
                piece = board.state[row, col]
                
                hl_pos = pix_to_idx(row, col, reverse=True)
                if piece.status != 'empty': first_click = False
                
            else:
                target = pix_to_idx(*dum)
                success, output = piece.move(chess.convert(target))
                turn = "White" if game.wTurn else "Black"
                message = f'Make a move. {turn} plays.'

                hl_pos = None
                first_click = True
                if 'NOW IN CHECK' in output: check = True
                else: check = False

        draw(message, output, hl_pos, check)
        
    pygame.quit()

if __name__ == '__main__': main()

# %%
