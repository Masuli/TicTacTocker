import os
import subprocess

if __name__ == "__main__":
    for i in range(0, 100):
        subprocess.Popen("ai_client.py client-{}".format(i), shell=True)