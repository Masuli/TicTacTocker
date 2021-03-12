import socket
import sys
import random
import os

GAME_MATCHING_PORT = 1999
available_ports = [i for i in range(2000, 3000)]

def start_game_matching():
    available_players = []
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("localhost", GAME_MATCHING_PORT)
    sock.bind(server_address)
    sock.listen(1)
    
    while True:
        print("GAME_MATCHING: Listening for connections...")
        connection, client_address = sock.accept()
        data = connection.recv(256).decode()
        credentials = data.split(",")[1:]
        if not os.path.isfile("credentials.txt"):
            open("credentials.txt", "w").close()
            
        with open("credentials.txt", "r+") as file:
            lines = [line.rstrip() for line in file]
            if ",".join(credentials) in lines:
                print("GAME_MATCHING: User exists.")
            else:
                print("GAME_MATCHING: User does not exist. Creating new user...")
                file.write(",".join(credentials) + "\n")
                    
        connection.sendall("GAME_MATCHING: You are now being matched against another player.\n".encode())
        available_players.append(connection)
        if len(available_players) >= 2:
            print("GAME_MATCHING: 2 players found")
            create_game_instance("localhost", available_players[0], available_players[1], available_ports.pop(0))
            #del available_players[:2]
            print("GAME_MATCHING: 2 players deleted")
            
def create_game_instance(address, player_1, player_2, port):
    game_board = [[" "," "," "], [" "," "," "], [" "," "," "]]
    player_1_role = random.randint(1,2)
    if player_1_role == 1:
        player_1_role = "x"
        player_1.sendall(("Role,{}\n".format(player_1_role)).encode())
        player_2_role = "o"
        player_2.sendall(("Role,{}\n".format(player_2_role)).encode())
    else:
        player_1_role = "o"
        player_1.sendall(("Role,{}\n".format(player_1_role)).encode())
        player_2_role = "x"
        player_2.sendall(("Role,{}\n".format(player_2_role)).encode())
    
    print("GAME_INSTANCE: player 1 is {} and player 2 is {}".format(player_1_role, player_2_role))    
    
    if player_1_role == "x":
        while True:
            game_board, x, y = player_1_turn(player_1, game_board, player_1_role)
            if x and y:
                player_1.sendall(("Move,{},{}\n".format(x,y)).encode())
            game_board, x, y = player_2_turn(player_2, game_board, player_2_role)
            if x and y:
                player_2.sendall(("Move,{},{}\n".format(x,y)).encode())
    else:
        while True:
            game_board, x, y = player_2_turn(player_2, game_board, player_2_role)
            if x and y:
                player_2.sendall(("Move,{},{}\n".format(x,y)).encode())
            game_board, x, y = player_1_turn(player_1, game_board, player_1_role)
            if x and y:
                player_1.sendall(("Move,{},{}\n".format(x,y)).encode())

def player_1_turn(player_1, game_board, player_1_role):
    #player_1.sendall("GAME_INSTANCE: Your turn. Make a move.".encode())
    player_1.sendall("Turn,Make a move.\n".encode())
    player_1_data = player_1.recv(64).decode()
    player_1_input = player_1_data.split(",")
    if "Move" in player_1_input:
        game_board[player_1_input[1]][player_1_input[0]] = player_1_role
        check_board_state(game_board, player_1_role)
        return game_board
    else:
        print("GAME_INSTANCE: No 'Move' in data. No move was made. (P1)")
        return game_board
            
def player_2_turn(player_2, game_board, player_2_role):
    #player_2.sendall("GAME_INSTANCE: Your turn. Make a move.".encode())
    player_2.sendall("Turn,Make a move.\n".encode())
    player_2_data = player_2.recv(64).decode()
    player_2_input = player_2_data.split(",")
    if "Move" in player_2_input:
        game_board[player_2_input[1]][player_2_input[0]] = player_2_role
        check_board_state(game_board, player_2_role)
        return game_board, player_2_input[0], player_2_input[1]
    else:
        print("GAME_INSTANCE: No 'Move' in data. No move was made. (P2)")
        return game_board, False, False

def check_board_state(game_board, role):
    for i in range(3):
        horizontal_check = all(space == role for space in game_board[i])
        vertical_check = all(space == role for space in [game_board[j][i] for j in range(3)])
        if vertical_check or horizontal_check:
            win_game(game_board)
            
    diagonal_check = all(space == role for space in [game_board[i][i] for i in range(3)])
    opposite_diagonal_check = all(space == role for space in [game_board[2-i][0+i] for i in range(3)])
    if diagonal_check or opposite_diagonal_check:
        win_game(game_board)
        
def win_game(game_board):
    print("GAME_INSTANCE: GAME WON")
    for i in range(3):
        print(game_board[i])
    
if __name__ == "__main__":
    start_game_matching()
    