#!/usr/bin/env python3

import socket
import sys

GAME_MATCHING_PORT = 1999
available_ports = [i for i in range(2000, 3000)]

def start_game_matching():
    print("toimii")
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
                file.write(",".join(credentials))
                    
        connection.encode().sendall("GAME_MATCHING: You are now being matched against another player.")
        available_players.append(connection)
        if len(available_players) >= 2:
            create_game_instance("localhost", available_players[0], available_players[1], available_ports.pop(0))
            del available_players[:2]
            
def create_game_instance(address, player_1, player_2, port):
    player_1.sendall("GAME_INSTANCE: Player 2 connected.".encode())
    player_2.sendall("GAME_INSTANCE: Player 1 connected.".encode())
if __name__ == "__main__":
    start_game_matching()
    