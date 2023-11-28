
"""
 recive message format:
    {
        'usertoken': 'token',
        'username': 'username',
        'userid': 'userid',
        'message': 'message'
    }

    message format:
        {
            'type': 'type',
            'data': 'data'
        }
        types:
            joinroom
            leaveroom
            createroom
            deleteroom
            statusroom
            gameupdate

        data:
        
            joinroom, leaveroom, createroom, deleteroom, statusroom:
                {
                    'roomid': 'roomid'
                }

            gameupdate:
                {
                    'roomid': 'roomid',
                    'type': 'type',
                    'data': 'data'
                }
                types:
                    playermove

                data:
                    {
                        'playerposx': 'playerposx',
                        'playerposy': 'playerposy',
                        'playervelx': 'playervelx',
                        'playervely': 'playervely',
                        'playermomentumx': 'playermomentumx',
                        'playermomentumy': 'playermomentumy',
                    }
                
"""
import json

class Reciver:
	def __init__(self, raw_message):
		self.raw_message = raw_message
		try:

			self.data = json.loads(raw_message)
			print(self.data)
			self.usertoken = self.data['usertoken']
			self.username = self.data['username']
			self.userid = self.data['userid']
			self.message = self.data['message']
			self.message_type = self.message['type']
			self.message_data = self.message['data']

		except Exception as e:
			print(e)
			self.data = None
			self.usertoken = None
			self.username = None
			self.userid = None
			self.message = None
			self.message_type = None
			self.message_data = None

	class RoomOperation:
		def __init__(self, data):
			self.data = data
			self.roomid = data['roomid']

		def parse(self):
			if self.type == 'joinroom':
				self.joinroom()
			elif self.type == 'leaveroom':
				self.leaveroom()
			elif self.type == 'createroom':
				self.createroom()
			elif self.type == 'deleteroom':
				self.deleteroom()
			elif self.type == 'statusroom':
				self.statusroom()
			else:
				pass

		@staticmethod
		def joinroom(self):
			pass
		@staticmethod
		def leaveroom(self):
			pass
		@staticmethod
		def createroom(self):
			pass
		@staticmethod
		def deleteroom(self):
			pass
		@staticmethod
		def statusroom(self):
			pass

	
	
class GameUpdate:
	def __init__(self, data):
		self.data = data
		self.type = data['type']
		self.data = data['data']

		if self.type == 'playermove':
			self.playerposx = self.data['playerposx']
			self.playerposy = self.data['playerposy']
			self.playervelx = self.data['playervelx']
			self.playervely = self.data['playervely']
			self.playermomentumx = self.data['playermomentumx']
			self.playermomentumy = self.data['playermomentumy']
		else:
			self.playerposx = None
			self.playerposy = None
			self.playervelx = None
			self.playervely = None
			self.playermomentumx = None
			self.playermomentumy = None

		if self.type == 'playerready':
			self.playerready = self.data['playerready']

	def parse(self):
		if self.type == 'playermove':
			self.playermove()
		else:
			pass


	@staticmethod
	def playermove(self):
		pass


