import socket
import threading


class Server:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.location = (host, port)
        self.size = 1024
        try:
            self.socket.bind(self.location)
        except socket.error as e:
            print(str(e))

    def listen(self):
        self.socket.listen()  # enable a server to accept connections
        while True:
            conn, address = self.socket.accept()  # accept a connection to socket
            conn.settimeout(60)  # after 60 seconds must reconnect
            print(f'Connected to : {address[0]}:{address[1]}')
            threading.Thread(target=self.listen_to_client, args=(conn,)).start()

    def listen_to_client(self, conn):
        while True:
            try:
                data = conn.recv(self.size)  # get data from client
                if data:
                    conn.send(data)  # send data to client
                else:
                    raise Exception('Client was disconnected')
            except:
                conn.close()
                return False


def main():
    s = Server('127.0.0.1', 55555)
    s.listen()


if __name__ == '__main__':
    main()
