

class User:
	def __init__(self, userid, username, token, socket):
		self.userid = userid
		self.username = username
		self.token = token
		self.socket = socket

	def __str__(self):
		return self.username
	
	def __repr__(self):
		return self.username
	
	def __eq__(self, __value: object) -> bool:
		if isinstance(__value, User):
			return self.userid == __value.userid or self.token == __value.token
		return False
	
