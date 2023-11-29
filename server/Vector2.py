import math

class Vector2:
	def __init__(self, x, y):
		self.x = x
		self.y = y


	def angle(self, vec):
		return math.atan2(vec.y - self.y, vec.x - self.x)

	def add(self, vec):
		self.x += vec.x
		self.y += vec.y

	def sub(self, vec):

		self.x -= vec.x
		self.y -= vec.y

	def mul(self, vec):
		self.x *= vec.x
		self.y *= vec.y

	def div(self, vec):

		self.x /= vec.x
		self.y /= vec.y

	def mag(self):
		return (self.x ** 2 + self.y ** 2) ** 0.5
	
	def normalize(self):
		mag = self.mag()
		self.x /= mag
		self.y /= mag

	def __str__(self):
		return "({},{})".format(self.x, self.y)
	
	def __repr__(self):
		return (self.x, self.y)
	
	def __add__(self, vec):
		return Vector2(self.x + vec.x, self.y + vec.y)
	
	def __sub__(self, vec):
		return Vector2(self.x - vec.x, self.y - vec.y)

	def __mul__(self, vec):
		if type(vec) == type(self):
			return Vector2(self.x * vec.x, self.y * vec.y)
		return Vector2(self.x * vec, self.y * vec)
	def __div__(self, n):
		if type(n) == type(self):
			return Vector2(self.x / n.x, self.y / n.y)
		return Vector2(self.x / n, self.y / n)
	def __truediv__(self, n):
		if type(n) == type(self):
			return Vector2(self.x / n.x, self.y / n.y)
		return Vector2(self.x / n, self.y / n)

	def __eq__(self, vec):
		return self.x == vec.x and self.y == vec.y
	def __ne__(self, vec):
		return self.x != vec.x or self.y != vec.y
	def __neg__(self):
		return Vector2(-self.x, -self.y)
	def __pos__(self):
		return Vector2(self.x, self.y)
	
	def __iadd__(self, vec):
		self.x += vec.x
		self.y += vec.y
		return self
	def __isub__(self, vec):
		self.x -= vec.x
		self.y -= vec.y
		return self
	
	def __imul__(self, vec):
		self.x *= vec.x
		self.y *= vec.y
		return self
	
	def __idiv__(self, vec):
		self.x /= vec.x
		self.y /= vec.y
		return self
	