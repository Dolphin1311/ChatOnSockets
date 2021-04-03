import socket
import threading
import sys


class Client:
    def __init__(self, host, port, nickname):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.location = (host, port)
        self.size = 1024
        self.nickname = nickname
        self.stop_thread = False

        # check if the client is admin
        if nickname == 'admin':
            self.password = input('Enter admin\'s password: ')

        try:
            self.socket.connect(self.location)
        except ConnectionRefusedError:
            print('Cannot connect to server.')
            sys.exit()

        # start threads of receiving and writing messages
        self.receive_thread = threading.Thread(target=self.receive)
        self.write_thread = threading.Thread(target=self.write)

        self.receive_thread.start()
        self.write_thread.start()

    def receive(self):
        """ Get messages from server """
        while True:
            if self.stop_thread:
                break

            try:
                message = self.socket.recv(self.size).decode('ascii')
                if message == 'NICK':
                    self.socket.send(self.nickname.encode('ascii'))  # send nickname to the server
                    next_message = self.socket.recv(self.size).decode('ascii')
                    if next_message == 'PASS':
                        self.socket.send(self.password.encode('ascii'))  # send password to the server
                        if self.socket.recv(self.size).decode('ascii') == 'REFUSE':
                            print('Wrong password')
                            self.stop_thread = True
                    elif next_message == 'BAN':
                        print('Connection refused because of BAN')
                        self.socket.close()
                else:
                    print(f'{message}')
            except socket.error as e:
                print(str(e))
                self.socket.close()
                break

    def write(self):
        """ Send messages to server """
        while True:
            if self.stop_thread:
                break

            message = f'{self.nickname}: {input("")}'
            if message[len(self.nickname) + 2:].startswith('/'):
                if self.nickname == 'admin':
                    if message[len(self.nickname) + 2:].startswith('/kick'):
                        self.socket.send(f'/kick {message[len(self.nickname) + 2 + 6:]}'.encode('ascii'))
                    elif message[len(self.nickname) + 2:].startswith('/ban'):
                        self.socket.send(f'/ban {message[len(self.nickname) + 2 + 5:]}'.encode('ascii'))
                    pass
                else:
                    print('Commands can only be executed by admin')
            else:
                self.socket.send(message.encode('ascii'))


def main():
    nickname = input('Enter nickname: ')
    c = Client('127.0.0.1', 55555, nickname)
    c.receive()


if __name__ == '__main__':
    main()
