from ppadb.client import Client as AdbClient
from ppadb.device import Device
import time
import numpy as np
from image_recognition import analyze_photo
from solver import solve_10x10


def connect():
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    if len(devices) == 0:
        print("No devices")
        quit()
    device: Device = devices[0]
    return device, client

def enter_solution(device, s):
    x_0 = 240
    y_0 = 816
    loc = zip(*np.where(s))
    swipestart = None
    swipeend = None
    for pos_y, pos_x in loc:
        device.shell(f"input tap {x_0 + 88*pos_x} {y_0 + 88*pos_y}")

def start_new_game(device: Device):
    device.shell("input tap 160 2058")
    device.shell("input tap 558 1680")


def solve_game(device: Device):
    device.shell("screencap -p /storage/emulated/0/Pictures/Screenshots/image.png")
    device.pull("/storage/emulated/0/Pictures/Screenshots/image.png", "/home/jannik/Documents/android_debug/img/screenshot.png")
    hints = analyze_photo()
    print(hints)
    assert sum([sum(x) for x in hints[0]]) == sum([sum(x) for x in hints[1]])
    assert sum([sum(x) for x in hints[0]]) > 10
    solution = solve_10x10(*hints)
    enter_solution(device, solution)

if __name__ == "__main__":
    device, client = connect()
    while True:
        solve_game(device)
        time.sleep(5)
        start_new_game(device)
        time.sleep(1)
