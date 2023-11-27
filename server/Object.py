import math



class GameObject:
	def __init__(self, x, y, width, height, static = False, name="GameObject"):
		self.name = name
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.physics = {
			'static': static, # If true, object will not have physics applied to it
			'friction': 0.9,
			'mass': 1,
			'velx': 0,
			'vely': 0,
			'momentumx': 0,
			'momentumy': 0
		}

	def get_center(self):
		return self.x + self.width / 2, self.y + self.height / 2
	
	def get_distance(self, other):
		return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
	
	def get_collision(self, other):
		if self.x < other.x + other.width and self.x + self.width > other.x and self.y < other.y + other.height and self.y + self.height > other.y:
			return True
		else:
			return False
		
	def apply_newton_force(self, force):
		self.physics['momentumx'] += force[0]
		self.physics['momentumy'] += force[1]

	def apply_friction(self):
		self.physics['velx'] *= self.physics['friction']
		self.physics['vely'] *= self.physics['friction']

	def update(self, dt = 1):
		if self.physics['static']:
			return
		self.pre_update()
		self.physics['velx'] = self.physics['momentumx'] / self.physics['mass'] 
		self.physics['vely'] = self.physics['momentumy'] / self.physics['mass']
		self.physics['momentumx'] = self.physics['mass'] * self.physics['velx']
		self.physics['momentumy'] = self.physics['mass'] * self.physics['vely']
		self.apply_friction()
		self.x += self.physics['velx'] * dt
		self.y += self.physics['vely'] * dt
		self.physics['velx'] += self.physics['momentumx']
		self.physics['vely'] += self.physics['momentumy']
		self.post_update()

	def on_collision(self, other : 'GameObject'):
		self.apply_newton_force((other.physics['momentumx'], other.physics['momentumy']))
		other.apply_newton_force((self.physics['momentumx'], self.physics['momentumy']))

	@staticmethod
	def pre_update():
		pass

	@staticmethod
	def post_update():
		pass

