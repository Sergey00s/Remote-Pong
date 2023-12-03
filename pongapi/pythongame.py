import pygame
import math
import numpy as np
import requests
import time
import threading as th


sizex = 1000
sizey = 1000

class Paddle:
	def __init__(self, x, y, width, height):
		self.firstpos = (x, y)
		self.x = x
		self.y = y
		self.width = width 
		self.height = height
		self.ready = False
		self.winner = False
		self.id = None		

	def reset(self):
		self.x = self.firstpos[0]
		self.y = self.firstpos[1]

	def move(self, direction):
		if direction == "up" and self.y > 0:
			self.y -= 10
		if direction == "down" and self.y < sizey - self.height:
			self.y += 10

	def beready(self):
		self.ready = True

	def gameover(self, winner):
		self.ready = False
		self.winner = winner


class Ball:
	def __init__(self, x, y, radius):
		self.firstpos = (x, y)
		self.x = x
		self.y = y
		self.radius = radius
		self.direction = [np.random.choice([-1, 1]), np.random.choice([-1, 1])]
		self.speed = 5


	def reset(self):
		self.x = self.firstpos[0]
		self.y = self.firstpos[1]
		self.direction = self.direction = [np.random.choice([-1, 1]), np.random.choice([-1, 1])]

	def bounce_x(self):
		self.direction[0] *= -1 * np.random.uniform(1, 1.4)
	def bounce_y(self):
		self.direction[1] *= -1 * np.random.uniform(1, 1.4)


	def update(self, delta=1):
		self.x += self.direction[0] * self.speed * delta
		self.y += self.direction[1] * self.speed * delta


class Game:
	def __init__(self, password, gameid, sizex=1000, sizey=1000):
		self.password = password
		self.gameid = gameid
		self.sizex = sizex
		self.sizey = sizey
		self.paddle1 = Paddle(0, sizey / 2, 20, 100)
		self.paddle2 = Paddle(sizex - 20, sizey / 2, 20, 100)
		self.ball = Ball(sizex / 2, sizey / 2, 10)
		self.score1 = 0
		self.score2 = 0
		self.state = "menu"
		self.gameid = None
		self.run_thread = th.Thread(target=self.run)
		self.run_thread.start()

	def run(self):
		inittime = time.time()
		while True:
			delta = time.time() - inittime
			self.update(delta)
			time.sleep(0.01)

	def score_2(self):
		self.score2 += 1
		self.ball.reset()
		self.paddle1.reset()
		self.paddle2.reset()

	def score_1(self):
		self.score1 += 1
		self.ball.reset()
		self.paddle1.reset()
		self.paddle2.reset()

	def gameover(self, winner):
		self.state = "gameover"
		self.winner = winner
		
	def leave(self, api):
		if api == self.paddle1.id:
			self.paddle1.id = None
			self.paddle1.ready = False
			self.gameover(self.paddle2)
		if api == self.paddle2.id:
			self.paddle2.id = None
			self.paddle2.ready = False
			self.gameover(self.paddle1)

	def move(self, api, direction):
		if api == self.paddle1.id:
			self.paddle1.move(direction)
		if api == self.paddle2.id:
			self.paddle2.move(direction)
		
	def join(self, api):
		if self.paddle1.id == None:
			self.paddle1.id = api
		elif self.paddle2.id == None:
			self.paddle2.id = api
		else:
			return False
		return True
		
	def ball_pos(self):
		return self.ball.x, self.ball.y
	
	def p1_pos(self):
		return self.paddle1.x, self.paddle1.y
	
	def p2_pos(self):
		return self.paddle2.x, self.paddle2.y
	def state(self):
		return self.state
	def winner(self):
		if self.score1 == 5:
			return self.paddle1
		if self.score2 == 5:
			return self.paddle2
		return None

	def reset(self):
		self.score1 = 0
		self.score2 = 0
		self.ball.reset()
		self.paddle1.reset()
		self.paddle1.ready = False
		self.paddle2.ready = False
		self.paddle2.reset()
		self.state = "pause"
		self.gameid = None
		self.paddle1.id = None
		self.paddle2.id = None

	def update(self, delta):
		if self.state == "menu":
			return
		if self.state == "pause":
			return
		if self.state == "gameover":
			return
		if self.score1 == 5:
			self.paddle1.gameover(True)
			self.paddle2.gameover(False)
			self.state = "gameover"
			return
		if self.score2 == 5:
			self.paddle1.gameover(False)
			self.paddle2.gameover(True)
			self.state = "gameover"
			return
		if self.paddle1.ready == False:
			return
		if self.paddle2.ready == False:
			return			
		if self.ball.x < 0:
			self.score_2()
			return 
		if self.ball.x > self.sizex:
			self.score_1()
			return
		if self.ball.y < 0 or self.ball.y > self.sizey:
			self.ball.bounce_y()
		if self.ball.x < self.paddle1.x + self.paddle1.width and self.ball.y > self.paddle1.y and self.ball.y < self.paddle1.y + self.paddle1.height:
			self.ball.bounce_x()
		if self.ball.x > self.paddle2.x and self.ball.y > self.paddle2.y and self.ball.y < self.paddle2.y + self.paddle2.height:
			self.ball.bounce_x()
		self.ball.update(delta)














	



