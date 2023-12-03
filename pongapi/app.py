#flask api

from flask import Flask, jsonify, request, Response
import hashlib as hasher
from pythongame import Game



keys = []
app = Flask(__name__)
keys.append("test")
games = []


@app.route('/ping', methods=['GET'])
def ping():
	return jsonify({'response': 'pong!'})

@app.route('/ping', methods=['POST'])
def post_ping():
	data = request.get_json()
	return jsonify(data), 201

@app.route('/api/get_key', methods=['POST'])
def give_key():
	data = request.get_json()
	key = hasher.sha256(str(data).encode('utf-8')).hexdigest()
	keys.append(key)
	return jsonify({'api': key}), 201

#done
@app.route('/api/new_game', methods=['POST'])
def new_game():
	data = request.get_json()
	if data['api'] not in keys:
		return jsonify({'response': 'invalid api key'}), 401
	if len(games) > 5:
		return jsonify({'response': 'server is full'}), 401
	password = data['password']
	game_id = data['game_id']
	for game in games:
		if game.game_id == game_id:
			return jsonify({'response': 'game id already exists'}), 401
	game = Game(password, game_id)
	games.append(game)
	resp = {'response': 'game created', 'game_id': game_id}
	return jsonify(resp), 201

#done
@app.route('/api/join_game', methods=['POST'])
def join_game():
	data = request.get_json()
	if data['api'] not in keys:
		return jsonify({'response': 'invalid api key'}), 401
	game_id = data['game_id']
	password = data['password']
	for game in games:
		if game.game_id == game_id:
			if game.password == password:
				game.join(data['api'])
				return jsonify({'response': 'game joined', 'game_id': game_id}), 201
			else:
				return jsonify({'response': 'invalid password'}), 401
		
	return jsonify({'response': 'game not found'}), 401


#done
@app.route('/api/game_state', methods=['POST'])
def game_state():
	data = request.get_json()
	if data['api'] not in keys:
		return jsonify({'response': 'invalid api key'}), 401
	game_id = data['game_id']
	for game in games:
		if game.game_id == game_id:
			if game.password == data['password']:
				ballx, bally = game.ball_pos()
				if game.paddle1.id == data['api']:
					p1x, p1y = game.p1_pos()
					p2x, p2y = game.p2_pos()
				else:
					p1x, p1y = game.p2_pos()
					p2x, p2y = game.p1_pos()

				state = game.state()
				resp = {'response': 'game state', 'game_id': game_id, 'ballx': ballx, 'bally': bally, 'p1x': p1x, 'p1y': p1y, 'p2x': p2x, 'p2y': p2y, 'state': state}
				return jsonify(resp), 201
			

			else:
				return jsonify({'response': 'invalid password'}), 401
	return jsonify({'response': 'game not found'}), 401


#done
@app.route('/api/move', methods=['POST'])
def move():
	data = request.get_json()
	if data['api'] not in keys:
		return jsonify({'response': 'invalid api key'}), 401
	game_id = data['game_id']
	for game in games:
		if game.game_id == game_id:
			if game.password == data['password']:
				game.move(data['api'], data['direction'])
				return jsonify({'response': 'moved'}), 201
			else:
				return jsonify({'response': 'invalid password'}), 401
	return jsonify({'response': 'game not found'}), 401


#done
@app.route('/api/leave_game', methods=['POST'])
def leave_game():
	data = request.get_json()
	if data['api'] not in keys:
		return jsonify({'response': 'invalid api key'}), 401
	game_id = data['game_id']
	for game in games:
		if game.game_id == game_id:
			if game.password == data['password']:
				game.leave(data['api'])
				return jsonify({'response': 'left'}), 201
			else:
				return jsonify({'response': 'invalid password'}), 401
	return jsonify({'response': 'game not found'}), 401

#done
@app.route('/api/game/<game_id>', methods=['POST'])
def game(game_id):
	data = request.get_json()
	if data['api'] not in keys:
		return jsonify({'response': 'invalid api key'}), 401
	for game in games:
		if game.game_id == game_id:
			if game.password == data['password']:
				if game.winner() == None:
					return jsonify({'response': 'game not over'}), 201
				if game.winner() == data['api']:
					return jsonify({'response': 'you won'}), 201
				if game.winner() != data['api']:
					return jsonify({'response': 'you lost'}), 201
			else:
				return jsonify({'response': 'invalid password'}), 401
	return jsonify({'response': 'game not found'}), 401





if __name__ == '__main__':
	app.run(debug=True)