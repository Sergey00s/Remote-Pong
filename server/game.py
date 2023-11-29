import json

class Player:
	def __init__(self, id, socket):
		self.id = id
		self.socket = socket
		self.is_winner = False
		self.status = "unready"
		self.x = 0
		self.y = 0
		self.velx = 0
		self.vely = 0
		self.momx = 0
		self.momy = 0

	def move(self, data):
		print("player move")
		self.momx = data["momx"]
		self.momy = data["momy"]
		self.velx = data["velx"]
		self.vely = data["vely"]
		self.posx = data["posx"]
		self.posy = data["posy"]


class GameRoot:

	def __init__(self, witdh , height,  sendf, recvf):
		self.witdh = witdh
		self.height = height
		self.send = sendf
		self.recv = recvf
		self.gameid = None
		self.player1 = None
		self.player2 = None

	def new_game(self, gameid, player1id, player2id):
		if self.gameid != None:
			return False
		self.gameid = gameid
		self.player1 = Player(player1id, None)
		self.player2 = Player(player2id, None)
		print("new game")
		return True
		

	def get_result(self, gameid):
		if self.gameid == None:
			return False
		if self.gameid != gameid:
			return False
		if self.player1.is_winner:
			self.gameid = None
			return self.player1.id
		elif self.player2.is_winner:
			self.gameid = None
			return self.player2.id
		else:
			return -1
		
	def join(self, playerid, socket):
		if self.player1.id == playerid:
			self.player1.socket = socket
		elif self.player2.id == playerid:
			self.player2.socket = socket
		else:
			return False		
		return True
		
	def player_ready(self, playerid):
		if self.player1.id == playerid:
			self.player1.status = "ready"
		elif self.player2.id == playerid:
			self.player2.status = "ready"
		else:
			return False
		return True

	def send_start_warning(self):
		msg = {"type": "starting"}
		msg = json.dumps(msg)
		self.send(msg, self.player1.socket)
		self.send(msg, self.player2.socket)

	def send_be_ready(self):
		msg = {"type": "beready"}
		msg = json.dumps(msg)
		self.send(msg, self.player1.socket)
		self.send(msg, self.player2.socket)
	
	def send_winner(self, socket):
		msg = {"type": "winner"}
		msg = json.dumps(msg)
		self.send(msg, socket)
	
	def send_loser(self, socket):
		msg = {"type": "loser"}
		msg = json.dumps(msg)
		self.send(msg, socket)

	def send_ball(self, x, y):
		msg = {"type": "ball", "x": x, "y": y}
		msg = json.dumps(msg)
		self.send(msg, self.player1.socket)
		self.send(msg, self.player2.socket)


	def recive_playermove(self, socket, data):
		if self.player1.socket == socket:
			self.player1.move(data)
		elif self.player2.socket == socket:
			self.player2.move(data)
		else:
			return False
		return True



class gameobject:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.height = height
		self.width = width



class Ball(gameobject):
	def __init__(self, x, y, width, height, velx, vely):
		super().__init__(x, y, width, height)
		self.velx = velx
		self.vely = vely
		self.momx = 0
		self.momy = 0

	def applyforce(self, momx, momy):
		self.momx += momx
		self.momy += momy

	def update(self):
		if self.y <= 0:
			self.vely = -self.vely
		if self.y >= 390:
			self.vely = -self.vely
		self.momx = self.momx * 0.9
		self.momy = self.momy * 0.9
		self.velx += self.momx
		self.vely += self.momy
		self.x += self.velx
		self.y += self.vely

	def is_collide(self, obj):
		if self.x < obj.x + 10 and self.x + self.width > obj.x and self.y < obj.y + 50 and self.y + self.height > obj.y:
			return True
		return False

	def bounce(self, obj):
		if self.x < obj.x + 10 and self.x + self.width > obj.x:
			self.velx = -self.velx
		if self.y < obj.y + 50 and self.y + self.height > obj.y:
			self.vely = -self.vely

	def is_out(self, width, height):
		if self.x < 0 or self.x > width or self.y < 0 or self.y > height:
			return True
		return False
	
	def start(self,):
		self.velx = -1
		self.vely = 0
		self.momx= -0.5
		self.momy = 0





class Game(GameRoot):
	def __init__(self, witdh, height, sendf, recvf):
		super().__init__(witdh, height, sendf, recvf)
		self.status = "waiting"
		self.ball = Ball(200, 200, 10, 10, 0, 0)

	def playermove(self, socket, data):
		if self.status != "ongoing":
			return False
		if self.recive_playermove(socket, data) == False:
			return False
		return True

	def update(self):
		if (self.player1 is not None and self.player2 is not None):
			if (self.player1.socket is None or self.player2.socket is None):
				return
			if self.player1.status == "ready" and self.player2.status == "ready" and self.status == "waiting":
				self.status = "ongoing"
				self.send_start_warning()
				self.ball.start()
			else:
				self.send_be_ready()
		if self.status == "waiting":
			return
		if self.status == "ongoing":
			if self.ball.is_collide(self.player1):
				self.ball.bounce(self.player1)
			if self.ball.is_collide(self.player2):
				self.ball.bounce(self.player2)
			if self.ball.is_out(self.witdh, self.height):
				if self.ball.x < 0:
					self.player2.is_winner = False
					self.player1.is_winner = True
					self.status = "finished"
					self.send_winner(self.player1.socket)
					self.send_loser(self.player2.socket)
					return
				elif self.ball.x > self.witdh:
					self.player1.is_winner = False
					self.player2.is_winner = True
					self.status = "finished"
					self.send_winner(self.player2.socket)
					self.send_loser(self.player1.socket)
					return
			self.ball.update()
			self.send_ball(self.ball.x, self.ball.y)
			return
		if self.status == "finished":
			return