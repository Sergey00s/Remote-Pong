from Object import GameObject
import time

class Pong:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.player1 = GameObject(0, 0, 10, 100, name="Player 1")
		self.player1ready = False
		self.player2 = GameObject(0, 0, 10, 100, name="Player 2")
		self.player2ready = False
		self.ball = GameObject(0, 0, 10, 10, name="Ball")
		self.borderTop = GameObject(0, 0, width, 1, static=True, name="Border")
		self.borderBottom = GameObject(0, height - 1, width, 1, static=True, name="Border")
		self.borderLeft = GameObject(0, 0, 1, height, static=True, name="Border")
		self.borderRight = GameObject(width - 1, 0, 1, height, static=True, name="Border")
		self.score = {
			'player1': 0,
			'player2': 0
		}
		self.status = 'waiting'
		self.reset()

	def get_score(self):
		return self.score['player1'], self.score['player2']

	def get_ball_pos(self):
		return self.ball.x, self.ball.y
	
	def get_player_pos(self):
		return self.player1.x, self.player1.y, self.player2.x, self.player2.y


	def update_player1(self, posx, posy, velx, vely, momentumx, momentumy):
		self.player1.x = posx
		self.player1.y = posy
		self.player1.physics['velx'] = velx
		self.player1.physics['vely'] = vely
		self.player1.physics['momentumx'] = momentumx
		self.player1.physics['momentumy'] = momentumy

	def update_player2(self, posx, posy, velx, vely, momentumx, momentumy):
		self.player2.x = posx
		self.player2.y = posy
		self.player2.physics['velx'] = velx
		self.player2.physics['vely'] = vely
		self.player2.physics['momentumx'] = momentumx
		self.player2.physics['momentumy'] = momentumy

	def update(self, dt = 1):
		if (self.player1ready == True and self.player2ready == True and self.status == 'waiting'):
			self.status = 'playing'
		if self.status == 'waiting' or self.status == 'finished' or self.status == 'reset':
			return False
		self.check_collision()
		self.player1.update(dt)
		self.player2.update(dt)
		self.ball.update(dt)
		return True
	
	def check_collision(self):
		if self.ball.get_collision(self.player1):
			self.ball.on_collision(self.player1)
		elif self.ball.get_collision(self.player2):
			self.ball.on_collision(self.player2)
		elif self.ball.get_collision(self.borderTop):
			self.ball.on_collision(self.borderTop)
		elif self.ball.get_collision(self.borderBottom):
			self.ball.on_collision(self.borderBottom)
		elif self.ball.get_collision(self.borderLeft):
			self.score['player2'] += 1
			self.ball.x = self.width / 2 - self.ball.width / 2
			self.ball.y = self.height / 2 - self.ball.height / 2
			self.ball.physics['velx'] = 0.5
			self.ball.physics['vely'] = 0.5
			self.status = 'finished'
			self.ball.on_collision(self.borderLeft)
		elif self.ball.get_collision(self.borderRight):
			self.score['player1'] += 1
			self.ball.x = self.width / 2 - self.ball.width / 2
			self.ball.y = self.height / 2 - self.ball.height / 2
			self.ball.physics['velx'] = 0.5
			self.ball.physics['vely'] = 0.5
			self.status = 'finished'
			self.ball.on_collision(self.borderRight)
		else:
			pass

	def reset(self):
		self.player1.x = 0
		self.player1.y = self.height / 2 - self.player1.height / 2
		self.player2.x = self.width - self.player2.width
		self.player2.y = self.height / 2 - self.player2.height / 2
		self.ball.x = self.width / 2 - self.ball.width / 2
		self.ball.y = self.height / 2 - self.ball.height / 2
		self.ball.physics['static'] = False
		self.ball.physics['friction'] = 0.99
		self.ball.physics['mass'] = 0.5
		self.ball.physics['velx'] = 0.5
		self.ball.physics['vely'] = 0.5
		self.ball.physics['momentumx'] = 0.5
		self.ball.physics['momentumy'] = 0.5
		self.status = 'waiting'
		self.score['player1'] = 0
		self.score['player2'] = 0
		self.player1ready = False
		self.player2ready = False

		