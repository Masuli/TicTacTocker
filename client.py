import socket
import sys
import os

BOARD_WIDTH = 3
BOARD_HEIGHT = 3

def initialize_board(board):
    for _ in range(BOARD_WIDTH * BOARD_HEIGHT):
        board.append(" ")

def get_board_value(board, x, y):
    return board[x + BOARD_WIDTH * y]    

def set_board_value(board, x, y, value):
    board[x + BOARD_WIDTH * y] = value

def render_board(board):
    os.system("clear")
    print(" X 0 1 2")
    print("Y -------")
    for y in range(BOARD_HEIGHT):
        print("{} |{}|{}|{}|".format(y, get_board_value(board, 0, y), get_board_value(board, 1, y), get_board_value(board, 2, y)))
        print("  -------")

def run_game_logic(sock):
    role = 'X'
    board = []
    initialize_board(board)
    render_board(board)
    try:
        recv_data = sock.recv(256)
        data = recv_data.split(",")
        if data[0] == "Role":
            role = data[1]
        elif data[0] == "Stats":
            if data[1] == "W":
                print("You Won :) Your stats: Wins: {}, Losses: {}")
            else:
                print("You Lost :( Your stats: Wins: {}, Losses: {}")
            input("Press Enter to continue...")
            return
        elif data[0] == "Move":
            if role == 'X':
                set_board_value(board, int(data[1]), int(data[2]), 'O')
            else:
                set_board_value(board, int(data[1]), int(data[2]), 'X')
            render_board(board)
        elif data[0] == "Turn":
            try:
                x = int(input("Move to X: "))
                y = int(input("Move to Y: "))
                if x >= 3 or y >= 3 or x < 0 or y < 0 or  get_board_value(board, x, y) != " ":
                    raise ValueError("")
            except ValueError:
                print("Invalid Position or entered value!")

            if x < 3 and y < 3 and x >= 0 and y >= 0 and get_board_value(board, x, y) == " ":
                set_board_value(board, x, y, role)
            else:
                print("Invalid Board Position!!")
    except:
        pass

def run_tick_tack_tocker():
    server_address = ('localhost', 1999)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    if len(username) > 1 and len(password) > 1:
        try:
            sock.connect(server_address)
            message = 'Login,{},{}'.format(username, password)
            sock.sendall(message)
            sock.recv(256)
            run_game_logic(sock)
        except: 
            print("Failed to connect to server.")
            input("Press Enter to continue...")
        sock.close()

if __name__ == "__main__":
    run_tick_tack_tocker()