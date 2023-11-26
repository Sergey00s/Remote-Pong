import asyncio
import websockets
import threading as th
import json
import privilage as pr


connections = set()

rooms = pr.Rooms()

def make_msg(type, data):
    return json.dumps({'type': type, 'data': data})

 
async def each_loop(websocket):
    global connections
    global rooms
    
    raw_message = await websocket.recv()
    try:
        parse = pr.Parser(raw_message)
        val = parse.data_parser(websocket, rooms)
        print(f'Parsed: {val}')
        if val is not None:
            obj = make_msg('data', {'data': val})
            await websocket.send(obj)
    except Exception as e:
        err = f"Error: {e}\nRawMessage: {raw_message}\nRemoteAddr: {websocket.remote_address}"
        print(err)
        await websocket.send(make_msg('error', {'data': err}))


async def handle_connection(websocket, path):
    global connections
    
    connections.add(websocket)
    try:
        while True:
            await   each_loop(websocket)

    except websockets.exceptions.ConnectionClosed as e:
        print(f'Connection with {websocket.remote_address} closed: {e}')
        connections.remove(websocket)



start_server = websockets.serve(handle_connection, "localhost", 2734)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
