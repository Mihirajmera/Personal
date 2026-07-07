from os import system
import random

board = [' '] * 9

def print_board():
    system("cls" if __name__ == "__main__" else "clear")
    for i in range(3):
        print(board[i*3] + "|" + board[i*3+1] + "|" + board[i*3+2])
        if i != 2:
            print("-+-+-")

def check_winner(player):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]

    for win in wins:
        if board[win[0]] == board[win[1]] == board[win[2]] == player:
            return True
    return False

def draw():
    return ' ' not in board

def computer_move():
    available = []

    for i in range(9):
        if board[i] == ' ':
            available.append(i)

    return random.choice(available)

while True:

    # Player move
    print_board()

    while True:
        move = int(input("Enter position (1-9): ")) - 1

        if 0 <= move <= 8 and board[move] == ' ':
            break

        print("Invalid move!")

    board[move] = 'X'

    if check_winner('X'):
        print_board()
        print("You Win!")
        break

    if draw():
        print_board()
        print("Draw!")
        break

    # Computer move
    ai = computer_move()
    board[ai] = 'O'

    if check_winner('O'):
        print_board()
        print("Computer Wins!")
        break

    if draw():
        print_board()
        print("Draw!")
        break
