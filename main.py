# %%
import chess

def main():

    print(
    '''
    CHESS!!! - by SankE
    For additional help, enter "help" as a move
    '''
    )
    chess.start_game()
    
    run = True
    while run:
        move_str = input(
        f'''
        Insert a move. {chess.game.turn} plays.
        (EXAMPLE: To move a pawn from E2 to E4, type: "p E2 E4")
        '''
        )
        if move_str.lower() == 'exit': break
        chess.move_parser(move_str)

    print(
    '''
    Game finished. Press ENTER to exit.
    '''
    )

if __name__ == '__main__':
    main()