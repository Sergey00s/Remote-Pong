import time
import json
from game import Game
send = None
recive = None
new_data = None

game = None



def handle_gamerequest(data, socket):
	token = data["token"]
	gameid = data["gameid"]
	player1id = data["player1id"]
	player2id = data["player2id"]
	if player1id == player2id:
		msj_json = {"error": "player1id and player2id can not be same"}
		msj_json = json.dumps(msj_json)
		send(msj_json, socket)
		return False
	if game.new_game(gameid, player1id, player2id) is False:
		msj_json = {"error": "refused"}
		msj_json = json.dumps(msj_json)
		send(msj_json, socket)
		return False  
	else:
		msj_json = {"success": "true"}
		msj_json = json.dumps(msj_json)
		send(msj_json, socket)
		return True

def handle_command(data, socket):
	try:
		data = json.loads(data)
	except Exception as e:
		print(e)
		msj_json = {"error": "invalid json"}
		msj_json = json.dumps(msj_json)
		send(msj_json, socket)
		return False
	typeof = data["type"]
	if typeof == "gamerequest":
		handle_gamerequest(data, socket)
	elif typeof == "getresult":
		result = game.get_result(data["gameid"])
		send_result = {"result": result}
		send_result = json.dumps(send_result)
		send(send_result, socket)
	elif typeof == "playerpos":
		game.playermove(socket, data)
	elif typeof == "join":
		if (game.join(data["playerid"], socket) == False):
			print("join refused: {} != {}".format((data["playerid"]), (game.player1.id)))
			msj_json = {"error": "refused"}
			msj_json = json.dumps(msj_json)
			send(msj_json, socket)
			return False
		return True
	elif typeof == "meready":
		game.player_ready(data["playerid"])
		return True
	else:
		msj_json = {"error": "invalid type"}
		msj_json = json.dumps(msj_json)
		send(msj_json, socket)
		return False

def app(sendf , recivef, new_dataf):
	global send, recive, new_data, game
	send = sendf
	recive = recivef
	new_data = new_dataf
	game = Game(400, 400, send, recive)
	while True:
		data = recive()
		try:
			if data != None:
				handle_command(data[1], data[0])
		except Exception as e:
			print(e)
		game.update()
		time.sleep(0.1)























