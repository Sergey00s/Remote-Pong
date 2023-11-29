import pygame
import math
from Vector2 import Vector2
		
	

class Rect:
	def __init__(self, x, y, w, h):
		self.pos = Vector2(x, y)
		self.w = w
		self.h = h

	def collide(self, obj):
		if self.pos.x < obj.pos.x + obj.w and self.pos.x + self.w > obj.pos.x and self.pos.y < obj.pos.y + obj.h and self.pos.y + self.h > obj.pos.y:
			return True
		return False
	
class GameObj(Rect):
	def __init__(self, x, y, w, h, name="gameobj", static=False):
		super().__init__(x, y, w, h)
		self.velocity = Vector2(0, 0)
		self.momentum = Vector2(0, 0)
		self.acceleration = Vector2(0, 0)
		self.mass = 1
		self.static = static

		self.name = name
		self.stage = "init"
	
	def apply_force(self, force : Vector2):
		self.acceleration += force / self.mass

	def update_velocity(self, dt=1):
		self.velocity += self.acceleration * dt

	def update_position(self, dt = 1):
		if not self.static:
			self.pos += self.velocity * dt


	def update_collision(self, obj_list):
		for obj in obj_list:
			if obj == self:
				continue
			if self.collide(obj):
				self.on_collide(obj)

				collide_angle = self.pos.angle(obj.pos)
				collide_angle = math.degrees(collide_angle)

				#f = Vector2((self.velocity.x * math.cos(collide_angle)), (self.velocity.y * math.sin(collide_angle)))
				f = (obj.velocity * obj.mass ) - (Vector2(self.velocity * self.mass).x * math.cos(collide_angle), Vector2(self.velocity * self.mass).y * math.sin(collide_angle))
				self.velocity += f
				obj.velocity += f
				#obj.apply_force(f)

				obj_list.remove(obj)



				#obj.apply_force(obj.velocity * self.mass * self.velocity)

	def tick(self, dt=1, obj_list = []):
		if self.stage == "init":
			self.on_init()
			self.stage = "update"
		self.update_velocity(dt)
		self.update_collision(obj_list)
		self.update_position(dt)

	def update(self, dt=1):
		pass

	def on_init(self):
		self.velocity = Vector2(1, 1)

	def on_collide(self, obj):
		pass




app = pygame.init()

screen = pygame.display.set_mode((400, 400))

pygame.display.set_caption("Pong")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 30)


obj_list = []

rect = GameObj(100, 100, 10, 10, "ball")
rect2 = GameObj(100, 150, 10, 10, "ball2")
rect3 = GameObj(50, 120, 10, 10, "ball3")

border_top = GameObj(0, 0, 400, 10, "border_top", True)
border_bottom = GameObj(0, 390, 400, 10, "border_bottom", True)

border_left = GameObj(0, 0, 10, 400, "border_left", True)
border_right = GameObj(390, 0, 10, 400, "border_right", True)

border_bottom.mass = 100000
border_top.mass = 100000
border_left.mass = 100000
border_right.mass = 100000


obj_list.append(rect)
obj_list.append(rect2)
obj_list.append(rect3)
obj_list.append(border_top)
obj_list.append(border_bottom)
obj_list.append(border_left)
obj_list.append(border_right)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
	screen.fill((0, 0, 0))
	rect.tick(1, obj_list)
	rect2.tick(1, obj_list)
	rect3.tick(1, obj_list)
	pygame.draw.rect(screen, (255, 255, 255), (rect.pos.x, rect.pos.y, rect.w, rect.h))
	pygame.draw.rect(screen, (255, 255, 255), (rect2.pos.x, rect2.pos.y, rect2.w, rect2.h))
	pygame.draw.rect(screen, (255, 255, 255), (rect3.pos.x, rect3.pos.y, rect3.w, rect3.h))
	pygame.draw.rect(screen, (255, 255, 255), (border_top.pos.x, border_top.pos.y, border_top.w, border_top.h))
	pygame.draw.rect(screen, (255, 255, 255), (border_bottom.pos.x, border_bottom.pos.y, border_bottom.w, border_bottom.h))
	pygame.draw.rect(screen, (255, 255, 255), (border_left.pos.x, border_left.pos.y, border_left.w, border_left.h))
	pygame.draw.rect(screen, (255, 255, 255), (border_right.pos.x, border_right.pos.y, border_right.w, border_right.h))

	pygame.display.update()
	clock.tick(60)
