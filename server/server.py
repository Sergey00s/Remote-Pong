import asyncio
import websockets
import json
import threading as th

data_list = []
respond_list = []

def send(data, socket):
	global respond_list
	respond_list.append((socket, data))

def recive(socket=None):
	global data_list
	if socket == None:
		if len(data_list) > 0:
			data = data_list.pop(0)
			return data
		else:
			return None
	for i in range(len(data_list)):
		if data_list[i][0] == socket:
			data = data_list.pop(i)
			return data
	return None

def new_data(data, socket):
	return (socket, data)

async def server(websocket, path):
	global data_list
	global respond_list
	while True:
		try:
			data = await websocket.recv()
			#print(data)
			data_list.append(new_data(data, websocket))
		except websockets.ConnectionClosed:
			print("Connection closed")
			break
		except Exception as e:
			print(e, "error")
			break

async def sender():
	global data_list
	global respond_list
	while True:
		if len(respond_list) > 0:
			respond = respond_list.pop(0)
			try:
				await respond[0].send(respond[1])
			except websockets.ConnectionClosed:
				print("Connection closed")
				continue
			except Exception as e:
				print(e, "error")
				continue
		await asyncio.sleep(0.01)



import application


def other_process(send, recive, new_data):
	application.app(send, recive, new_data)

async def main():
	server_task = asyncio.ensure_future(websockets.serve(server, 'localhost', 8765))
	sender_task = asyncio.ensure_future(sender())
	application_th = th.Thread(target=other_process, args=(send, recive, new_data))
	application_th.start()
	await asyncio.gather(server_task, sender_task)

if __name__ == '__main__':
	asyncio.run(main())




