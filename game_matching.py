import socket
import sys
import random
import os

GAME_MATCHING_PORT = 1999
GAME_STATS_PORT = 1998
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
        credentials = connection.recv(256).decode().split(",")[1:]
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
        available_players.append((connection, credentials[0]))
        if len(available_players) >= 2:
            print("GAME_MATCHING: 2 players found")
            create_game_instance("localhost", available_players[0], available_players[1], available_ports.pop(0))
            #del available_players[:2]
            print("GAME_MATCHING: 2 players deleted")
            
def create_game_instance(address, player_1, player_2, port):
    game_board = [[" "," "," "], [" "," "," "], [" "," "," "]]
    player_1_name = player_1[1]
    player_1 = player_1[0]
    player_2_name = player_2[1]
    player_2 = player_2[0]
    
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
            game_board, x, y = player_1_turn(player_1, player_2, game_board, player_1_role, player_1_name, player_2_name)
            if x and y:
                player_2.sendall(("Move,{},{}\n".format(x,y)).encode())
            game_board, x, y = player_2_turn(player_2, player_2, game_board, player_2_role, player_2_name, player_1_name)
            if x and y:
                player_1.sendall(("Move,{},{}\n".format(x,y)).encode())
    else:
        while True:
            game_board, x, y = player_2_turn(player_2, player_1, game_board, player_2_role, player_2_name, player_1_name)
            if x and y:
                player_1.sendall(("Move,{},{}\n".format(x,y)).encode())
            game_board, x, y = player_1_turn(player_1, player_2, game_board, player_1_role, player_1_name, player_2_name)
            if x and y:
                player_2.sendall(("Move,{},{}\n".format(x,y)).encode())

def player_1_turn(player_1, player_2, game_board, player_1_role, player_1_name, player_2_name):
    player_1.sendall("Turn,Make a move.\n".encode())
    player_1_data = player_1.recv(64).decode().split(",")
    if "Move" in player_1_data:
        game_board[int(player_1_data[2])][int(player_1_data[1])] = player_1_role
        result = check_board_state(game_board, player_1_role)
        if (result == "win" or result == "tie"):
            win_game_or_tie(player_1, player_2, player_1_role, result, player_1_name, player_2_name, game_board)
        return game_board, player_1_data[1], player_1_data[2]
    else:
        print("GAME_INSTANCE: No 'Move' in data. No move was made. (P1)")
        return game_board, False, False
            
def player_2_turn(player_2, player_1, game_board, player_2_role, player_2_name, player_1_name):
    player_2.sendall("Turn,Make a move.\n".encode())
    player_2_data = player_2.recv(64).decode().split(",")
    if "Move" in player_2_data:
        game_board[int(player_2_data[2])][int(player_2_data[1])] = player_2_role
        result = check_board_state(game_board, player_2_role)
        if (result == "win" or result == "tie"):
            win_game_or_tie(player_2, player_1, player_2_role, result, player_2_name, player_1_name, game_board)
        return game_board, player_2_data[1], player_2_data[2]
    else:
        print("GAME_INSTANCE: No 'Move' in data. No move was made. (P2)")
        return game_board, False, False

def check_board_state(game_board, role):
    for i in range(3):
        horizontal_check = all(space == role for space in game_board[i])
        vertical_check = all(space == role for space in [game_board[j][i] for j in range(3)])
        if vertical_check or horizontal_check:
            return "win"
            
    diagonal_check = all(space == role for space in [game_board[i][i] for i in range(3)])
    opposite_diagonal_check = all(space == role for space in [game_board[2-i][0+i] for i in range(3)])
    if diagonal_check or opposite_diagonal_check:
        return "win"
        
    is_empty_spaces = False
    for i in range(3):
        for j in range(3):
            if game_board[i][j] == " ":
                is_empty_spaces = True
                
    if not is_empty_spaces:
        return "tie"
    return False
        
def win_game_or_tie(winner, loser, winning_role, result, winner_name, loser_name, game_board):
    server_address = ('localhost', 1998)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(server_address)
        if result == "win":
            sock.sendall("Game,{},w,{},l".format(winner_name, loser_name).encode())
            stats = sock.recv(128).decode().split(",")
            if "CombinedStats" in stats:
                winner.sendall(("Stats,w,{},{},{}".format(stats[1], stats[2], stats[3])).encode())
                loser.sendall(("Stats,l,{},{},{}".format(stats[4], stats[5], stats[6])).encode())
            
        elif result == "tie":
            sock.sendall("Game,{},t,{},t".format(winner_name, loser_name).encode())
            stats = sock.recv(128).decode().split(",")
            if "CombinedStats" in stats:
                winner.sendall(("Stats,t,{},{},{}".format(stats[1], stats[2], stats[3])).encode())
                loser.sendall(("Stats,t,{},{},{}".format(stats[4], stats[5], stats[6])).encode())
        sock.close()
    except: 
        print("Failed to connect to server.")
        input("Press Enter to continue...")
        sock.close()
    for i in range(3):
        print(game_board[i])
    
if __name__ == "__main__":
    start_game_matching()
    