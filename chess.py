# %%
from textwrap import wrap
import numpy as np
# from ui_game import promotion_prompt


class Board():

    state = np.empty((8, 8))

    @classmethod
    def show(cls): print(cls.state, end='\n\n')

    @classmethod
    def check(cls, pos):
        row, col = convert(pos)
        return cls.state[row, col]

    @classmethod
    def reset_board(cls, layout='default'):
        cls.xx0 = Piece('-', '-', 'X0', status='empty')

        if layout == 'default':

            cls.pW1, cls.pB1 = Piece('p', 'W', 'A2'), Piece('p', 'B', 'A7')
            cls.pW2, cls.pB2 = Piece('p', 'W', 'B2'), Piece('p', 'B', 'B7')
            cls.pW3, cls.pB3 = Piece('p', 'W', 'C2'), Piece('p', 'B', 'C7')
            cls.pW4, cls.pB4 = Piece('p', 'W', 'D2'), Piece('p', 'B', 'D7')
            cls.pW5, cls.pB5 = Piece('p', 'W', 'E2'), Piece('p', 'B', 'E7')
            cls.pW6, cls.pB6 = Piece('p', 'W', 'F2'), Piece('p', 'B', 'F7')
            cls.pW7, cls.pB7 = Piece('p', 'W', 'G2'), Piece('p', 'B', 'G7')
            cls.pW8, cls.pB8 = Piece('p', 'W', 'H2'), Piece('p', 'B', 'H7')

            cls.rW1, cls.rB1 = Piece('r', 'W', 'A1'), Piece('r', 'B', 'A8')
            cls.rW2, cls.rB2 = Piece('r', 'W', 'H1'), Piece('r', 'B', 'H8')

            cls.nW1, cls.nB1 = Piece('n', 'W', 'B1'), Piece('n', 'B', 'B8')
            cls.nW2, cls.nB2 = Piece('n', 'W', 'G1'), Piece('n', 'B', 'G8')

            cls.bW1, cls.bB1 = Piece('b', 'W', 'C1'), Piece('b', 'B', 'C8')
            cls.bW2, cls.bB2 = Piece('b', 'W', 'F1'), Piece('b', 'B', 'F8')

            cls.qW1, cls.qB1 = Piece('q', 'W', 'D1'), Piece('q', 'B', 'D8')
            cls.kW1, cls.kB1 = Piece('k', 'W', 'E1'), Piece('k', 'B', 'E8')

            cls.state = np.array([
                [cls.rB1, cls.nB1, cls.bB1, cls.qB1, cls.kB1, cls.bB2, cls.nB2, cls.rB2],
                [cls.pB1, cls.pB2, cls.pB3, cls.pB4, cls.pB5, cls.pB6, cls.pB7, cls.pB8],
                [cls.xx0]*8,
                [cls.xx0]*8,
                [cls.xx0]*8,
                [cls.xx0]*8,
                [cls.pW1, cls.pW2, cls.pW3, cls.pW4, cls.pW5, cls.pW6, cls.pW7, cls.pW8],
                [cls.rW1, cls.nW1, cls.bW1, cls.qW1, cls.kW1, cls.bW2, cls.nW2, cls.rW2]
            ], dtype=object)
        
        elif layout == 'promote':
            
            cls.pW1, cls.pB1 = Piece('p', 'W', 'X0'), Piece('p', 'B', 'A2')
            cls.pW2, cls.pB2 = Piece('p', 'W', 'B2'), Piece('p', 'B', 'B7')
            cls.pW3, cls.pB3 = Piece('p', 'W', 'C2'), Piece('p', 'B', 'C7')
            cls.pW4, cls.pB4 = Piece('p', 'W', 'D2'), Piece('p', 'B', 'D7')
            cls.pW5, cls.pB5 = Piece('p', 'W', 'E7'), Piece('p', 'B', 'X0')
            cls.pW6, cls.pB6 = Piece('p', 'W', 'F7'), Piece('p', 'B', 'X0')
            cls.pW7, cls.pB7 = Piece('p', 'W', 'G7'), Piece('p', 'B', 'X0')
            cls.pW8, cls.pB8 = Piece('p', 'W', 'H7'), Piece('p', 'B', 'X0')

            cls.rW1, cls.rB1 = Piece('r', 'W', 'X0'), Piece('r', 'B', 'A8')
            cls.rW2, cls.rB2 = Piece('r', 'W', 'H1'), Piece('r', 'B', 'X0')

            cls.nW1, cls.nB1 = Piece('n', 'W', 'B1'), Piece('n', 'B', 'B8')
            cls.nW2, cls.nB2 = Piece('n', 'W', 'G1'), Piece('n', 'B', 'X0')

            cls.bW1, cls.bB1 = Piece('b', 'W', 'C1'), Piece('b', 'B', 'C8')
            cls.bW2, cls.bB2 = Piece('b', 'W', 'F1'), Piece('b', 'B', 'X0')

            cls.qW1, cls.qB1 = Piece('q', 'W', 'D1'), Piece('q', 'B', 'D8')
            cls.kW1, cls.kB1 = Piece('k', 'W', 'E1'), Piece('k', 'B', 'A7')

            cls.state = np.array([
                [cls.rB1, cls.nB1, cls.bB1, cls.qB1, cls.xx0, cls.xx0, cls.xx0, cls.xx0],
                [cls.kB1, cls.pB2, cls.pB3, cls.pB4, cls.pW5, cls.pW6, cls.pW7, cls.pW8],
                [cls.xx0]*8,
                [cls.xx0]*8,
                [cls.xx0]*8,
                [cls.xx0]*8,
                [cls.pB1, cls.pW2, cls.pW3, cls.pW4, cls.xx0, cls.xx0, cls.xx0, cls.xx0],
                [cls.xx0, cls.nW1, cls.bW1, cls.qW1, cls.kW1, cls.bW2, cls.nW2, cls.rW2]
            ], dtype=object)

        elif layout == 'check1':
            
            cls.rW1, cls.rB1 = Piece('r', 'W', 'A1'), Piece('r', 'B', 'A8')
            cls.rW2, cls.rB2 = Piece('r', 'W', 'H3'), Piece('r', 'B', 'H1')

            cls.kW1, cls.kB1 = Piece('k', 'W', 'E1'), Piece('k', 'B', 'C2')

            cls.state = np.array([
                [cls.rB1, cls.xx0, cls.xx0, cls.xx0, cls.xx0, cls.xx0, cls.xx0, cls.xx0],
                [cls.xx0]*8,
                [cls.xx0]*8,
                [cls.xx0]*8,
                [cls.xx0]*8,
                [cls.xx0, cls.xx0, cls.xx0, cls.xx0, cls.xx0, cls.xx0, cls.xx0, cls.rW2],
                [cls.xx0, cls.xx0, cls.kB1, cls.xx0, cls.xx0, cls.xx0, cls.xx0, cls.xx0],
                [cls.rW1, cls.xx0, cls.xx0, cls.xx0, cls.kW1, cls.xx0, cls.xx0, cls.rB2]
            ], dtype=object)

        elif layout == 'empty' or layout == '' or layout is None:
            cls.state = np.array([[cls.xx0]*8]*8, dtype=object)


class Piece():
    
    positions = {
        'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7,
        '8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7
    }
    
    inverse = {key: value for value, key in list(positions.items())[:8]}

    names = {
        'p': 'Pawn'     , 'r': 'Rook'       , 'n': 'Knight',
        'b': 'Bishop'   , 'q': 'Queen'      , 'k': 'King',
        '-': 'Empty'
    }

    colors = {'W': 'White', 'B': 'Black', '-': 'None'}
    
    def __init__(self, name, color, pos, status='alive', special=None):
        self.short = name + color
        self.name = Piece.names[name]
        self.color = Piece.colors[color]
        self.pos = pos
        self.status = status
        self.special = special
    
    def __repr__(self): return str(self.short)

    def promote(self, console=True):
        if console:
            while True:
                piece_name = input('Choose a piece [r, n, b, q]:\n')
                
                if piece_name.lower() in ('r', 'n', 'b', 'q'):
                    break
                else:
                    output = 'YOU CAN\'T PROMOTE TO THAT PIECE. TRY AGAIN'
                    print(output)
        else:
            piece_name = Game.pp('White' if Game.wTurn else 'Black')
        
        self.__init__(
            piece_name, 'W' if Game.wTurn else 'B',
            self.pos, special='promoted'
        )
        Game.promotions += 1

    def move(self, place, check=False):
        turn, sign = ('White', 1) if Game.wTurn else ('Black', -1)
        output = ''
        
        _err_color      = f'WRONG PIECE. MOVE ONLY {turn.upper()} PIECES'
        _err_samepos    = 'YOU CAN\'T MOVE YOUR PIECES TO THE SAME PLACE'
        _err_invalid    = 'INVALID MOVE'
        _err_capture    = 'YOU CAN\'T CAPTURE YOUR OWN PIECES'
        _err_collision  = 'PIECES IN THE WAY'
        _err_castle     = 'CASTLING NOT POSSIBLE, CHECK CONDITIONS'
        _err_check      = 'KING IN CHECK, TRY ANOTHER MOVE'

        def validate_move(func):
            def wrapper(row_i, col_i, row_f, col_f, check=False):
                if self.color == turn:
                    if not (row_i == row_f and col_i == col_f):
                        return func(row_i, col_i, row_f, col_f, check)

                    output = _err_samepos
                    print(output)
                    return False, output
                
                output = _err_color
                print(output)
                return False, output

            return wrapper

        def check_collision(func):
            def wrapper(row_i, col_i, row_f, col_f, check=False):
                success, output = func(row_i, col_i, row_f, col_f, check)
                
                if not success: return False, output

                row_dis = row_f - row_i
                col_dis = col_f - col_i
                
                for x, y in zip(
                    [0]*(abs(col_dis) - 1) if row_dis == 0 else ran(row_dis),
                    [0]*(abs(row_dis) - 1) if col_dis == 0 else ran(col_dis)
                ):
                    if Board.state[row_i + x, col_i + y].status != 'empty':
                        break
                else: return True, output

                output = _err_collision
                print(output)
                return False, output
            
            return wrapper

        def check_capture(func):
            def wrapper(row_i, col_i, row_f, col_f, check=False):
                success, output = func(row_i, col_i, row_f, col_f, check)
                
                if not success: return False, output

                if Board.state[row_f, col_f].color != turn:
                    return True, output

                output = _err_capture
                print(output)
                return False, output
            
            return wrapper

        def commit_move(func):
            def wrapper(row_i, col_i, row_f, col_f, check=False):
                success, output = func(row_i, col_i, row_f, col_f, check)

                if not success: return False, output
                
                old_place = self.pos
                old_piece = Board.state[row_f, col_f]
                
                self.pos = place
                Board.state[row_f, col_f] = self
                Board.state[row_i, col_i] = Board.xx0
                
                if not check_mate():
                    if old_piece.status != 'empty' and not check:                
                        old_piece.pos, old_piece.status = 'X0', 'captured'
                    
                    if not check: Game.pass_turn()
                    
                    if check:
                        self.pos = old_place
                        Board.state[row_f, col_f] = old_piece
                        Board.state[row_i, col_i] = self

                    Board.show()

                    return True, output
                else:
                    self.pos = old_place
                    Board.state[row_f, col_f] = old_piece
                    Board.state[row_i, col_i] = self

                output = _err_check
                print(output)
                return False, output
            
            return wrapper

        def check_mate():
            valid_move = False
            
            king = Board.kW1 if Game.wTurn else Board.kB1
            k_row, k_col = convert(king.pos)

            horse_pos = [
                (k_row + 1, k_col + 2), (k_row + 2, k_col + 1),
                (k_row - 1, k_col + 2), (k_row - 2, k_col + 1),
                (k_row + 1, k_col - 2), (k_row + 2, k_col - 1),
                (k_row - 1, k_col - 2), (k_row - 2, k_col - 1)
            ]
            horse_iterable = []
            for row, col in horse_pos:
                if row in range(8) and col in range(8):
                    horse_iterable.append((row, col))

            iterables = [
                list(zip(range(k_row + 1, 8), [k_col]*7)),                      # Down
                list(zip(range(k_row - 1, -1, -1), [k_col]*7)),                 # Up
                list(zip([k_row]*7, range(k_col + 1, 8))),                      # Right
                list(zip([k_row]*7, range(k_col - 1, -1, -1))),                 # Left

                list(zip(range(k_row + 1, 8), range(k_col + 1, 8))),            # Down Right
                list(zip(range(k_row - 1, -1, -1), range(k_col + 1, 8))),       # Up Right
                list(zip(range(k_row + 1, 8), range(k_col - 1, -1, -1))),       # Down Left
                list(zip(range(k_row - 1, -1, -1), range(k_col - 1, -1, -1))),  # Up Left

                horse_iterable                                                  # Horse
            ]

            for iterable in iterables:
                for row, col in iterable:
                    piece = Board.state[row, col]
                    
                    if piece.status == 'empty': continue
                    if piece.color == king.color: break

                    Game.pass_turn()
                    valid_move, _ = piece.move(king.pos, check=True)
                    Game.pass_turn()

                    if valid_move: break
                
                if valid_move: break
            else:
                return False

            return True


        @commit_move
        @check_capture
        @check_collision
        @validate_move
        def pawn_move(row_i, col_i, row_f, col_f, check=False):
            flag = False
            
            if (
                (target := Board.state[row_f, col_f]).status == 'empty' and
                col_f == col_i
            ):
                if (
                    row_f + sign == row_i or
                    row_f + sign*2 == row_i and row_i in (1, 6)
                ):
                    if self.special == 'Double': self.special = None
                    if abs(row_f - row_i) == 2: self.special = 'Double'
                    if row_f in (0, 7): self.promote(console=Game.console)
                    flag = True
            elif abs(col_f - col_i) == 1 and row_f + sign == row_i:
                if target.status == 'empty':
                    if (
                        (target := Board.state[row_f + sign, col_f])
                        .special == 'Double'
                    ):
                        target.pos, target.status = 'X0', 'captured'
                        Board.state[row_f + sign, col_f] = Board.xx0
                        flag = True
                else:
                    if row_f in (0, 7): self.promote(console=Game.console)
                    flag = True

            if flag:
                if self.special == 'promoted':
                    return True, f'{self.color} Pawn promoted to {self.name}'
                return True, f'{self.color} {self.name} moved to {place}'
            
            output = _err_invalid
            print(output)
            return False, output
        
        @commit_move
        @check_capture
        @check_collision
        @validate_move
        def rook_move(row_i, col_i, row_f, col_f, check=False):
            if col_i == col_f or row_i == row_f:
                if self.special is None: self.special = 'Moved'
                return True, f'{self.color} {self.name} moved to {place}'
            
            output = _err_invalid
            print(output)
            return False, output

        @commit_move
        @check_capture
        @validate_move
        def knight_move(row_i, col_i, row_f, col_f, check=False):
            if (col_f - col_i)**2 + (row_f - row_i)**2 == 5:
                return True, f'{self.color} {self.name} moved to {place}'
            
            output = _err_invalid
            print(output)
            return False, output
        
        @commit_move
        @check_capture
        @check_collision
        @validate_move
        def bishop_move(row_i, col_i, row_f, col_f, check=False):
            if abs(col_f - col_i) == abs(row_f - row_i):
                return True, f'{self.color} {self.name} moved to {place}'
            
            output = _err_invalid
            print(output)
            return False, output
        
        @commit_move
        @check_capture
        @check_collision
        @validate_move
        def queen_move(row_i, col_i, row_f, col_f, check=False):
            if (
                (col_i == col_f or row_i == row_f) or
                abs(col_f - col_i) == abs(row_f - row_i)
            ): return True, f'{self.color} {self.name} moved to {place}'
            
            output = _err_invalid
            print(output)
            return False, output

        @commit_move
        @check_capture
        @validate_move
        def king_move(row_i, col_i, row_f, col_f, check=False):
            if abs(col_f - col_i)**2 + abs(row_f - row_i)**2 <= 2:
                if self.special is None: self.special = 'Moved'
                return True, f'{self.color} {self.name} moved to {place}'
            elif (
                self.special is None and
                row_f == row_i and abs(col_f - col_i) == 2
            ):
                if (
                    col_f > col_i and
                    (rook := Board.state[row_i, col_f + 1]).special is None
                ):
                    if (
                        Board.state[row_i, col_i + 1].status == 'empty' and
                        Board.state[row_i, col_i + 2].status == 'empty'
                    ):
                        rook.pos = convert((row_i, col_i + 1))
                        Board.state[row_i, col_i + 1] = rook
                        Board.state[row_i, col_f + 1] = Board.xx0
                        rook.special = 'Castled'
                        self.special = 'Castled'
                        return True, f'{self.color} {self.name} moved to {place}'
                elif (
                    col_f < col_i and
                    (rook := Board.state[row_i, col_f - 2]).special is None
                ):
                    if (
                        Board.state[row_i, col_i - 1].status == 'empty' and
                        Board.state[row_i, col_i - 2].status == 'empty' and
                        Board.state[row_i, col_i - 3].status == 'empty'
                    ):
                        rook.pos = convert((row_i, col_i - 1))
                        Board.state[row_i, col_i - 1] = rook
                        Board.state[row_i, col_f - 2] = Board.xx0
                        rook.special = 'Castled'
                        return True, f'{self.color} {self.name} moved to {place}'
                else :
                    output = _err_castle
                    print(output)
                    return False, output
            
            output = _err_invalid
            print(output)
            return False, output

        moves = {
            'Pawn'      : pawn_move,
            'Knight'    : knight_move,
            'Rook'      : rook_move,
            'Bishop'    : bishop_move,
            'Queen'     : queen_move,
            'King'      : king_move
        }

        pos_i = convert(self.pos)
        pos_f = convert(place)

        success, output = moves[self.name](*pos_i, *pos_f, check)

        return success, output


class Game():

    wTurn = True
    promotions = 0

    @classmethod
    def __init__(cls, console=True):
        cls.console = console

        if not console:
            from ui_game import promotion_prompt
            cls.pp = promotion_prompt
    
    @classmethod
    def new_game(cls, layout='default', console=True):
        Board.reset_board(layout)

        return Game(console), Board()

    @classmethod
    def pass_turn(cls): cls.wTurn = not cls.wTurn
    

def ran(dis):
    if dis > 0  : return range(1, dis)
    else        : return range(-1, dis, -1)

def convert(pos):
    '''
    Converts strings of the form \'A1\' to tuples
    of the form (row, col), with the letter character
    converted into column and the number into row.
    '''
    if type(pos) is str:
        return Piece.positions[pos[1]], Piece.positions[pos[0]]
    elif type(pos) is tuple:
        return Piece.inverse[pos[1]] + str(8 - pos[0])

def validate(string, Type='pos'):
    if Type == 'pos':
        if (
            len(string) == 2 and
            string[0] in list(Piece.positions)[:8] and
            string[1] in list(Piece.positions)[8:]
        ): return True
    elif Type == 'piece':
        if string in list(Piece.names)[:-1]: return True
    else:
        print('ERROR: This function only validates pieces and positions')
    
    return False

def move_parser(move_str):
    try:
        initial, pos_i, pos_f = move_str.split()
        initial, pos_i, pos_f = initial.lower(), pos_i.upper(), pos_f.upper()
    except:
        output = 'Incorrect Syntax. Please try again'
        print(output)
        return False, output
    
    if not (
        validate(initial, Type='piece') and
        validate(pos_i) and validate(pos_f)
    ):
        output = 'Non valid syntax. Try again'
        print(output)
        return False, output

    if (piece := Board.check(pos_i)).name == Piece.names[initial]:
        return piece.move(pos_f)
    else:
        output = f'ERROR: Piece in {pos_i} doesn\'t match input piece'
        print(output)
        return False, output

# %%
