import asyncio
import websockets
import threading as th
import json

connections = set()
"""
 recive message format:
    {
        'usertoken': 'token',
        'username': 'username',
        'userid': 'userid',
        'message': 'message'
    }

    message format:
        {
            'type': 'type',
            'data': 'data'
        }
        types:
            joinroom
            leaveroom
            createroom
            deleteroom
            statusroom
            gameupdate

        data:
        
            joinroom, leaveroom, createroom, deleteroom, statusroom:
                {
                    'roomid': 'roomid'
                }

            gameupdate:
                {
                    'roomid': 'roomid',
                    'type': 'type',
                    'data': 'data'
                }
                types:
                    playermove

                data:
                    {
                        'playerposx': 'playerposx',
                        'playerposy': 'playerposy',
                        'playervelx': 'playervelx',
                        'playervely': 'playervely',
                        'playermomentumx': 'playermomentumx',
                        'playermomentumy': 'playermomentumy',
                    }
                
"""


"""
    send message format:

    {
        'type': 'type',
        'data': 'data'
    }

    types:
        gameupdate

    data:

        gameupdate:
            {
                'type': 'type',
                'data': 'data'
            }
            types:
                playermove
                ballmove

            data:
                playermove:
                    {
                        'remoteposx': 'remoteposx',
                        'remoteposy': 'remoteposy',
                    }
                ballmove:
                    {
                        'ballposx': 'ballposx',
                        'ballposy': 'ballposy',
                    }

                status:
                    winner, loser, waiting, playing, error, notfound
                    {
                        'status': 'status'
                    }

"""




def make_msg(type, data):
    return json.dumps({'type': type, 'data': data})

 
async def each_loop(websocket):
    global connections
    
    raw_message = await websocket.recv()
    try:
        message = json.loads(raw_message)

    except json.decoder.JSONDecodeError as e:
        print(f'Invalid JSON: {e}')

        return

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
