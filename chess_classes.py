# %%
import numpy as np


class Board():
    def __init__(self, layout='default'):
        self.layout = layout
        self.reset()

    def show(self):
        print(self.state, end='\n\n')

    def reset(self):
        self.state = reset_board(self.layout)

    def check(self, pos):
        row, col = convert(pos)
        return self.state[row, col]

class Piece():
    def __init__(self, name, color, pos, status='alive'):
        self.short = name + color
        self.name = dct_pieces[name]
        self.color = dct_colors[color]
        self.pos = pos
        self.status = status
    
    def __repr__(self):
        return str(self.short)

    def move(self, place):
        
        _err_color = f'WRONG PIECE. MOVE ONLY {game.turn.upper()} PIECES'
        _err_invalid = 'INVALID MOVE'
        _err_capture = 'YOU CAN\'T CAPTURE YOUR OWN PIECES'
        _err_collision = 'PIECES IN THE WAY'

        def commit_move(row_i, col_i, row_f, col_f):
            self.pos = place
            board.state[row_f, col_f] = self
            board.state[row_i, col_i] = xx0
            game.pass_turn()
            board.show()

        def check_collision(func):
            def wrapper(row_i, col_i, row_f, col_f):
                if not func(row_i, col_i, row_f, col_f): return

                row_dis = row_f - row_i
                col_dis = col_f - col_i
                
                def ran(dis):
                    if dis > 0: return range(1, dis)
                    else:       return range(-1, dis, -1)
                
                for x, y in zip(
                    (0,)*(col_dis - 1) if row_dis == 0 else ran(row_dis),
                    (0,)*(row_dis - 1) if col_dis == 0 else ran(col_dis)
                ):
                    if board.state[row_i + x, col_i + y] is not xx0: break
                else: return True

                print(_err_collision)
                return False
            
            return wrapper

        def check_capture(func):
            def wrapper(row_i, col_i, row_f, col_f):
                if not func(row_i, col_i, row_f, col_f): return
                
                piece = board.state[row_f, col_f]
                if piece.color != game.turn:
                    if piece.color != 'None':                
                        piece.pos, piece.status = 'X0', 'captured'
                    commit_move(row_i, col_i, row_f, col_f)
                else:
                    print(_err_capture)
            
            return wrapper

        @check_capture
        @check_collision
        def pawn_move(row_i, col_i, row_f, col_f, check=False):
            if col_f == col_i and board.state[row_f, col_f] == xx0:
                if (
                    game.turn == 'White' and 
                    (row_f + 1 == row_i or row_f + 2 == row_i and row_i == 6) or
                    game.turn == 'Black' and 
                    (row_f - 1 == row_i or row_f - 2 == row_i and row_i == 1)
                ): return True
            elif (
                abs(col_f - col_i) == 1 and
                (game.turn == 'White' and row_f + 1 == row_i or
                game.turn == 'Black' and row_f - 1 == row_i)
            ): return True
            
            print(_err_invalid)
            return False
        
        @check_capture
        @check_collision
        def rook_move(row_i, col_i, row_f, col_f, check=False):
            if col_i == col_f or row_i == row_f: return True
            
            print(_err_invalid)
            return False

        @check_capture
        def knight_move(row_i, col_i, row_f, col_f, check=False):
            if (col_f - col_i)**2 + (row_f - row_i)**2 == 5: return True
            
            print(_err_invalid)
            return False
        
        @check_capture
        @check_collision
        def bishop_move(row_i, col_i, row_f, col_f, check=False):
            if abs(col_f - col_i) == abs(row_f - row_i): return True
            
            print(_err_invalid)
            return False
        
        @check_capture
        @check_collision
        def queen_move(row_i, col_i, row_f, col_f, check=False):
            if (
                (col_i == col_f or row_i == row_f) or
                abs(col_f - col_i) == abs(row_f - row_i)
            ): return True
            
            print(_err_invalid)
            return False

        @check_capture
        def king_move(row_i, col_i, row_f, col_f, check=False):
            if abs(col_f - col_i) + abs(row_f - row_i) <= 2: return True
            
            print(_err_invalid)
            return False


        if self.color == game.turn:
            pos_i = convert(self.pos)
            pos_f = convert(place)
            
            if      self.name == 'Pawn':    pawn_move(*pos_i, *pos_f)
            elif    self.name == 'Knight':  knight_move(*pos_i, *pos_f)
            elif    self.name == 'Rook':    rook_move(*pos_i, *pos_f)
            elif    self.name == 'Bishop':  bishop_move(*pos_i, *pos_f)
            elif    self.name == 'Queen':   queen_move(*pos_i, *pos_f)
            elif    self.name == 'King':    king_move(*pos_i, *pos_f)

        else: print(_err_color)

class Game():
    def __init__(self):
        self.turn = 'White'

    def pass_turn(self):
        if self.turn == 'White': self.turn = 'Black'
        else: self.turn = 'White'

# Indexers for piece information
if True:
    dctPos = {
        'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7,
        '8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7
    }
    dctInv = {key: value for value, key in list(dctPos.items())[:8]}

    dct_pieces = {
        'p': 'Pawn'     , 'r': 'Rook'       , 'n': 'Knight',
        'b': 'Bishop'   , 'q': 'Queen'      , 'k': 'King',
        '-': 'Empty'
    }

    dct_colors = {'W': 'White', 'B': 'Black', '-': 'None'}
    
# Initializing pieces
if True:
    xx0 = Piece('-', '-', 'X0', status='empty')

    pW1 = Piece('p', 'W', 'A2')
    pW2 = Piece('p', 'W', 'B2')
    pW3 = Piece('p', 'W', 'C2')
    pW4 = Piece('p', 'W', 'D2')
    pW5 = Piece('p', 'W', 'E2')
    pW6 = Piece('p', 'W', 'F2')
    pW7 = Piece('p', 'W', 'G2')
    pW8 = Piece('p', 'W', 'H2')

    pB1 = Piece('p', 'B', 'A7')
    pB2 = Piece('p', 'B', 'B7')
    pB3 = Piece('p', 'B', 'C7')
    pB4 = Piece('p', 'B', 'D7')
    pB5 = Piece('p', 'B', 'E7')
    pB6 = Piece('p', 'B', 'F7')
    pB7 = Piece('p', 'B', 'G7')
    pB8 = Piece('p', 'B', 'H7')


    rW1 = Piece('r', 'W', 'A1')
    rW2 = Piece('r', 'W', 'H1')

    rB1 = Piece('r', 'B', 'A8')
    rB2 = Piece('r', 'B', 'H8')


    nW1 = Piece('n', 'W', 'B1')
    nW2 = Piece('n', 'W', 'G1')

    nB1 = Piece('n', 'B', 'B8')
    nB2 = Piece('n', 'B', 'G8')
        
        
    bW1 = Piece('b', 'W', 'C1')
    bW2 = Piece('b', 'W', 'F1')

    bB1 = Piece('b', 'B', 'C8')
    bB2 = Piece('b', 'B', 'F8')


    qW1 = Piece('q', 'W', 'D1')

    qB1 = Piece('q', 'B', 'D8')


    kW1 = Piece('k', 'W', 'E1')

    kB1 = Piece('k', 'B', 'E8')

def convert(pos):
    '''
    Converts strings of the form \'A1\' to tuples
    of the form (row, col), with the letter character
    converted into column and the number into row.
    '''
    if type(pos) is str:
        return dctPos[pos[1]], dctPos[pos[0]]
    elif type(pos) is tuple:
        return dctInv[pos[1]] + str(8 - pos[0])

def reset_board(layout='default'):
    if layout == 'default':
        return np.array([
        [rB1, nB1, bB1, qB1, kB1, bB2, nB2, rB2],
        [pB1, pB2, pB3, pB4, pB5, pB6, pB7, pB8],
        [xx0]*8,
        [xx0]*8,
        [xx0]*8,
        [xx0]*8,
        [pW1, pW2, pW3, pW4, pW5, pW6, pW7, pW8],
        [rW1, nW1, bW1, qW1, kW1, bW2, nW2, rW2],
    ], dtype=object)
    
    if layout == 'empty': return np.array([['--']*8]*8, dtype=object)
    
# %%

game = Game()
board = Board()
board.show()

# %%
