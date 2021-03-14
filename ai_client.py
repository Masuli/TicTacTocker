import socket
import sys
import os
import time

BOARD_WIDTH = 3
BOARD_HEIGHT = 3
role = 'x'
board = []
client_id = ""
delta = 0.0

def initialize_board():
    for _ in range(BOARD_WIDTH * BOARD_HEIGHT):
        board.append(" ")

def get_board_value(x, y):
    return board[x + BOARD_WIDTH * y]    

def set_board_value(x, y, value):
    board[x + BOARD_WIDTH * y] = value

def render_board():
    return
    os.system("clear")
    print(" X 0 1 2")
    print("Y -------")
    for y in range(BOARD_HEIGHT):
        print("{} |{}|{}|{}|".format(y, get_board_value(0, y), get_board_value(1, y), get_board_value(2, y)))
        print("  -------")

def get_ai_move():
    for y in range(0, BOARD_HEIGHT):
        for x in range(0, BOARD_WIDTH):
            if get_board_value(x, y) == " ":
                return (x, y) 

def handle_packet(sock, packet_data):
    data = packet_data.split(",")
    if data[0] == "Stats":
        if data[1] == "w":
            print("{} You Won :) Your stats: Wins: {}, Losses: {}, Ties: {}".format(client_id, data[2], data[3], data[4]))
        elif data[1] == "l":
            print("{} You Lost :( Your stats: Wins: {}, Losses: {}, Ties: {}".format(client_id, data[2], data[3], data[4]))
        elif data[1] == "t":
            print("{} Tie! Your stats: Wins: {}, Losses: {}, Ties: {}".format(client_id, data[2], data[3], data[4]))
        global delta
        while True:
            try:
                stats = open("latency.txt", "a")
                stats.write("{}\n".format(delta))
                stats.close()
                break
            except:
                pass
        sock.close()
        sys.exit()
    elif data[0] == "Move":
        if role == 'x':
            set_board_value(int(data[1]), int(data[2]), 'o')
        else:
            set_board_value(int(data[1]), int(data[2]), 'x')
        render_board()
    elif data[0] == "Turn":
        while True:
            try:
                (x, y) = get_ai_move()
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
    start_time = time.time()
    recv_data = sock.recv(256)
    delta_time = time.time() - start_time
    global delta
    if delta_time > delta:
        delta = delta_time
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
            return

def wait_for_game(sock):
    #print("Waiting for opponent...")
    global role
    while True:
        recv_data = sock.recv(7)
        whole_packets = recv_data.decode().split("\n")
        for whole_packet in whole_packets:
            data = whole_packet.split(",")
            if data[0] == "Role":
                role = data[1]
                return
            if data[0] == "Fail":
                print("Incorrect Password!")
                sys.exit()

def run_tick_tack_tocker(args):
    
    server_address = ("localhost", 1999)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    global client_id
    client_id = args
    if len(client_id) >= 1 and len(client_id) >= 1:
        try:
            sock.connect(server_address)
            print("Login,{},{}".format(client_id, client_id))
            sock.sendall("Login,{},{}".format(client_id, client_id).encode())
            wait_for_game(sock)
            run_game_logic(sock)
            print("{} Exit successfully.".format(client_id))
        except Exception as e: 
            print("Failed to connect to server. {}".format(e))
        sock.close()

if __name__ == "__main__":
    run_tick_tack_tocker(sys.argv[1])
