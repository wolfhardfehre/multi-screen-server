#! /usr/bin/python3
import _thread
import socket
import time
import markdown2
from multiprocessing import Process
import random
import urllib.request
from random import random
from random import randint
from flask import Flask
from flask import request


app = Flask(__name__)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SERVER_IP = "192.168.1.9"
UDP_PORT = 8888
SHADER_PRESET_INTERVAL = 120
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


@app.route('/')
def index():
    file = open("README.md", "r")
    markdown = file.read()
    content = markdown2.markdown(markdown, extras=["tables"])
    return content


@app.route("/toggle_screen")
def toggle_screen():
    """
    Example: 192.168.1.9:5000/toggle_screen?on=1&screen=1

    Possibilities:
        0 -> Off
        1 -> On

    Possible Screens:
        0 -> all
        Other Number -> Specific Screen
    """
    on = request.args.get('on')
    screen = request.args.get('screen')
    if on is None or screen is None:
        return "Please choose either 0 (OFF) or 1 (ON) and provide a screen number!"
    package = bytes([1, int(on)])
    address = ADDRESSES[int(screen)]
    sock.sendto(package, (address, UDP_PORT))
    return "Turned Screen {} on: {}".format(screen, bool(int(on)))


@app.route("/change_shader")
def change_shader():
    """
    Example: 192.168.1.9:5000/change_shader?shader=3

    Possible Shader:
        0 -> Ren
        1 -> Stimpy
        2 -> Pinky
        3 -> Brain
    """
    shader = request.args.get('shader')
    if shader is None:
        return "Please provide a shader"
    package = bytes([1, int(shader)])
    for address in ADDRESSES:
        sock.sendto(package, (address, UDP_PORT))
    return "Changed all screens to shader {}".format(shader)


@app.route("/reset_time")
def reset_time():
    """
    Example: 192.168.1.9:5000/reset_time?screen=2

    Possible Screens:
        0 -> all
        Other Number -> Specific Screen
    """
    screen = request.args.get('screen')
    if screen is None:
        return "Please provide a screen"
    address = ADDRESSES[int(screen)]
    package = bytes([2])
    sock.sendto(package, (address, UDP_PORT))

    return "Reset time of Screen {}".format(screen)


@app.route("/reset_times")
def reset_times():
    """
    Example: 192.168.1.9:5000/reset_times?synced=1

    Possible Resets:
        0 -> random
        1 -> synced
    """
    synced = request.args.get('synced')
    if synced is None:
        return "Please provide an info if you want to sync times"
    synced = bool(int(synced))
    _thread.start_new_thread(reset_times_of_addresses, (synced,))
    return "Sync time off all screens: {}".format(synced)


def reset_times_of_addresses(synced):
    for address in ADDRESSES:
        package = bytes([2])
        sock.sendto(package, (address, UDP_PORT))
        if not synced:
            time.sleep(random())


@app.route("/screen_span")
def screen_span():
    """
    Example: 192.168.1.9:5000/screen_span?mode=1

    Possible Modes:
        0 -> local
        1 -> global
        > 1 -> random
    """
    modes = ("local", "global", "random")
    mode = request.args.get('mode')
    if mode is None:
        return "Please provide a span"
    mode = int(mode)
    for address in ADDRESSES:
        tmp = mode if mode < 2 else randint(0, 1)
        package = bytes([3, tmp])
        sock.sendto(package, (address, UDP_PORT))
    return "Changed screen spans to {}".format(modes[mode])


@app.route("/manual")
def manual():
    """
    Example: 192.168.1.9:5000/manual?mode=1

    Possible Modes:
        0 -> manual mode
        1 -> preset mode
    """
    modes = ["Manual Mode", "Preset Mode"]
    mode = request.args.get('mode')
    if mode is None:
        return "Please provide a mode"
    mode = int(mode)
    if mode == 0:
        if queue[0].is_alive():
            queue[0].terminate()
        queue.append(Process(target=change_shader_worker, args=(SHADER_PRESET_INTERVAL,)))
        if len(queue) > 1:
            del queue[0]
    else:
        if not queue[0].is_alive():
            queue[0].start()
    return "Changed mode to {}".format(modes[mode])


def change_shader_worker(interval):
    while True:
        shader = randint(1, 17)
        address = "http://{}:5000/change_shader?shader={}".format(SERVER_IP, shader)
        urllib.request.urlopen(address).read()
        time.sleep(interval)


if __name__ == '__main__':
    queue = [Process(target=change_shader_worker, args=(SHADER_PRESET_INTERVAL,))]
    app.run(host=SERVER_IP, port=5000)
