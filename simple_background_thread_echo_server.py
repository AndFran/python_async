from threading import Thread
import socket


def handle_client(client_socket: socket.socket):
    while data := client_socket.recv(2048):
        print(f"Data received {data}")
        client_socket.sendall(data)  # echo data


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', 8000))
        server_socket.listen()
        print("Waiting for connections...........")
        while True:
            client_socket, address = server_socket.accept()
            print(f"New connection received: {address}")
            thread = Thread(target=handle_client, args=(client_socket,))
            thread.daemon = True
            thread.start()


if __name__ == '__main__':
    main()
