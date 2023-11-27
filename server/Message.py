class Message:
	def __init__(self, user_id=None, message=None, socket = None):
		self.user_id = user_id
		self.message = message
		self.socket = socket

	def __str__(self):
		return self.message
	
	def __repr__(self):
		return self.message
	
	def __eq__(self, other):
		return self.user_id == other.user_id and self.message == other.message
	
	def __ne__(self, other):
		return self.user_id != other.user_id or self.message != other.message
	