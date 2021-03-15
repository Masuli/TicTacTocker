FROM python:3.8

WORKDIR /usr/local/bin

EXPOSE 1999

COPY game_matching.py .

RUN pip3 install psutil

CMD ["python3", "game_matching.py"]
