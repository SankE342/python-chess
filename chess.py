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
    def __init__(self, name, color, pos, status='alive', special=None):
        self.short = name + color
        self.name = dct_names[name]
        self.color = dct_colors[color]
        self.pos = pos
        self.status = status
        self.special = special
    
    def __repr__(self): return str(self.short)

    def move(self, place):
        _err_color      = f'WRONG PIECE. MOVE ONLY {game.turn.upper()} PIECES\n'
        _err_samepos    = 'YOU CAN\'T MOVE YOUR PIECES TO THE SAME PLACE\n'
        _err_invalid    = 'INVALID MOVE\n'
        _err_capture    = 'YOU CAN\'T CAPTURE YOUR OWN PIECES\n'
        _err_collision  = 'PIECES IN THE WAY\n'
        _err_castle     = 'CASTLING NOT POSSIBLE, CHECK CONDITIONS\n'
        _err_promotion  = 'YOU CAN\'T PROMOTE TO THAT PIECE. TRY AGAIN\n'

        def commit_move(row_i, col_i, row_f, col_f):
            self.pos = place
            board.state[row_f, col_f] = self
            board.state[row_i, col_i] = xx0
            game.pass_turn()
            board.show()

        def validate_move(func):
            def wrapper(row_i, col_i, row_f, col_f):
                if self.color == game.turn:
                    if not (row_i == row_f and col_i == col_f):
                        return func(row_i, col_i, row_f, col_f)

                    print(_err_samepos)
                    return False
                
                print(_err_color)
                return False

            return wrapper

        def check_collision(func):
            def wrapper(row_i, col_i, row_f, col_f):
                if not func(row_i, col_i, row_f, col_f): return False

                row_dis = row_f - row_i
                col_dis = col_f - col_i
                
                def ran(dis):
                    if dis > 0: return range(1, dis)
                    else:       return range(-1, dis, -1)
                
                for x, y in zip(
                    (0,)*(abs(col_dis) - 1) if row_dis == 0 else ran(row_dis),
                    (0,)*(abs(row_dis) - 1) if col_dis == 0 else ran(col_dis)
                ):
                    if board.state[row_i + x, col_i + y] is not xx0: break
                else: return True

                print(_err_collision)
                return False
            
            return wrapper

        def check_capture(func):
            def wrapper(row_i, col_i, row_f, col_f):
                if not func(row_i, col_i, row_f, col_f): return False

                if (piece := board.state[row_f, col_f]).color != game.turn:
                    if piece.status != 'empty':                
                        piece.pos, piece.status = 'X0', 'captured'
                    commit_move(row_i, col_i, row_f, col_f)
                    return True
                else:
                    print(_err_capture)
                    return False
            
            return wrapper

        @check_capture
        @check_collision
        @validate_move
        def pawn_move(row_i, col_i, row_f, col_f, check=False):
            def promote():
                while True:
                    if (
                        (piece_name := input('Choose a piece [r, n, b, q]:\n')
                        .lower()) in ('r', 'n', 'b', 'q')
                    ):
                        self.__init__(
                            piece_name, game.turn[0],
                            self.pos, special='promoted'
                        )
                        game.promotions += 1
                        break
                    else:
                        print(_err_promotion)

            if (
                (target := board.state[row_f, col_f]) == xx0 and
                col_f == col_i
            ):
                if (
                    row_f + game.sign == row_i or
                    row_f + game.sign*2 == row_i and row_i in (1, 6)
                ):
                    if self.special == 'Double': self.special = None
                    if abs(row_f - row_i) == 2: self.special = 'Double'
                    if row_f in (0, 7): promote()
                    return True
            elif abs(col_f - col_i) == 1 and row_f + game.sign == row_i:
                if target.status == 'empty':
                    if (
                        (target := board.state[row_f + game.sign, col_f])
                        .special == 'Double'
                    ):
                        target.pos, target.status = 'X0', 'captured'
                        board.state[row_f + game.sign, col_f] = xx0
                        return True
                else:
                    if row_f in (0, 7): promote()
                    return True

            print(_err_invalid)
            return False
        
        @check_capture
        @check_collision
        @validate_move
        def rook_move(row_i, col_i, row_f, col_f, check=False):
            if col_i == col_f or row_i == row_f:
                if self.special is None: self.special = 'Moved'
                return True
            
            print(_err_invalid)
            return False

        @check_capture
        @validate_move
        def knight_move(row_i, col_i, row_f, col_f, check=False):
            if (col_f - col_i)**2 + (row_f - row_i)**2 == 5: return True
            
            print(_err_invalid)
            return False
        
        @check_capture
        @check_collision
        @validate_move
        def bishop_move(row_i, col_i, row_f, col_f, check=False):
            if abs(col_f - col_i) == abs(row_f - row_i): return True
            
            print(_err_invalid)
            return False
        
        @check_capture
        @check_collision
        @validate_move
        def queen_move(row_i, col_i, row_f, col_f, check=False):
            if (
                (col_i == col_f or row_i == row_f) or
                abs(col_f - col_i) == abs(row_f - row_i)
            ): return True
            
            print(_err_invalid)
            return False

        @check_capture
        @validate_move
        def king_move(row_i, col_i, row_f, col_f, check=False):
            if abs(col_f - col_i)**2 + abs(row_f - row_i)**2 <= 2:
                if self.special is None: self.special = 'Moved'
                return True
            elif (
                self.special is None and
                row_f == row_i and abs(col_f - col_i) == 2
            ):
                if (
                    col_f > col_i and
                    (rook := board.state[row_i, col_f + 1]).special is None
                ):
                    if (
                        board.state[row_i, col_i + 1] is xx0 and
                        board.state[row_i, col_i + 2] is xx0
                    ):
                        rook.pos = convert((row_i, col_i + 1))
                        board.state[row_i, col_i + 1] = rook
                        board.state[row_i, col_f + 1] = xx0
                        rook.special = 'Castled'
                        self.special = 'Castled'
                        return True
                elif (
                    col_f < col_i and
                    (rook := board.state[row_i, col_f - 2]).special is None
                ):
                    if (
                        board.state[row_i, col_i - 1] is xx0 and
                        board.state[row_i, col_i - 2] is xx0 and
                        board.state[row_i, col_i - 3] is xx0
                    ):
                        rook.pos = convert((row_i, col_i - 1))
                        board.state[row_i, col_i - 1] = rook
                        board.state[row_i, col_f - 2] = xx0
                        rook.special = 'Castled'
                        return True
                else :
                    print(_err_castle)
                    return False
            
            print(_err_invalid)
            return False

        dct_moves = {
                'Pawn'      : pawn_move,
                'Knight'    : knight_move,
                'Rook'      : rook_move,
                'Bishop'    : bishop_move,
                'Queen'     : queen_move,
                'King'      : king_move
        }

        pos_i = convert(self.pos)
        pos_f = convert(place)

        dct_moves[self.name](*pos_i, *pos_f)


class Game():
    def __init__(self):
        self.turn = 'White'
        self.sign = 1
        self.promotions = 0

    def pass_turn(self):
        if self.turn == 'White':
            self.turn = 'Black'
            self.sign = -1
        else:
            self.turn = 'White'
            self.sign = 1

# Indexers for piece information
if True:
    dct_pos = {
        'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7,
        '8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7
    }
    dct_inv = {key: value for value, key in list(dct_pos.items())[:8]}

    dct_names = {
        'p': 'Pawn'     , 'r': 'Rook'       , 'n': 'Knight',
        'b': 'Bishop'   , 'q': 'Queen'      , 'k': 'King',
        '-': 'Empty'
    }

    dct_colors = {'W': 'White', 'B': 'Black', '-': 'None'}
    

def convert(pos):
    '''
    Converts strings of the form \'A1\' to tuples
    of the form (row, col), with the letter character
    converted into column and the number into row.
    '''
    if type(pos) is str:
        return dct_pos[pos[1]], dct_pos[pos[0]]
    elif type(pos) is tuple:
        return dct_inv[pos[1]] + str(8 - pos[0])

# Initializing board and pieces
xx0 = Piece('-', '-', 'X0', status='empty')
def reset_board(layout='default'):
    if layout == 'default':

        pW1, pB1 = Piece('p', 'W', 'A2'), Piece('p', 'B', 'A7')
        pW2, pB2 = Piece('p', 'W', 'B2'), Piece('p', 'B', 'B7')
        pW3, pB3 = Piece('p', 'W', 'C2'), Piece('p', 'B', 'C7')
        pW4, pB4 = Piece('p', 'W', 'D2'), Piece('p', 'B', 'D7')
        pW5, pB5 = Piece('p', 'W', 'E2'), Piece('p', 'B', 'E7')
        pW6, pB6 = Piece('p', 'W', 'F2'), Piece('p', 'B', 'F7')
        pW7, pB7 = Piece('p', 'W', 'G2'), Piece('p', 'B', 'G7')
        pW8, pB8 = Piece('p', 'W', 'H2'), Piece('p', 'B', 'H7')

        rW1, rB1 = Piece('r', 'W', 'A1'), Piece('r', 'B', 'A8')
        rW2, rB2 = Piece('r', 'W', 'H1'), Piece('r', 'B', 'H8')

        nW1, nB1 = Piece('n', 'W', 'B1'), Piece('n', 'B', 'B8')
        nW2, nB2 = Piece('n', 'W', 'G1'), Piece('n', 'B', 'G8')

        bW1, bB1 = Piece('b', 'W', 'C1'), Piece('b', 'B', 'C8')
        bW2, bB2 = Piece('b', 'W', 'F1'), Piece('b', 'B', 'F8')

        qW1, qB1 = Piece('q', 'W', 'D1'), Piece('q', 'B', 'D8')
        kW1, kB1 = Piece('k', 'W', 'E1'), Piece('k', 'B', 'E8')

        return np.array([
            [rB1, nB1, bB1, qB1, kB1, bB2, nB2, rB2],
            [pB1, pB2, pB3, pB4, pB5, pB6, pB7, pB8],
            [xx0]*8,
            [xx0]*8,
            [xx0]*8,
            [xx0]*8,
            [pW1, pW2, pW3, pW4, pW5, pW6, pW7, pW8],
            [rW1, nW1, bW1, qW1, kW1, bW2, nW2, rW2]
        ], dtype=object)
    
    elif layout == 'promote':
        
        pW1, pB1 = Piece('p', 'W', 'X0'), Piece('p', 'B', 'A2')
        pW2, pB2 = Piece('p', 'W', 'B2'), Piece('p', 'B', 'B7')
        pW3, pB3 = Piece('p', 'W', 'C2'), Piece('p', 'B', 'C7')
        pW4, pB4 = Piece('p', 'W', 'D2'), Piece('p', 'B', 'D7')
        pW5, pB5 = Piece('p', 'W', 'E7'), Piece('p', 'B', 'X0')
        pW6, pB6 = Piece('p', 'W', 'F7'), Piece('p', 'B', 'X0')
        pW7, pB7 = Piece('p', 'W', 'G7'), Piece('p', 'B', 'X0')
        pW8, pB8 = Piece('p', 'W', 'H7'), Piece('p', 'B', 'X0')

        rW1, rB1 = Piece('r', 'W', 'X0'), Piece('r', 'B', 'A8')
        rW2, rB2 = Piece('r', 'W', 'H1'), Piece('r', 'B', 'X0')

        nW1, nB1 = Piece('n', 'W', 'B1'), Piece('n', 'B', 'B8')
        nW2, nB2 = Piece('n', 'W', 'G1'), Piece('n', 'B', 'X0')

        bW1, bB1 = Piece('b', 'W', 'C1'), Piece('b', 'B', 'C8')
        bW2, bB2 = Piece('b', 'W', 'F1'), Piece('b', 'B', 'X0')

        qW1, qB1 = Piece('q', 'W', 'D1'), Piece('q', 'B', 'D8')
        kW1, kB1 = Piece('k', 'W', 'E1'), Piece('k', 'B', 'X0')

        return np.array([
            [rB1, nB1, bB1, qB1, xx0, xx0, xx0, xx0],
            [xx0, pB2, pB3, pB4, pW5, pW6, pW7, pW8],
            [xx0]*8,
            [xx0]*8,
            [xx0]*8,
            [xx0]*8,
            [pB1, pW2, pW3, pW4, xx0, xx0, xx0, xx0],
            [xx0, nW1, bW1, qW1, kW1, bW2, nW2, rW2]
        ], dtype=object)
    
    elif layout == 'empty': return np.array([[xx0]*8]*8, dtype=object)
    
def start_game(layout='default'):
    global game
    global board

    game = Game()
    board = Board(layout)
    board.show()

def validate(string, Type='pos'):
    if Type == 'pos':
        if (
            len(string) == 2 and
            string[0] in list(dct_pos.keys())[:8] and
            string[1] in list(dct_pos.keys())[8:]
        ): return True
    elif Type == 'piece':
        if (
            len(string) == 1 and
            string in list(dct_names.keys())[:-1]
        ): return True
    else:
        print('ERROR: This function only validates pieces and positions')
    
    print(f'ERROR: {Type} not written correctly')
    return False

def move_parser(move_str):
    try:
        initial, pos_i, pos_f = move_str.split(' ')
        initial, pos_i, pos_f = initial.lower(), pos_i.upper(), pos_f.upper()
    except:
        print('Incorrect Syntax. Please try again')
        return False
    
    if not (
        validate(initial, Type='piece') and
        validate(pos_i) and validate(pos_f)
    ): return False

    if (piece := board.check(pos_i)).name == dct_names[initial]:
        piece.move(pos_f)
        return True
    else:
        print(f'ERROR: Piece in {pos_i} doesn\'t match input piece')
        return False

# %%

# pW5.move('E4')
# pB1.move('A5')

# # %%
# pW5.move('E5')
# pB4.move('D6')

# # %%

# pW5.move('D6')
# qB1.move('D6')

# # %%

# pW6.move('F4')
# qB1.move('F6')

# # %%

# pW6.move('F5')
# nB1.move('A6')

# # %%

# pW1.move('A3')
# qB1.move('E5')

# # %%
# pW1.move('A4')
# pB5.move('E6')

# # %%

# nW2.move('H3')
# bB1.move('D7')

# # %%

# bW2.move('E2')
# kB1.move('C8')

# # %%

# %%
