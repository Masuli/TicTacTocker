#GAME MATCHING LOGIC
#ports 100-1000
available_ports = [True for i in range(900)]

while True:
    connections = recv_connections()
    if connections:
        for connection in connections: 
            if account_doesnt_exist(connection.username, connection.password):
                create_account(connection.username, connection.password)
            add_player_to_pool(connection.username, connection.password)

    while pool has enough players:
        send game instance address / port to players
        create instance()
        remove players from pool()

#GAME INSTANCE LOGIC

def main(address, port):

    wait_for_players()
    player1_role = X
    player2_role = O

    send_roles()

    is_Player1_turn = True

    while game_is_running():
        notify_turn(is_player1_turn)
        recv_data = recv()
        handle_recv_data(recv_data, is_Player1_turn)
        #JNE
    
    connect_to_stats_component()
    send_result_to_stats_component()
    recv_stats_froms_stats()
    send_stats_to_clients()
    end()

#GAME CLIENT LOGIC
username = get_username()
pw = get_password()
#Login packet data: "Login <username>,<password>"
connection_succesful = connect_to_game_matching(username, password)
if connection_failed:
    return
address, port = wait_for_game()
connect(address, port)

role = recv_role()

while True:
    data = recv_data()
    if data.contains("Stats"):
        print_stats(data)
        end_game()
    if data.contains("Move x,y")
        update_board()
    if data.contains("Turn"):
        wait_for_player_input()
        send_move()


#GAME STATS COMPONENT

while True:
    accept_connections()
    data = recv_data()
    send_stats()