#! /usr/bin/python3
import socket
from app import UDP_PORT, ADDRESSES

UDP_IP = ADDRESSES[0]
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, address = sock.recvfrom(1024)
    print(f"received message:{data}")
