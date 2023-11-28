import asyncio
import websockets

async def client():
    uri = "ws://localhost:2734"  # Server WebSocket URI'si

    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()  # Server'dan mesajı bekler
            print(f"Received message from server: {message}")

if __name__ == "__main__":
    asyncio.run(client())
