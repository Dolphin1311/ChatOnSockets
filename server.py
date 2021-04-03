import socket
import threading


class Server:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.location = (host, port)
        self.size = 1024
        self.clients = []
        self.nicknames = []
        self.password = 'admin'

        try:
            self.socket.bind(self.location)
            self.socket.listen()
        except socket.error as e:
            print(str(e))

    def broadcast(self, message: bytes):
        """ Send message to all clients on server """
        for client in self.clients:
            client.send(message)

    def handle(self, client: socket.socket):
        """ Handle the client """
        while True:
            try:
                msg = message = client.recv(self.size)
                if msg.decode('ascii').startswith('/kick'):  # kick client
                    if self.nicknames[self.clients.index(client)] == 'admin':
                        name_to_kick = msg.decode('ascii')[6:]
                        self.kick_user(name_to_kick)
                    else:
                        client.send('Command was refused'.encode('ascii'))
                elif msg.decode('ascii').startswith('/ban'):  # ban client
                    if self.nicknames[self.clients.index(client)] == 'admin':
                        name_to_ban = msg.decode('ascii')[5:]
                        self.ban_user(name_to_ban)

                        with open('bans.txt', 'a') as f:
                            f.write(f'{name_to_ban}\n')
                    else:
                        client.send('Command was refused'.encode('ascii'))
                else:
                    self.broadcast(message)
            except socket.error as e:
                if client in self.clients:
                    print(str(e))
                    index = self.clients.index(client)
                    self.clients.remove(client)
                    client.close()
                    nickname = self.nicknames[index]
                    self.broadcast(f'{nickname} left the chat.'.encode('ascii'))
                    self.nicknames.remove(nickname)
                    break

    def receive(self):
        """ Get connections from clients """
        while True:
            client, address = self.socket.accept()  # accept a connection to socket
            print(f'Connected to: {address[0]}:{address[1]}')
            client.send('NICK'.encode('ascii'))  # send the key word to the client to get his nickname
            nickname = client.recv(self.size).decode('ascii')  # get the nickname from client

            # check if client is banned
            with open('bans.txt', 'r') as f:
                bans = f.readlines()
                if nickname+'\n' in bans:
                    client.send('BAN'.encode('ascii'))
                    client.close()
                    break

            if nickname == 'admin':
                client.send('PASS'.encode('ascii'))  # send the key word to the client to get admin password
                password = client.recv(self.size).decode('ascii')

                if password != self.password:
                    client.send('REFUSE'.encode('ascii'))
                    client.close()
                    continue

            self.nicknames.append(nickname)
            self.clients.append(client)
            print(f'Nickname of the client is: {nickname}')
            self.broadcast(f'{nickname} joined the chat.'.encode('ascii'))
            client.send('Connected to server.'.encode('ascii'))

            threading.Thread(target=self.handle, args=(client,)).start()

    def kick_user(self, nickname: str):
        """ Kick client from server """
        if nickname in self.nicknames:
            name_index = self.nicknames.index(nickname)
            client_to_kick = self.clients[name_index]
            self.clients.remove(client_to_kick)
            client_to_kick.send('You were kicked by admin'.encode('ascii'))
            self.nicknames.remove(nickname)
            client_to_kick.close()
            self.broadcast(f'{nickname} was kicked by admin'.encode('ascii'))

    def ban_user(self, nickname):
        """ Ban client on server """
        self.kick_user(nickname)


def main():
    s = Server('127.0.0.1', 55555)
    s.receive()


if __name__ == '__main__':
    main()
