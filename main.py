# %%
import chess

move_list = [
    'p E2 E4', 'p E7 E5',
    'q D1 F3', 'n G8 F6',
    'b F1 C4', 'p C7 C6',
    'n G1 H3', 'b F8 C5',
    'k E1 G1', 'q D8 E7',
    'exit'
]

def main():

    print(
        'CHESS!!! - by SankE\nFor additional help, enter "help" as a move\n'
    )
    game, board = chess.Game().new_game()
    
    run = True
    i = 0
    while run:
        # print(f'Insert a move. {chess.game.turn} plays.')
        # move_str = input('(EXAMPLE: To move a pawn from E2 to E4, type: "p E2 E4")')

        print(f'Insert a move. {game.turn} plays.')
        print('(EXAMPLE: To move a pawn from E2 to E4, type: "p E2 E4")\n')
        move_str = move_list[i]

        if move_str.lower() == 'exit': break
        
        chess.move_parser(move_str)
        i += 1

    print(game)
    input('Game finished. Press ENTER to exit.\n')

if __name__ == '__main__':
    main()

# %%
