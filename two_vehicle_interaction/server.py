# RSU code
#!/usr/bin/env python

import asyncio
import random
from turtle import position
from typing import List
import websockets
from websockets.server import serve, WebSocketServerProtocol
import os
import json

THRESHOLDMAX = 5.5
THRESHOLDMIN = 2.0
nodes = {}
clients = {}
printfn = print
last_msgs = []
last_msg = ""
divider = ("-"*5+' '*5)*5

def shift(st):
    return st[1:]+st[0]

def dist(a: List[float], b: List[float]) -> float:
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5

async def echo(websocket: WebSocketServerProtocol):
    global position, nodes, last_msgs
    async for message in websocket:
        last_msgs.append(message)
        obj = json.loads(message)
        if obj["id"].startswith("rsu_"):
            if obj["query"]=="alert" and obj["msg"]=="blockage":
                for i,sock in clients.items():
                    try:
                        await sock.send(json.dumps({"id":"Ym1r", "type": "alert", "to": i, "msg": "go {redirect}", "options":{"redirect": random.choice(["left", "right"])}}))
                    except:
                        last_msgs.append(f"{sock} is empty")
        elif obj["query"] == "hello":
            if obj["id"] not in nodes:
                clients[obj["id"]] = websocket
                nbors = [i for i,v in nodes.items() if dist(v["pos"],obj["pos"])<=THRESHOLDMAX]
                nodes[obj["id"]]={"pos":obj["pos"],"neighbours":nbors}
            else:
                nodes[obj["id"]]["pos"] = obj["pos"]
            for i,v in nodes.items():
                if i==obj["id"]:
                    break
                vneighbours = list(v["neighbours"])
                if obj["id"] in vneighbours:
                    if dist(obj["pos"], v["pos"]) > THRESHOLDMAX:
                        nodes[i]["neighbours"].remove(obj["id"])
                    elif dist(obj["pos"], v["pos"]) < THRESHOLDMIN:
                        if obj["pos"][1]<v["pos"][1]:
                            await clients[obj["id"]].send(json.dumps({"type":"alert", "to": obj["id"], "msg": "slow down!!", "options":{}}))
                        elif obj["pos"][1]>v["pos"][1]:
                            await clients[i].send(json.dumps({"type":"alert", "to": i, "msg": "slow down!!", "options":{}}))
                else:
                    if dist(obj["pos"], v["pos"]) <= THRESHOLDMAX:
                        nodes[i]["neighbours"].append(obj["id"])

async def servermain():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

async def gui():
    global last_msg, last_msgs, divider
    while True:
        os.system("clear")
        printfn('-'*50)
        printfn(' '*50)
        e=""
        try:
            y = nodes["car1"]["pos"][1]*2
            printfn(" "*(int(y))+"car1")
        except BaseException as err:
            printfn(" "*50)
            e=repr(err)
        printfn(divider)
        divider = shift(divider)
        try:
            y = nodes["car2"]["pos"][1]*2
            printfn(" "*(int(y)-4)+"car2")
        except BaseException as err:
            printfn(" "*50)
            e=repr(err)
        printfn(' '*50)
        printfn('-'*50)
        if len(last_msgs)==0:
            printfn(last_msg)
        else:
            last_msg = last_msgs.pop()
            printfn(last_msg)
        printfn("simul server 1.3",nodes)
        await asyncio.sleep(0.1)

async def main():
    await asyncio.gather(servermain(), gui())

asyncio.run(main())
