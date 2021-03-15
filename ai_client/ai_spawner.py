import os
import subprocess
import time

if __name__ == "__main__":
    clients = []
    for i in range(0, 1000):
        clients.append(subprocess.Popen(["python3", "ai_client.py", "client-{}".format(i)]))
    finished_clients = [client.wait() for client in clients]
