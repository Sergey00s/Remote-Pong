import json
import dotenv
import requests
import threading as th
import time
import objects as bl
import asyncio

env = dotenv.dotenv_values()

class Client:
    def __init__(self, websocket, id, player = bl.Player(0, 0)):
        self.websocket = websocket
        self.id = id
        self.privilage = None
        self.room = None
        self.player = player

    async def send(self, data):
        await self.websocket.send(data)
    
    def update_player(self, posX, posY):
        self.player = {'posX': posX, 'posY': posY}

    def __repr__(self) -> str:
        return f'Client(id={self.id}, room={self.room})'

class Room:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.client_one = None 
        self.client_two = None
        self.ball = bl.Ball(0, 0)
        self.winner = 0
        self.running = False
        print(f'Created room {self.name}')

    
    def add_client(self, client : Client):
        if self.client_one is None:
            self.client_one = client
        elif self.client_two is None:
            self.client_two = client
        else:
            raise Exception('Room is full')
        
        if self.client_one is not None and self.client_two is not None:
            if not self.running:
                self.running = True
                gameloop = asyncio.create_task(self.game_loop())
                print('Game loop started')

    async def _init(self):
        self.ball = bl.Ball(500, 500)
        self.client_one.player = bl.Player(10, 500)
        self.client_two.player = bl.Player(990, 500)
        self.winner = 0
        await self.client_one.send(json.dumps({'type': 'game', 'data': {'command': 'start', 'args': {}}}))
        await self.client_two.send(json.dumps({'type': 'game', 'data': {'command': 'start', 'args': {}}}))


    async def _collisions(self):
        if self.ball.is_colliding(self.client_one.player):
            f = self.client_one.player.velocity * self.client_one.player.mass
            self.ball.apply_force(f)
        if self.ball.is_colliding(self.client_two.player):
            f = self.client_two.player.velocity * self.client_two.player.mass
            self.ball.apply_force(f)
        if self.ball.is_out_of_bounds():
            if self.ball.x < 0:
                self.winner = 2
            elif self.ball.x > 1000:
                self.winner = 1
            else:
                self.winner = 0
            await self._init()

    async def _send_info(self):
        if self.client_one is not None:
            if self.client_two is not None:
                x = self.client_two.player.x
                y = self.client_two.player.y
                rdata = {'type': 'game', 'data': {'command': 'player', 'args': {'posX': x, 'posY': y}}}
                await self.client_one.send(json.dumps(rdata))
                x = self.ball.x
                y = self.ball.y
                rdata = {'type': 'game', 'data': {'command': 'ball', 'args': {'posX': x, 'posY': y}}}
                await self.client_one.send(json.dumps(rdata))
        if self.client_two is not None:
            if self.client_one is not None:
                x = self.client_one.player.x
                y = self.client_one.player.y
                rdata = {'type': 'game', 'data': {'command': 'player', 'args': {'posX': x, 'posY': y}}}
                await self.client_two.send(json.dumps(rdata))
                x = self.ball.x
                y = self.ball.y
                rdata = {'type': 'game', 'data': {'command': 'ball', 'args': {'posX': x, 'posY': y}}}
                await self.client_two.send(json.dumps(rdata))

    async def game_loop(self):
        await self._init()
        thickrate = 17
        print('Game loop started')
        while True:
            if self.client_one is None or self.client_two is None:
                break
            if self.winner != 0:
                break
            
            await self._collisions()
            self.ball.update(1/thickrate)
            await self._send_info()
            time.sleep(1/thickrate)

            



    def update_ball(self, posX, posY):
        self.ball = {'posX': posX, 'posY': posY}

    def __repr__(self) -> str:
        return f'Room(name={self.name})'
    
        

class Rooms:
    def __init__(self):
        self.rooms = {}

    def add_room(self, room):
        if room.name in self.rooms:
            raise Exception(f'Room {room.name} already exists')
        self.rooms[room.name] = room

    def remove_room(self, room):
        del self.rooms[room.name]

    def get_room(self, name):
        return self.rooms[name]
    
    def get_rooms(self):
        return self.rooms.values()
    
    def get_room_names(self):
        return self.rooms.keys()
    
    def get_room_clients(self):
        cleints = []
        for room in self.get_rooms():
            if room.client_one is not None:
                cleints.append(room.client_one)
            if room.client_two is not None:
                cleints.append(room.client_two)
        return cleints
    
    def get_user_by_id(self, id):
        clients = self.get_room_clients()
        print(clients)
        for client in clients:
            if client.id == id:
                return client
        return None


class Parser:
    # { type: 'type', data: 'data' }
    
    def __init__(self, data : str):
     
        self.raw = data
        try:
            self.data = json.loads(data)
            self.type = self.data['type']
            self.raw_data = self.data['data']
            #self.admin_parser = self.AdminParser(self.raw_data)

        except json.JSONDecodeError as e:
            self.data = None
            raise e
        
    class AdminParser:
        def __init__(self, websocket, data : dict):
            self.data = data
            try:
                self.websocket = websocket
                self.admin_password = data['password']
                #self.admin_password = Privilage.rot13(self.admin_password)
                if self.admin_password != env['ADMIN_PASSWORD']:
                    raise Exception('Wrong admin password : ' + self.admin_password)
                self.command = data['command']
                self.args = data['args']
            except KeyError as e:
                raise Exception(f'KeyError: {e}')

        def parse_run(self, rooms : Rooms):
            if self.command == 'CRTROOM':
                name = self.args['name']
                password = self.args['password']
                room = Room(name, password)
                rooms.add_room(room)
                return None
            elif self.command == 'RMVROOM':
                rooms.remove_room(rooms.get_room(self.args['name']))
                return None
            elif self.command == 'LIST':
                return list(rooms.get_room_names())
            elif self.command == 'PING':
                return 'PONG'
            elif self.command == 'GET':
                what = self.args['what']
                if what == "RESULTS":
                    all_winners = []
                    for room in rooms.get_rooms():
                        all_winners.append(room.winner)
                    return all_winners
                else:
                    raise Exception('Unknown what')
            
            else:
                raise Exception(f'Unknown command {self.command}')
            
            return None
            

    class UserParser:
        def __init__(self, websocket, data : dict):
            self.data = data
            try:
                self.id = data['user_token']
                self.command = data['command']
                self.args = data['args']
                self.websocket = websocket
            except KeyError as e:
                raise Exception(f'UserParser Key error: {e}')

        def parse_run(self, rooms : Rooms):
            if self.command == "JOIN":
                room = rooms.get_room(self.args['name'])
                if room.password != self.args['password']:
                    raise Exception('Wrong password')
                if rooms.get_user_by_id(self.id) is not None:
                    raise Exception('User already in room')
                room.add_client(Client(self.websocket, self.id))
                return None
            if self.command == "STATUS":
                return rooms.get_room_by_id(self.args['name']).winner
            if self.command == "MOVE":
                posX = self.args['posX']
                posY = self.args['posY']
                room = rooms.get_room(self.args['name'])
                if room.client_one.websocket == self.websocket:
                    room.client_one.update_player(posX, posY)
                else:
                    room.client_two.update_player(posX, posY)
                return None
            if self.command == "BALL":
                
                posX = self.args['posX']
                posY = self.args['posY']
                room = rooms.get_room(self.args['name'])
                if room.client_one.websocket == self.websocket:
                    room.client_one.update_ball(posX, posY)
                else:
                    raise Exception('Wrong host')
                return None
        
            if self.command == "WINNER":
                room = rooms.get_room(self.args['name'])
                room.winner = self.args['winner']
                return None
            
            if self.command == "PING":
                return 'PONG'
            
            if self.command == "GET":
                what = self.args['what']
                if what == "BALL":
                    room = rooms.get_room(self.args['name'])
                    return room.ball
                elif what == "PLAYER":
                    room = rooms.get_room(self.args['name'])
                    if room.client_one.websocket == self.websocket:
                        return room.client_one.player
                    else:
                        return room.client_two.player
                elif what == "WINNER":
                    room = rooms.get_room(self.args['name'])
                    return room.winner
                else:
                    raise Exception('Unknown what')
                
            

    def __str__(self):
        return self.raw
    
    
    
    def data_parser(self, websocket, rooms : Rooms):
        if self.type == 'admin':
            return self.AdminParser(websocket, self.raw_data).parse_run(rooms)
        elif self.type == 'user':
            return self.UserParser(websocket, self.raw_data).parse_run(rooms)
        elif self.type == 'guest':
            return 'pass' #GuestParser(self.raw_data)
        raise Exception(f'Unknown type {self.type}')




class Privilage:
    def __init__(self):
        self.level = 0

    def __eq__(self, other):
        return self.level == other.level
    
    def __lt__(self, other):
        return self.level < other.level
    
    def __gt__(self, other):
        return self.level > other.level
    
    def __le__(self, other):
        return self.level <= other.level
    
    def __ge__(self, other):
        return self.level >= other.level
    
    def __ne__(self, other):
        return self.level != other.level
    
    def __str__(self):
        if self.level == 0:
            return 'guest'
        elif self.level == 1:
            return 'user'
        elif self.level == 2:
            return 'admin'
        elif self.level == 3:
            return 'owner'
        else:
            return 'unknown'
        
    def __hash__(self):
        return self.level
    
    def __add__(self, other):
        return Privilage(self.level + other)
    
    def __sub__(self, other):
        return Privilage(self.level - other)
    
    def rot13(string):
        result = ''
        for char in string:
            if char.isalpha():
                if char.isupper():
                    result += chr((ord(char) + 13 - 65) % 26 + 65)
                else:
                    result += chr((ord(char) + 13 - 97) % 26 + 97)
            else:
                result += char
        return result


    



    
