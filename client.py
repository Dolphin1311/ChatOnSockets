import socket
import threading
import sys


class Client:
    def __init__(self, host, port, nickname):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.location = (host, port)
        self.size = 1024
        self.nickname = nickname

        try:
            self.socket.connect(self.location)
        except ConnectionRefusedError:
            print('Cannot connect to server.')
            sys.exit()

        self.receive_thread = threading.Thread(target=self.receive)
        self.write_thread = threading.Thread(target=self.write)

        self.receive_thread.start()
        self.write_thread.start()

    def receive(self):
        """ Get messages from server """
        while True:
            try:
                message = self.socket.recv(self.size).decode('ascii')
                # send nickname of the client to server
                if message == 'NICK':
                    self.socket.send(self.nickname.encode('ascii'))
                elif message == 'NICK_ERROR':
                    print('This nickname is already used on server.')
                else:
                    print(message)
            except socket.error as e:
                print(str(e))
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()
                break

    def write(self):
        """ Send messages to server """
        while True:
            message = f'{self.nickname}: {input("")}'
            self.socket.send(message.encode('ascii'))


def main():
    c = Client('127.0.0.1', 55555, 'Arnold1')
    c.receive()


if __name__ == '__main__':
    main()
