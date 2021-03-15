# TicTacTocker
Distributed Systems 521290S Course Project 2021

How to setup:

build everything first:
cd component/
sudo docker build -t <image_name> .

after building everything:
sudo docker run --net=host -i -t -p 1999:1999 <game_server_image_name> 
sudo docker run -i -t -p 1998:1998 <game_stats_image_name> 
sudo docker run --net=host -i -t <game_ai_client> #spawns ai_clients for testing 
sudo docker run --net=host -i -t <game_client> #for human players 

Get results:
sudo docker cp <game_server_container_id>:/usr/local/bin/memory.txt /path/to/file.txt
sudo docker cp <ai_client_container_id>:/usr/local/bin/latency.txt /path/to/file.txt
