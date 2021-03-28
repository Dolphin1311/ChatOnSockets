import socket


class Client:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.location = (host, port)
        self.size = 1024
        print('Created')

    def connect_to_server(self):
        self.socket.connect(self.location)  # connect to server
        data = input('Enter your message: ').encode()
        self.send_data_to_server(data)

    def send_data_to_server(self, data: bytes):
        while True:
            self.socket.sendall(data)  # send data to server
            reply = self.socket.recv(self.size)  # get data from server
            print(repr(reply))


def main():
    c = Client('127.0.0.1', 55555)
    c.connect_to_server()


if __name__ == '__main__':
    main()

