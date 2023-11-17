import websockets
import asyncio
import threading as th
import json
import time
import sys
import readline




sock = None


while True:
    inpt = sys.stdin.readline()
    inpt = inpt.strip()
    cmd = inpt.split(' ')[0]
    if cmd == 'connect':
        sock = websockets.connect('ws://localhost:8080')
        print('Connected')
    elif cmd == 'send':
        msg = inpt.split(' ')[1]
        asyncio.get_event_loop().run_until_complete(sock.send(msg))
        print('Sent')












