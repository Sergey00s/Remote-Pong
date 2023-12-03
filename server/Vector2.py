import math



class Vector2:
	def __init__(self, x, y):
		self.x = x
		self.y = y


	def distance(self, vec):
		return ((self.x - vec.x) ** 2 + (self.y - vec.y) ** 2) ** 0.5
	

	def distance_to_line(self, line_start, line_end):
		# https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
		# d = |(x2-x1)(y1-y0)-(x1-x0)(y2-y1)| / sqrt((x2-x1)^2 + (y2-y1)^2)
		d = abs((line_end.x - line_start.x) * (line_start.y - self.y) - (line_start.x - self.x) * (line_end.y - line_start.y)) / ((line_end.x - line_start.x) ** 2 + (line_end.y - line_start.y) ** 2) ** 0.5
		return d

	def angle(self):
		return math.atan2(self.y, self.x)

	def angle_between(self, vec):
		dot = self.dot(vec)
		mag = self.mag() * vec.mag()
		costheta = dot / mag
		return math.acos(costheta)

	def rotate(self, angle):
		angle = math.radians(angle)
		x = self.x * math.cos(angle) - self.y * math.sin(angle)
		y = self.x * math.sin(angle) + self.y * math.cos(angle)
		return Vector2(x, y)

	def ray_at(self, ray_start, ray_dir, t):
		return ray_start + ray_dir * t

	def is_ray_on(self, ray_origin, ray_dir, point):
		# ray_origin + ray_dir * t = point
		# t = (point - ray_origin) / ray_dir
		t = (point - ray_origin) / ray_dir

		return (t>=0)

	def is_point_on_line(self, line_start, line_end, point):
		# line_start + t * (line_end - line_start) = point
		# t = (point - line_start) / (line_end - line_start)
		t = (point - line_start) / (line_end - line_start)
		return (t>=0 and t<=1)

	def dot(self, vec):
		return self.x * vec.x + self.y * vec.y
	
	def cross(self, vec):
		result = self.x * vec.y - self.y * vec.x
		return result

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
		return self

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
	



