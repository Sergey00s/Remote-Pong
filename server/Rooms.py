
from User import User
from Game import Pong
from Sender import Sender
from Message import Message


class Room:
	def __init__(self, name, password, messages_reference, passedTokens = []):
		self.name = name
		self.users = []
		self.password = password
		self.passedTokens = passedTokens
		self.messages_reference = messages_reference
		self.game = Pong(800, 800)
	
	def add_user(self, user : User):
		if user in self.users:
			return False
		if self.game.status == 'playing':
			return False
		if len(self.users) >= 2:
			return False
		# if self.passedTokens != [] and user.token not in self.passedTokens:
		# 	return False
		self.users.append(user)
		if len(self.users) >= 2:
			self.start_game()
		print(f'User {user.username} joined room {self.name}')
		return True
		
	def remove_user(self, user : User):
		if user in self.users:
			self.users.remove(user)
			return True
		return False

	def update_user_position(self, user : User, posx, posy, velx, vely, momentumx, momentumy):
		if user == self.users[0]:
			self.game.update_player1(posx, posy, velx, vely, momentumx, momentumy)
		elif user == self.users[1]:
			self.game.update_player2(posx, posy, velx, vely, momentumx, momentumy)
		else:
			return False
		return True
	
	def message_player_pos(self):
		posx = self.game.player1.x
		posy = self.game.player1.y
		sender = Sender()
		msg = sender.send_playermove((posx, posy))
		msg_obj = Message(message=msg, socket=self.users[0].socket)
		self.messages_reference.append(msg_obj)
		pos2x = self.game.player2.x
		pos2y = self.game.player2.y
		msg2 = sender.send_playermove((pos2x, pos2y))
		msg_obj2 = Message(message=msg2, socket=self.users[1].socket)
		self.messages_reference.append(msg_obj2)

	def message_ball_pos(self):
		posx, posy = self.game.get_ball_pos()
		sender = Sender()
		msg = sender.send_ballmove((posx, posy))
		msg_obj = Message(message=msg, socket=self.users[0].socket)
		self.messages_reference.append(msg_obj)
		msg_obj2 = Message(message=msg, socket=self.users[1].socket)
		self.messages_reference.append(msg_obj2)


	def message_user_is_ready(self, user : User):
		if user == self.users[0]:
			self.game.player1ready = True
		elif user == self.users[1]:
			self.game.player2ready = True
		else:
			return False

	def update_game(self, dt = 1):
		if (self.game.update(dt) == False):
			return False
		self.message_player_pos()
		self.message_ball_pos()
		return True
	

	def start_game(self):
		self.game.reset()
		sender = Sender()
		msg = sender.send_status('beready')
		msg_obj = Message(message=msg, socket=self.users[0].socket)
		self.messages_reference.append(msg_obj)
		msg_obj2 = Message(message=msg, socket=self.users[1].socket)
		self.messages_reference.append(msg_obj2)
		self.game.status = 'waiting'


	def __str__(self):
		return self.name
	
	def __repr__(self):
		return self.name
	
	def __eq__(self, __value: object) -> bool:
		if isinstance(__value, Room):
			return self.name == __value.name
		return False


class Rooms:
	def __init__(self):
		self.rooms = []

	def update_each(self, dt = 1):
		for room in self.rooms:
			room.update_game(dt)

	def join_room(self, room : Room, user : User):
		if room.add_user(user):
			return True
		return False

	def add_room(self, room : Room):
		if room in self.rooms:
			return False
		self.rooms.append(room)

		return True
	
	def remove_room(self, room : Room):
		if room in self.rooms:
			self.rooms.remove(room)
			return True
		return False
	
	def get_room(self, name):
		for room in self.rooms:
			if room.name == name:
				return room
		return None
	
	def get_room_by_user(self, user : User):
		for room in self.rooms:
			if user in room.users:
				return room
		return None
	
	def get_room_by_token(self, token):
		for room in self.rooms:
			if token in room.passedTokens:
				return room
		return None
	
	def get_room_by_user_id(self, user_id):
		for room in self.rooms:
			for user in room.users:
				if user.id == user_id:
					return room
		return None
	
	def get_room_by_socket(self, socket):
		for room in self.rooms:
			for user in room.users:
				if user.socket == socket:
					return room
		return None
	
	def get_room_by_user_name(self, username):
		for room in self.rooms:
			for user in room.users:
				if user.username == username:
					return room
		return None
	
	def __str__(self):
		return str(self.rooms)
	
	def __repr__(self):
		return str(self.rooms)