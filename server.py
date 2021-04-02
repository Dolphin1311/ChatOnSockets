import socket
import threading


class Server:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.location = (host, port)
        self.size = 1024
        self.clients = []
        self.nicknames = []

        try:
            self.socket.bind(self.location)
            self.socket.listen()
        except socket.error as e:
            print(str(e))

    def broadcast(self, message: bytes):
        """ Send message to all clients on server """
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        """ Handle the client """
        while True:
            try:
                message = client.recv(self.size)
                self.broadcast(message)
            except socket.error as e:
                print(str(e))
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast(f'{nickname} left the chat.'.encode('ascii'))
                self.nicknames.remove(nickname)
                break

    def receive(self):
        """ Get connections from clients"""
        while True:
            client, address = self.socket.accept()  # accept a connection to socket
            print(f'Connected to: {address[0]}:{address[1]}')
            client.send('NICK'.encode('ascii'))  # send the key word to client to get his nickname
            nickname = client.recv(self.size).decode('ascii')  # get the nickname from client

            if nickname in self.nicknames:
                client.send('NICK_ERROR'.encode('ascii'))
                client.shutdown(socket.SHUT_RDWR)
                client.close()
            else:
                self.nicknames.append(nickname)
                self.clients.append(client)
                print(f'Nickname of the client is: {nickname}')
                self.broadcast(f'{nickname} joined the chat.'.encode('ascii'))
                client.send('Connected to server.'.encode('ascii'))

                threading.Thread(target=self.handle, args=(client,)).start()


def main():
    s = Server('127.0.0.1', 55555)
    s.receive()


if __name__ == '__main__':
    main()
