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
                    playerready

                playermove:
                    data:
                        {
                            'playerposx': 'playerposx',
                            'playerposy': 'playerposy',
                            'playervelx': 'playervelx',
                            'playervely': 'playervely',
                            'playermomentumx': 'playermomentumx',
                            'playermomentumy': 'playermomentumy',
                        }
                playerready:
                    data:
                        {
                            'playerready': 'playerready'
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
from Message import Message
from Rooms import Rooms, Room
from User import User
from Reciver import Reciver

recived_messages  = []
messages_to_send = []

async def each_loop(websocket):
    global connections
    
    raw_message = await websocket.recv()
    try:
        rcv = Reciver(raw_message)
        message_obj = Message(message=rcv, socket=websocket)    
        recived_messages.append(message_obj)
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



async def send_messages():
    global messages_to_send
    global connections
    print('send loop')
    while True:
        if len(messages_to_send) > 0:
            message = messages_to_send.pop(0)
            await message.socket.send(message.message)
        else:
            await asyncio.sleep(0.01)



def update_player_pos(room: Room, data, user: User):
    if user == room.users[0]:
        room.game.player1.x = data['playerposx']
        room.game.player1.y = data['playerposy']
        room.game.player1.physics['velx'] = data['playervelx']
        room.game.player1.physics['vely'] = data['playervely']
        room.game.player1.physics['momentumx'] = data['playermomentumx']
        room.game.player1.physics['momentumy'] = data['playermomentumy']
    elif user == room.users[1]:
        room.game.player2.x = data['playerposx']
        room.game.player2.y = data['playerposy']
        room.game.player2.physics['velx'] = data['playervelx']
        room.game.player2.physics['vely'] = data['playervely']
        room.game.player2.physics['momentumx'] = data['playermomentumx']
        room.game.player2.physics['momentumy'] = data['playermomentumy']
    else:
        return False
    return True


def update_ready(room, data, user):
    if user == room.users[0]:
        room.game.player1ready = data['playerready']
    elif user == room.users[1]:
        room.game.player2ready = data['playerready']
    else:
        return False
    return True


def handle_messages(rooms: Rooms):
    global recived_messages
    global messages_to_send
    while len(recived_messages) > 0:
        message_obj = recived_messages.pop(0)
        message = message_obj.message
        user = User(message.userid, message.username, message.usertoken, message_obj.socket)
        print(message.message_type, " typed")
        if message.message_type == 'joinroom':
            room = rooms.get_room(message.message_data['roomid'])
            if room != None:
                rooms.join_room(room, user)
        elif message.message_type == 'leaveroom':
            pass
        elif message.message_type == 'createroom':
            room_to_add = Room(message.message_data['roomid'], password=None,messages_reference=messages_to_send)
            room = rooms.add_room(room_to_add)
        elif message.message_type == 'deleteroom':
            pass
        elif message.message_type == 'statusroom':
            pass
        elif message.message_type == 'gameupdate':
            room = rooms.get_room(message.message_data['roomid'])
            typeof = message.message_data['type']
            data = message.message_data['data']
            if typeof == "playermove":
                update_player_pos(room, data, user)
            elif typeof == "playerready":
                update_ready(room, data, user)
        else:
            pass
        
rooms = Rooms()

async def start_loop():

    global rooms
    print("manage loop")
    while True:
        handle_messages(rooms)
        rooms.update_each()
        await asyncio.sleep(0.01)


import signal
import os

def command_loop():
    global rooms
    while True:
        command = input("Command: ")
        if command == "rooms":
            print(rooms)
        elif command == "messages":
            print(messages_to_send)
        elif command == "connections":
            print(connections)
        elif command == "exit":
            pid = os.getpid()
            os.kill(pid, signal.SIGKILL)
            exit(0)
        else:
            print("Invalid command")



async def main():
    start_server_task = websockets.serve(handle_connection, "localhost", 2734)
    start_loop_task = asyncio.create_task(start_loop())
    send_messages_task = asyncio.create_task(send_messages())
    #command_loop_task = asyncio.create_task(command_loop())
    thread = th.Thread(target=command_loop)
    thread.start()
    await asyncio.gather(send_messages_task, start_server_task, start_loop_task)



if __name__ == "__main__":
    asyncio.run(main())




