import socket
import sys
import os

BOARD_WIDTH = 3
BOARD_HEIGHT = 3
role = 'x'
board = []

def initialize_board():
    for _ in range(BOARD_WIDTH * BOARD_HEIGHT):
        board.append(" ")

def get_board_value(x, y):
    return board[x + BOARD_WIDTH * y]    

def set_board_value(x, y, value):
    board[x + BOARD_WIDTH * y] = value

def render_board():
    os.system("clear")
    print(" X 0 1 2")
    print("Y -------")
    for y in range(BOARD_HEIGHT):
        print("{} |{}|{}|{}|".format(y, get_board_value(0, y), get_board_value(1, y), get_board_value(2, y)))
        print("  -------")

def handle_packet(sock, packet_data):
    data = packet_data.split(",")
    if data[0] == "Stats":
        if data[1] == "w":
            print("You Won :) Your stats: Wins: {}, Losses: {}, Ties: {}".format(data[2], data[3], data[4]))
        elif data[1] == "l":
            print("You Lost :( Your stats: Wins: {}, Losses: {}, Ties: {}".format(data[2], data[3], data[4]))
        elif data[1] == "t":
            print("Tie! Your stats: Wins: {}, Losses: {}, Ties: {}".format(data[2], data[3], data[4]))
        input("Press Enter to continue...")
        return
    elif data[0] == "Move":
        if role == 'x':
            set_board_value(int(data[1]), int(data[2]), 'o')
        else:
            set_board_value(int(data[1]), int(data[2]), 'x')
        render_board()
    elif data[0] == "Turn":
        while True:
            try:
                x = int(input("Move to x: "))
                y = int(input("Move to y: "))
                if x >= 3 or y >= 3 or x < 0 or y < 0 or  get_board_value(x, y) != " ":
                    raise ValueError("")
                else:
                    break
            except ValueError:
                print("Invalid Position or entered value!")
        set_board_value(x, y, role)
        render_board()
        sock.sendall("Move,{},{}".format(x, y).encode())

def recv_and_handle_packets(sock):
    recv_data = sock.recv(256)
    whole_packets = recv_data.decode().split("\n")
    for whole_packet in whole_packets:
        handle_packet(sock, whole_packet)

def run_game_logic(sock):
    initialize_board()
    render_board()
    while True:
        try:
            recv_and_handle_packets(sock)
        except Exception as e:
            print("Fatal error {}".format(e))
            input("Press Enter to continue...")
            return

def wait_for_game(sock):
    print("Waiting for opponent...")
    global role
    while True:
        recv_data = sock.recv(256)
        whole_packets = recv_data.decode().split("\n")
        for whole_packet in whole_packets:
            data = whole_packet.split(",")
            if data[0] == "Role":
                role = data[1]
                return
            if data[0] == "Fail":
                print("Incorrect Password!")
                input("Press Enter to continue...")
                sys.exit()

def run_tick_tack_tocker():
    server_address = ('localhost', 1999)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    if len(username) >= 1 and len(password) >= 1:
        try:
            sock.connect(server_address)
            sock.sendall("Login,{},{}".format(username, password).encode())
            wait_for_game(sock)
            run_game_logic(sock)
        except: 
            print("Failed to connect to server.")
            input("Press Enter to continue...")
        sock.close()

if __name__ == "__main__":
    run_tick_tack_tocker()