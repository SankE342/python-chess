board = [
    ['Br', 'Bn', 'Bb', 'Bq', 'Bk', 'Bb', 'Bn', 'Br'],
    ['Bp', 'Bp', 'Bp', 'Bp', 'Bp', 'Bp', 'Bp', 'Bp'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp'],
    ['Wr', 'Wn', 'Wb', 'Wq', 'Wk', 'Wb', 'Wn', 'Wr']
]

turn = 'W'

def resetGame():
    yn = input('Are you sure you want to reset the game? (Y/N):  ')
    if (yn == 'Y'):
        board = [
            ['Br', 'Bn', 'Bb', 'Bq', 'Bk', 'Bb', 'Bn', 'Br'],
            ['Bp', 'Bp', 'Bp', 'Bp', 'Bp', 'Bp', 'Bp', 'Bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp'],
            ['Wr', 'Wn', 'Wb', 'Wq', 'Wk', 'Wb', 'Wn', 'Wr']
        ]
        turn = 'W'
        print('Board reseted succesfully')
    else:
        print('Board not reseted, game will continue')


def showBoard():
    print()

dctPos = {
          'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7,
          '8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7
          }

dctPie = {'p': 'Pawn', 'r': 'Rook', 'n': 'Knight', 'b': 'Bishop', 'q': 'Queen', 'k': 'King'}

def position(parP):
    row = dctPos[str(parP[1])]
    col = dctPos[str(parP[0])]
    
    return  [row, col]

def checkPiece(parP):
    posP = position(parP)
    piece = board[posP[0]][posP[1]]
    
    return piece

def moveType():
    print()


def movePiece(parI, parF):
    posI = position(parI)
    posF = position(parF)

    print(board[posI[0]][posI[1]])
    print(board[posF[0]][posF[1]])

    def pawn():
        print()
