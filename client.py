import socket

IP = "127.0.0.1"
PORT = 2222
HEADER = 4

# initialize IPv4 with TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP, PORT))

