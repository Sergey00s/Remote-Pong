
"""
    send message format:

    {
        'type': 'type',
        'data': 'data'
    }

    types:
        gameupdate

    data:

        gameupdate:
            {
                'type': 'type',
                'data': 'data'
            }
            types:
                playermove
                ballmove

            data:
                playermove:
                    {
                        'remoteposx': 'remoteposx',
                        'remoteposy': 'remoteposy',
                    }
                ballmove:
                    {
                        'ballposx': 'ballposx',
                        'ballposy': 'ballposy',
                    }

                status:
                    winner, loser, waiting, playing, error, notfound
                    {
                        'status': 'status'
                    }

"""




import json



	
class Sender:
	def __init__(self, message_list: list = []):
		self.message_list = message_list

	def send(self, message):
		if type(message) == dict:
			message = json.dumps(message)
		return message


	def send_gameupdate(self, gameupdate):
		return self.send({
			'type': 'gameupdate',
			'data': {
				'type': gameupdate['type'],
				'data': gameupdate['data']
			}
		})


	def send_playermove(self, remote_pos):
		return self.send_gameupdate({
			'type': 'playermove',
			'data': {
				'remoteposx': remote_pos[0],
				'remoteposy': remote_pos[1],
			}
		})

	def send_ballmove(self, ball_pos):
		return self.send_gameupdate({
			'type': 'ballmove',
			'data': {
				'ballposx': ball_pos[0],
				'ballposy': ball_pos[1],
			}
		})

	def send_status(self, status):
		return self.send_gameupdate({
			'type': 'status',
			'data': {
				'status': status
			}
		})


	
