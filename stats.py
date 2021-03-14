import os
import socket
import sys

def ensure_folder_exists(path):
    if not os.path.exists(path):
        os.makedirs(path,mode=0o777)

def get_path_for_player(player_name):
    return "players/{}/stats.txt".format(player_name)

def ensure_player_stats_exist(player_name):
    ensure_folder_exists("players/")
    ensure_folder_exists("players/" + player_name)
    filepath = get_path_for_player(player_name)
    if not os.path.exists(filepath):
        file = open(filepath, "w+")
        file.write("0,0,0")
        file.close()

def add_win_for_player(player_name):
    (wins, losses, ties) = get_stats_for_player(player_name)
    filepath = get_path_for_player(player_name)
    file = open(filepath, "w+")
    file.write("{},{},{}".format(wins + 1, losses, ties))
    file.close()

def add_loss_for_player(player_name):
    (wins, losses, ties) = get_stats_for_player(player_name)
    filepath = get_path_for_player(player_name)
    file = open(filepath, "w+")
    file.write("{},{},{}".format(wins, losses + 1, ties))
    file.close()

def add_tie_for_player(player_name):
    (wins, losses, ties) = get_stats_for_player(player_name)
    filepath = get_path_for_player(player_name)
    file = open(filepath, "w+")
    file.write("{},{},{}".format(wins, losses, ties + 1))
    file.close()

def get_stats_for_player(player_name):
    ensure_player_stats_exist(player_name)
    filepath = get_path_for_player(player_name)
    file = open(filepath, "r")
    file_content = file.read().split(",")
    file.close()
    return (int(file_content[0]), int(file_content[1]), int(file_content[2]))    

def add_player_stats(player_name, result):
    if result == 'w':
        add_win_for_player(player_name)
    elif result == 'l':
        add_loss_for_player(player_name)
    elif result == 't':
        add_tie_for_player(player_name)

def run_status_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("0.0.0.0", 1998)
    sock.bind(server_address)
    sock.listen(1)
    
    while True:
        connection, _ = sock.accept()
        recv_str = connection.recv(256).decode().split(",")
        if recv_str[0] != "Game":
            connection.close()
            continue
        add_player_stats(recv_str[1], recv_str[2])
        add_player_stats(recv_str[3], recv_str[4])
        (p1w, p1l, p1t) = get_stats_for_player(recv_str[1])
        (p2w, p2l, p2t) = get_stats_for_player(recv_str[3])
        connection.sendall("CombinedStats,{},{},{},{},{},{}".format(p1w, p1l, p1t, p2w, p2l, p2t).encode())
        connection.close()

if __name__ == "__main__":
    run_status_server()
