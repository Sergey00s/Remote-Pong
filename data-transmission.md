Gameserver

types : 
	admin :
		commands:
			CRTROOM:
				args:
					name
					password

			RMVROOM:
				args:
					name
					password

			LIST:
				

			GET:
				args:
					what:
						RESULTS:
					

	user :
		commands:
			JOIN:
				args:
					name
					password
			STATUS:
				args:
					name

			MOVE:
				args:
					posX
					posY
					name
			BALL:
				args:
					posX
					posY
					name
			GET:
				args:
					what:
						BALL
						PLAYER
						WINNER
					name

	guest:
		NONE



Admin commands:

	Room Creation:

		jsonObj = {
			'type': 'admin',
			'data': {
						'password': ADMINPASS,
						'command':	'CRTROOM',
						'args': {
							'name' : ROOMNAME,
							'password': ROOMPASS
						}
					}
		
		}

	Room Remove:

		jsonObj = {
			'type': 'admin',
			'data': {
						'password': ADMINPASS,
						'command':	'RMVROOM',
						'args': {
							'name' : ROOMNAME
						}
					}
		
		}

	List room names:
		
		jsonObj = {
			'type': 'admin',
			'data': {
						'password': ADMINPASS,
						'command':	'LIST',
						'args': {}
					}
		
		}

		Respond:
			jsonObj = {
				type: data,
				data: {
					[DATA_LIST]
				}
			}

		
	
	Get attr from server:

		jsonObj = {
			'type': 'admin',
			'data': {
						'password': ADMINPASS,
						'command':	'GET',
						'args': {
							'what': ATTR,
							'room': ROOM
							ATTR_ARG: ARG
						}
					}
		
		}

		Respond:
			jsonObj = {
				'type': 'data',
				'data': {
					[DATA_LIST]
				}
			}




User commands:

	join room:
		
		jsonObj = {
			'type': 'user',
			'data': {
						'user_token': TOKEN,
						'command':	'JOIN',
						'args': {
							'name' : ROOMNAME,
							'password': ROOMPASS
						}
					}
		
		}

	
	get status:

		jsonObj = {
			'type': 'user',
			'data': {
						'user_token': TOKEN,
						'command':	'STATUS',
						'args': {
							'name' : ROOMNAME
						}
					}
		}

		Respond:
			jsonObj = {
				'type': 'data',
				'data': {
					[DATA_LIST]
				}
			}
