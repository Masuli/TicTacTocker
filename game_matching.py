import socket
import sys
import random

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
        with open("credentials.txt", "a+") as file:
            lines = [line.rstrip() for line in file]
            if ",".join(credentials) in lines:
                print("GAME_MATCHING: User exists.")
            else:
                print("GAME_MATCHING: User does not exist. Creating new user...")
                file.write(",".join(credentials) + "\n")
                    
        connection.sendall("GAME_MATCHING: You are now being matched against another player.".encode())
        available_players.append(connection)
        if len(available_players) >= 2:
            print("GAME_MATCHING: 2 players found")
            create_game_instance("localhost", available_players[0], available_players[1], available_ports.pop(0))
            #del available_players[:2]
            print("GAME_MATCHING: 2 players deleted")
            
def create_game_instance(address, player_1, player_2, port):
    print("GAME_INSTANCE: Called game instance")
    result = player_1.sendall("GAME_INSTANCE: Player 2 connected.".encode())
    print(result)
    result_2 = player_2.sendall("GAME_INSTANCE: Player 1 connected.".encode())
    print(result_2)
    
    x = random.randint(1,2)
    if x == 1:
        player_1.sendall("GAME_INSTANCE: Player 1 is X and will start.".encode())
        player_2.sendall("GAME_INSTANCE: Player 2 is O and will go second.")
        #while True:
            #player_1.sendall("GAME_INSTANCE: Your turn. Make a move.")
            #move = player_1.recv(64)
            #check_move(move)
        
    else:
        player_1.sendall("GAME_INSTANCE: Player 2 is X and will start.".encode())
        player_2.sendall("GAME_INSTANCE: Player 1 is O and will go second.")
        #while True:
            #player_2.sendall("GAME_INSTANCE: Your turn. Make a move.")
            #move = player_1.recv(64)
            #check_move(move)
            
if __name__ == "__main__":
    start_game_matching()
    