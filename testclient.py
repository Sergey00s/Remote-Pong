import requests
import time




def create_game(gameid, password, private, password_p1, password_p2):
	data = {
		"gameid": gameid,
		"password": password,
		"private": private,
		"password_p1": password_p1,
		"password_p2": password_p2
	}
	resp = requests.post('http://localhost:5000/api/new_game', json=data)
	print (resp.status_code)
	print(resp.json())



def join_game(gameid, password, player, player_pass):
	data = {
		"gameid": gameid,
		"password": password,
		"player": player,
		"player_pass": player_pass
	}
	resp = requests.post('http://localhost:5000/api/join_game', json=data)
	print (resp.status_code)
	print(resp.json())

def get_game_state(gameid, password, player, player_pass):
	data = {
		"gameid": gameid,
		"password": password,
		"player": player,
		"player_pass": player_pass
	}
	resp = requests.post('http://localhost:5000/api/info', json=data)
	print (resp.status_code)
	print(resp.json())


def move(gameid, password, player, direction, player_pass):
	data = {
		"gameid": gameid,
		"password": password,
		"player": player,
		"direction": direction,
		"player_pass": player_pass
	}
	resp = requests.post('http://localhost:5000/api/move', json=data)
	print (resp.status_code)
	print(resp.json())



def new_get_state(gameid):
	resp = requests.get('http://localhost:5000/api/info/'+gameid)
	print (resp.status_code)
	print(resp.json())


def ping():
	resp = requests.get('http://localhost:5000/api/ping')
	print (resp.status_code)
	print(resp.json())



# create_game("game1", "pass", True, "pass1", "pass2")
# time.sleep(3)
# join_game("game1", "pass", 1, "pass1")
# time.sleep(3)
# join_game("game1", "pass", 2, "pass2")
# time.sleep(3)

# while True:
# 	new_get_state("game1")
# 	time.sleep(0.1)
# 	move("game1", "pass", 1, "up", "pass1")
# 	time.sleep(0.2)