#!/usr/bin/env python
import keyboard
import asyncio
from threading import Thread
import json
import time
from websockets.client import connect

id = "car2"
position = [0.0,10.0]
websock = None

async def hello():
    global websock
    async with connect("ws://localhost:8765") as websocket:
        websock = websocket
        while True:
            dat = json.loads(await websock.recv())
            if dat["to"]!=id:
                continue
            if dat["type"]=="alert":
                print("\x1b[38;2;255;255;0m[ALERT]",dat["msg"].format(**dat["options"]),"\x1b[0m")

async def loop_hello():
    global position, websock
    await asyncio.sleep(2)
    while True:
        if websock is not None:
            #sprint("[PINGING]")
            await websock.send(json.dumps({"query":"hello", "id":id, "pos":position}))
        await asyncio.sleep(1)

async def listen_key():
    while True:
        await asyncio.sleep(1)
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('s'):
                position[1] = 7.0
        except:
            break 
    print("[EXITING KEYBOARD LISTENER]")

async def main():
    await asyncio.gather(hello(), loop_hello(), listen_key())

asyncio.run(main())
