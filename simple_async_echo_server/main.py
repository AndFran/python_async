import asyncio
import socket
from asyncio import AbstractEventLoop


async def handle_client_connection(client_socket: socket.socket, loop: AbstractEventLoop):

    await loop.sock_sendall(client_socket, b"Welcome to the async echo server!\n")

    while data := await loop.sock_recv(client_socket, 1024):
        print(f"Data from {data}")
        await loop.sock_sendall(client_socket, data)
        print("Data echoed")


async def listen_for_connect(server_socket: socket.socket, loop: AbstractEventLoop):
    while True:
        client_socket, address = await loop.sock_accept(server_socket)
        print(f"connection from {address}")
        client_socket.setblocking(False)  # non blocking
        asyncio.create_task(handle_client_connection(client_socket, loop))


async def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind to an address
        server_address = ('127.0.0.1', 8000)
        server_socket.setblocking(False)  # non-blocking
        server_socket.bind(server_address)

        print("listing.......")
        server_socket.listen()

        loop = asyncio.get_event_loop()
        await listen_for_connect(server_socket, loop)


asyncio.run(main())
