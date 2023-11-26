


class Velocity:
	def __init__(self, x, y):
		self.x = x
		self.y = y


	def __add__(self, other):
		return Velocity(self.x + other.x, self.y + other.y)
	
	def __sub__(self, other):

		return Velocity(self.x - other.x, self.y - other.y)
	
	def __mul__(self, other):
		return Velocity(self.x * other, self.y * other)
	
	def __rmul__(self, other):
		return Velocity(self.x * other, self.y * other)
	
	def __truediv__(self, other):

		return Velocity(self.x / other, self.y / other)
	


class Ball:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.velocity = Velocity(0, 0)
		self.mass = 1
		self.momentum = self.mass * self.velocity


	def update(self, dt):
		self.velocity = self.momentum / self.mass
		self.x += self.velocity.x * dt
		self.y += self.velocity.y * dt
		self.momentum = self.mass * self.velocity
		

	def apply_force(self, force):
		self.momentum.x += force.x
		self.momentum.y += force.y


	def __repr__(self):
		return f'Ball: {self.x}, {self.y}'
	
	def is_colliding(self, player):
		if player is None:
			return False
		if self.x > player.topx and self.x < player.botx and self.y > player.topy and self.y < player.boty:
			return True
		return False
	
	def is_out_of_bounds(self):
		if self.x < 0 or self.x > 1000 or self.y < 0 or self.y > 1000:
			return True
		return False
	

class Player:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.topx = x - 10
		self.topy = y - 10
		self.botx = x + 10
		self.boty = y + 10
		self.velocity = Velocity(0, 0)
		self.mass = 1
		self.momentum = self.mass * self.velocity

	def update(self, x, y):
		self.x = x
		self.y = y
		self.topx = self.x - 10
		self.topy = self.y - 10
		self.botx = self.x + 10
		self.boty = self.y + 10

	def is_colliding(self, ball):
		if ball.x > self.topx and ball.x < self.botx and ball.y > self.topy and ball.y < self.boty:
			return True
		return False