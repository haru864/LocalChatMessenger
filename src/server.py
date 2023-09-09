import os
import socket
from faker import Factory


sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

server_address = "/tmp/socket_file"
try:
    os.unlink(server_address)
except FileNotFoundError:
    pass

print("Starting up on {}".format(server_address))

sock.bind(server_address)
sock.listen()
fake = Factory.create()

while True:
    connection, client_address = sock.accept()
    try:
        print(f"connection from {client_address}")
        while True:
            data = connection.recv(32)
            data_str = data.decode("utf-8")
            print("Received " + data_str)
            if data:
                respMessage = fake.text()
                print(f"Sending {respMessage}")
                connection.sendall(respMessage.encode())
            else:
                print(f"no data from {client_address}")
                break
    finally:
        print("Closing current connection")
        connection.close()
        break
