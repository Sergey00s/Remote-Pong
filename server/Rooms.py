

class User:
	def __init__(self, userid, socket, token = None):
		self.userid = userid
		self.token = token
		self.socket = socket


	def get_userid(self):
		return self.userid
	
	def get_token(self):
		return self.token
	

	def get_socket(self):
		return self.socket

	def set_socket(self, socket):
		self.socket = socket

	


class Room:
	def __init__(self, name, owner):
		self.name = name
		self.owner = owner
		self.users = []
		self.message_to_go = []
		self.messages = []

	def add_user(self, user):
		self.users.append(user)

	def remove_user(self, user):
		self.users.remove(user)

	def get_users(self):
		return self.users

	def add_message(self, message):
		self.messages.append(message)

	def get_messages(self):
		return self.messages



class Rooms:
	def __init__(self):
		self.rooms = {}

	def add_room(self, room):
		self.rooms[room.name] = room

	def get_room(self, name):
		return self.rooms.get(name)

	def get_rooms(self):
		return self.rooms.values()

	def remove_room(self, name):
		del self.rooms[name]

	def get_room_names(self):
		return self.rooms.keys()