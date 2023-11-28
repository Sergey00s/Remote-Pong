import asyncio
import websockets

connections = set()

async def listener(websocket, path):
    # Dinleyici fonksiyonu: Bağlanan kullanıcıları set'e ekler
    connections.add(websocket)
    try:
        async for message in websocket:
            # Eğer bir mesaj alırsanız, burada işlemleri gerçekleştirebilirsiniz
            pass
    finally:
        # Kullanıcı bağlantısı koptuğunda set'ten çıkar
        connections.remove(websocket)

async def sender():
    # Gönderici fonksiyonu: Connections set'indeki tüm websocketlere "hello" mesajı gönderir
    while True:
        await asyncio.sleep(1)  # Her saniye bir gönder
        for connection in connections:
            try:
                await connection.send("hello")
            except websockets.exceptions.ConnectionClosed:
                # Eğer bağlantı kapanmışsa, set'ten çıkar
                connections.remove(connection)

import time

async def hello():
    while True:
        await asyncio.sleep(1)
        print("hello")

async def main():
    # Hem dinleyici hem de gönderici fonksiyonlarını aynı anda çalıştır
    listener_task = websockets.serve(listener, "localhost", 8765)
    sender_task = asyncio.create_task(sender())
    hello_task = asyncio.create_task(hello())
    await asyncio.gather(listener_task, sender_task, hello_task)


if __name__ == "__main__":
    asyncio.run(main())
