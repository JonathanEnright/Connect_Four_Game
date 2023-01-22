import pandas as pd


def create_game():
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']]
    df = pd.DataFrame(board)
    df.index.name = 'Rows'
    df.rename_axis('Columns', axis=1)
    return df


def choose_token(game_over, skip = False):
    while game_over == False:
        if skip == False:
            print("""
    *************************************************************************************************
    Welcome to Jono's connect 4 game
    Player 1 will go first, and have the token of 'O'.
    Player 2 will go second, and have the token of 'X'.
    The aim of the game is to get 4 tokens in any which direction (vertical, horizontal, or diagonal).
    Good luck and have fun!
    *************************************************************************************************
    """)
        token = 'O'
        return token


def player_names(game_over, skip = False):
    while game_over == False:
        if skip == False:
            first_player = input("\nPlayer 1, please enter your name: ")
            print(f"Welcome {first_player}, you will play first and have the token 'O'! ")
            second_player = input("\nPlayer 2, please enter your name: ")
            print(f"Welcome {second_player}, you will play second and have the token 'X'! ")
            names = {'O': first_player, 'X': second_player}
        else:
            names = {'O': 'First_player', 'X': 'Second_player'}
        return names


def check_valid_turn(token, df, names):
    print(df)
    current_player = names[token]
    print(f"\n{current_player}, its your turn!")
    turn = input("Which column [0-7] would you like to place your token?: ")
    if turn not in str(list(range(8))):
        print("Sorry, not a valid entry")
        return check_valid_turn(token, df, names)
    elif turn == '':
        print("Sorry, not a valid entry")
        return check_valid_turn(token, df, names)
    else:
        turn = int(turn)
    last_available_row = df[df[turn] == '.'].shape[0]
    if last_available_row == 0:
        print("Sorry, this column is full, please try another")
        return check_valid_turn(token, df, names)
    else:
        df[turn][last_available_row - 1] = token
    return 'playing_on'


# Win vertical
def win_vertical(token, df, result):
    for row in df:
        counter = 0
        win_list = []
        for col in df:
            if token == df[row][col]:
                counter = counter + 1
                win_list.append([col, row])
                if counter == 4:
                    result = f"win - vertical with [rows,columns]'s of:\n\t\t{win_list}"
            else:
                counter = 0
                win_list = []
    return result


# Win Horizontal
def win_horizontal(token, df, result):
    counter = 0
    win_list = []
    for row in df:
        for col in df:
            if token == df[col][row]:
                counter = counter + 1
                win_list.append([row, col])
                if counter == 4:
                    result = f"win - horizontal with [rows,columns]'s of:\n\t\t{win_list}"
                    break
            else:
                counter = 0
                win_list = []
    return result


# NE to SW diagonal
def win_diagonal_nesw(token, df, result):
    """
    Create a list of winning diagonals starting in NE corner moving to SW corner.
    Diagonal winning options increase until list gets 8 options in size, then decreases.
    We have started on the diagonal prior to the first possible winning option already (x)
    """
    x = [[2, 0], [1, 1], [0, 2]]
    for i in range(9):
        counter = 0
        win_list = []
        if i < 5:
            z = [[x[0] + 1, x[1]] for x in x]
            z.append([z[0][1], z[0][0]])
            x = z
        elif i < 9:
            z.remove(z[-1])
            z = [[x[0], x[1] + 1] for x in x]
            x = z
        for win_diagonals in x:
            if token == df.iloc[win_diagonals[0], win_diagonals[1]]:
                counter = counter + 1
                win_list.append([win_diagonals[0], win_diagonals[1]])
                if counter == 4:
                    result = f"win - diagonal (NE-SW) with [rows,columns]'s of:\n\t\t{win_list}"
            else:
                counter = 0
                win_list = []
    return result


# NW to SE diagonal
def win_diagonal_nwse(token, df, result):
    """
    Create a list of winning diagonals starting in NW corner moving to SE corner.
    Diagonal winning options increase until list gets 8 options in size, then decreases.
    We have started on the diagonal prior to the first possible winning option already (x)
    """
    x = [[5, 0], [6, 1], [7, 2]]
    for i in range(9):
        counter = 0
        win_list = []
        if i < 5:
            z = [[x[0] - 1, x[1]] for x in x]
            z.append([z[-1][0] + 1, z[-1][1] + 1])
            x = z
        elif i < 9:
            z.remove(z[-1])
            z = [[x[0], x[1] + 1] for x in x]
            x = z
        for win_diagonals in x:
            if token == df.iloc[win_diagonals[0], win_diagonals[1]]:
                counter = counter + 1
                win_list.append([win_diagonals[0], win_diagonals[1]])
                if counter == 4:
                    result = f"win - diagonal (NW-SE) with [rows,columns]'s of:\n\t\t{win_list}"
            else:
                counter = 0
                win_list = []
    return result


def check_win_conditions(token, df, result):
    result = win_vertical(token, df, result)
    result = win_horizontal(token, df, result)
    result = win_diagonal_nwse(token, df, result)
    result = win_diagonal_nesw(token, df, result)
    return result


def check_game_over(win, df, token, names):
    screen = 'continue'
    current_player = names[token]
    if win.startswith('win'):
        print(df)
        print(f'''*****\n\t Congrats {current_player} has won {win[4:]}\n*****''')
        screen = 'game_over'
    elif '.' not in df.values:
        print(df)
        print('''*****\n No more moves left, its a draw!\n*****''')
        screen = 'game_over'
    return screen


def next_turn(token):
    if token == 'O':
        token = 'X'
    else:
        token = 'O'
    return token


def end_game(game_over = False):
    play_again = input("Game is now over. Do you wish to play again? Y/N: ")
    if play_again.upper().strip() in ['Y', 'YES']:
        game_over = False
    elif play_again == '':
        print("Invalid entry, please choose Y or N. ")
        return end_game()
    elif play_again.upper().strip() not in ['N', 'NO']:
        print("Invalid entry, please choose Y or N. ")
        return end_game()
    else:
        print("Thank you for playing, goodbye!")
        game_over = True
    return game_over


def main(game_over = False, skip = False):
    df = create_game()
    token = choose_token(game_over,skip)
    names = player_names(game_over,skip)
    while game_over == False:
        player_turn = check_valid_turn(token, df, names)
        win = check_win_conditions(token, df, player_turn)
        result = check_game_over(win, df, token, names)
        token = next_turn(token)
        skip = True
        if result != 'continue':
            is_game_over = end_game()
            main(is_game_over, skip = True)
            break


main()