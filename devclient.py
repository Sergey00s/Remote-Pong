import asyncio
import websockets
import json




    


async def client():
    uri = "ws://localhost:8765"  # Server WebSocket URI'si

    async with websockets.connect(uri) as websocket:
        while True:
            msg = {"type": "gamerequest", "gameid": "123", "token": "123", "player1id": "123", "player2id": "1234"}
            msg = json.dumps(msg)
            await websocket.send(msg)  # Server'a mesaj gönderir
            message = await websocket.recv()  # Server'dan mesajı bekler
            print(f"Received message from server: {message}")

if __name__ == "__main__":
    asyncio.run(client())
