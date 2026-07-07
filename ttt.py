from os import system

board = [' '] * 9

def print_board():
    system("cls" if __name__ == "__main__" else "clear")
    for i in range(3):
        print(board[i*3] + "|" + board[i*3+1] + "|" + board[i*3+2])
        if i != 2:
            print("-+-+-")


def check_winner(player):
    winning_combinations = [
        [0,1,2], [3,4,5], [6,7,8],   # Rows
        [0,3,6], [1,4,7], [2,5,8],   # Columns
        [0,4,8], [2,4,6]             # Diagonals
    ]

    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True
    return False


def is_draw():
    return ' ' not in board


isXTurn = True

while True:
    print_board()

    if isXTurn:
        player = "X"
    else:
        player = "O"

    try:
        move = int(input(f"Player {player}, enter position (1-9): ")) - 1

        if move < 0 or move > 8:
            print("Invalid position!")
            input("Press Enter...")
            continue

        if board[move] != ' ':
            print("Position already taken!")
            input("Press Enter...")
            continue

        board[move] = player

        if check_winner(player):
            print_board()
            print(f"Player {player} wins!")
            break

        if is_draw():
            print_board()
            print("It's a draw!")
            break

        isXTurn = not isXTurn

    except ValueError:
        print("Please enter a number from 1 to 9.")
        input("Press Enter...")
