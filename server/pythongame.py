import pygame
import math
from Vector2 import Vector2
		
	
class Edge:
	def __init__(self, a, b):
		self.a = a
		self.b = b
		self.normal = self.get_normal()

	def get_normal(self):
		normal = Vector2(self.b.y - self.a.y, self.b.x - self.a.x)
		normal.normalize()
		normal = normal * -1
		return normal

	def get_distance(self, point):
		# line_start + t * (line_end - line_start) = point
		# t = (point - line_start) / (line_end - line_start)
		t = (point - self.a) / (self.b - self.a)
		return t

	def is_point_on(self, point):
		# line_start + t * (line_end - line_start) = point
		# t = (point - line_start) / (line_end - line_start)
		t = (point - self.a) / (self.b - self.a)
		return (t>=0 and t<=1)

	def is_ray_on(self, ray_origin, ray_dir, point):
		# ray_origin + ray_dir * t = point
		# t = (point - ray_origin) / ray_dir
		t = (point - ray_origin) / ray_dir

		return (t>=0)


	def set_normal(self, normal):
		self.normal = normal





class Rect:
	def __init__(self, x, y, w, h):
		self.pos = Vector2(x, y)
		self.w = w
		self.h = h

		self.top_left = Vector2(x, y)
		self.top_right = Vector2(x + w, y)
		self.bottom_left = Vector2(x, y + h)
		self.bottom_right = Vector2(x + w, y + h)

		self.edges = [
			Edge(self.top_left, self.top_right),
			Edge(self.top_right, self.bottom_right),
			Edge(self.bottom_right, self.bottom_left),
			Edge(self.bottom_left, self.top_left)
		]

	def collide(self, obj):
		if self.pos.x < obj.pos.x + obj.w and self.pos.x + self.w > obj.pos.x and self.pos.y < obj.pos.y + obj.h and self.pos.y + self.h > obj.pos.y:
			return True
		return False
	
	def edge_normal(self, a, b):
		normal = Vector2(b.y - a.y, b.x - a.x)
		normal.normalize()
		normal = normal * -1
		return normal
	
	def get_intersection_edge(self, obj : "Rect"):

		min_dist = self.edges[0]
		old = -1
		for edge in self.edges:

			d = obj.pos.distance_to_line(edge.a, edge.b)
			if old == -1 or d < old:
				min_dist = edge
				old = d

		return min_dist
	

	def new_pos(self, newpos):
		self.pos = newpos
		self.top_left = Vector2(self.pos.x, self.pos.y)
		self.top_right = Vector2(self.pos.x + self.w, self.pos.y)
		self.bottom_left = Vector2(self.pos.x, self.pos.y + self.h)
		self.bottom_right = Vector2(self.pos.x + self.w, self.pos.y + self.h)
		self.edges = [
			Edge(self.top_left, self.top_right),
			Edge(self.top_right, self.bottom_right),
			Edge(self.bottom_right, self.bottom_left),
			Edge(self.bottom_left, self.top_left)
		]

	def change_normal_direction_to_outside(self):
		for edge in self.edges:
			if edge.normal.dot(edge.a) < 0:
				edge.set_normal(edge.normal * -1)
	

class GameObj(Rect):
	def __init__(self, x, y, w, h, name="gameobj", static=False):
		super().__init__(x, y, w, h)
		self.last_pos = Vector2(x, y)
		self.velocity = Vector2(0, 0)
		self.acceleration = Vector2(0, 0)
		self.mass = 1
		self.friction = 0.01
		self.static = static

		self.name = name
		self.stage = "init"




	def update_collision(self, obj_list):
		for obj in obj_list:
			if obj == self:
				continue
			if self.collide(obj):
				self.on_collide(obj)
				if self.static:
					continue
				
				edge = obj.get_intersection_edge(self)
				normal = edge.normal

				angle = self.velocity.angle_between(normal)
				cos = math.cos(angle)
				sin = math.sin(angle)

				fx = self.velocity.x * cos
				fy = self.velocity.y * sin
				f = Vector2(fx, fy)
				print(f  * -1)
				self.set_velocity(f + self.velocity, 1)

	def get_collision_force(self, obj):
		# f = (m1 * v1) + (m2 * v2)
		f = (self.velocity * self.mass) + (obj.velocity * obj.mass)
		return f

	def apply_force(self, force, dt=1):
		self.acceleration += force / self.mass



	def update_position(self, dt=1):
		newpos =  ((self.velocity * dt) + (self.acceleration * 0.5) * (dt ** 2)) + self.pos
		self.new_pos(newpos)


	def tick(self, dt=1, obj_list = []):
		if self.stage == "init":
			self.on_init()
			self.stage = "update"

		self.update_collision(obj_list)
		self.update(dt)
		self.update_position(dt)

	def set_velocity(self, velocity, dt=1):
		self.velocity = velocity
		self.acceleration = Vector2(0, 0)

	def get_velocity(self):
		return self.velocity
	

	def update(self, dt=1):
		pass

	def on_init(self):
		self.set_velocity(Vector2(0.1, 0.1), 1)
		pass
	def on_collide(self, obj):
		pass




app = pygame.init()

screen = pygame.display.set_mode((400, 400))

pygame.display.set_caption("Pong")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 30)


obj_list = []

rect = GameObj(200, 200, 10, 10, "ball")

border_top = GameObj(0, 0, 400, 10, "border_top", True)
border_bottom = GameObj(0, 390, 400, 10, "border_bottom", True)

border_left = GameObj(0, 0, 10, 400, "border_left", True)
border_right = GameObj(390, 0, 10, 400, "border_right", True)

border_bottom.mass = 100000
border_top.mass = 100000
border_left.mass = 100000
border_right.mass = 100000


obj_list.append(rect)
obj_list.append(border_top)
obj_list.append(border_bottom)
obj_list.append(border_left)
obj_list.append(border_right)


def draw_line_by_angle(screen, color, start_pos, length, angle):
	end_pos = (start_pos[0] + length * math.cos(angle), start_pos[1] + length * math.sin(angle))
	pygame.draw.line(screen, color, start_pos, end_pos)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
	screen.fill((0, 0, 0))
	delta = clock.get_time()
	rect.tick(delta, obj_list)
	pygame.draw.rect(screen, (255, 255, 255), (rect.pos.x, rect.pos.y, rect.w, rect.h))
	pygame.draw.rect(screen, (255, 255, 255), (border_top.pos.x, border_top.pos.y, border_top.w, border_top.h))
	pygame.draw.rect(screen, (255, 255, 255), (border_bottom.pos.x, border_bottom.pos.y, border_bottom.w, border_bottom.h))
	pygame.draw.rect(screen, (255, 255, 255), (border_left.pos.x, border_left.pos.y, border_left.w, border_left.h))
	pygame.draw.rect(screen, (255, 255, 255), (border_right.pos.x, border_right.pos.y, border_right.w, border_right.h))
	pygame.display.update()
	clock.tick(60)
