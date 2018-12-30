#! /usr/bin/python3
import socket
from flask import Flask, request

app = Flask(__name__)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

UDP_PORT = 8888
ADDRESSES = [
    "127.0.0.1",
    "192.168.1.10",
    "192.168.1.11",
    "192.168.1.12",
    "192.168.1.13",
    "192.168.1.14",
    "192.168.1.15",
    "192.168.1.16",
    "192.168.1.17",
    "192.168.1.18",
    "192.168.1.19",
]

# screen is address
PROTOCOL = {
    "0": "On/Off",          # [0, off=0 | on=1]
    "1": "Change Shader",   # [1, shader=[0..4]]
    "2": "Time Reset",      # [2]
    "3": "Global/Local"     # [3, local=0 | global=1]
}


@app.route("/change_shader")
def change_shader():
    shader = request.args.get('shader')
    if shader is None:
        return "Please provide a shader"
    package = bytes([1, int(shader)])
    for address in ADDRESSES:
        sock.sendto(package, (address, UDP_PORT))
    return f"changed shader to {shader}"


@app.route("/shader_span")
def shader_span():
    full = request.args.get('full')
    if full is None:
        return "Please provide a span"
    package = bytes([3, int(full)])
    for address in ADDRESSES:
        sock.sendto(package, (address, UDP_PORT))
    return "changed to local screens"


@app.route("/sync_times")
def time_reset():
    for address in ADDRESSES:
        package = bytes([2])
        sock.sendto(package, (address, UDP_PORT))
    return f"sync times"


@app.route("/local_screen")
def local_screen():
    screen = request.args.get('screen')
    shader = request.args.get('shader')
    if screen is None or shader is None:
        return "Please provide a screen and shader"
    address = ADDRESSES[int(screen)]
    package = bytes([0, 0])
    sock.sendto(package, (address, UDP_PORT))
    return f"reset screen={screen}"


