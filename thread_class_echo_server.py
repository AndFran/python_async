from threading import Thread
import socket


class EchoThreadClientSocket(Thread):
    def __init__(self, client_socket: socket.socket, address):
        super().__init__()
        self.client_socket = client_socket
        self.address = address

    def run(self) -> None:
        try:
            while data := self.client_socket.recv(2048):
                print(f"Data received {data}")
                self.client_socket.sendall(data)
            else:
                raise BrokenPipeError("Client closed connection")
        except OSError as e:
            print(f"Client thread closing {e}")

    def close(self):
        """
        Gracefully close the socket
        """
        if self.isAlive():
            print(f"Shutting down {self.address}")
            self.client_socket.shutdown(socket.SHUT_RDWR)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', 8000))
        server_socket.listen()
        print("Waiting for connections...........")
        thread_list: list[EchoThreadClientSocket] = []
        try:
            while True:
                client_socket, address = server_socket.accept()
                print(f"New connection received: {address}")
                thread = EchoThreadClientSocket(client_socket=client_socket, address=address)
                thread_list.append(thread)
                thread.start()
        except KeyboardInterrupt:
            print(f"Shitting down {len(thread_list)} threads")
            [thread.close() for thread in thread_list]


if __name__ == '__main__':
    main()
