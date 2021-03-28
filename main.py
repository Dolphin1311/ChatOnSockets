import server
from client import Client

s = server.Server('127.0.0.1', 55555)
s.listen()

c = Client('127.0.0.1', 55555)
c.connect_to_server()

# c1 = Client('127.0.0.1', 55555)
# c1.connect_to_server()
