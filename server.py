import socket

IP = "127.0.0.1"
PORT = 2222
# limiting to 4096 bytes per message, leaving the byte size to 4 digits
HEADER = 4

# initialize IPv4 with TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# persistence for port to keep it from hanging
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen(1)

def welcome_msg():
    message = "You have connected with the server!"
    message_header = len(message)
    result = bytes(f'{message_header}:<{{HEADER}}{message}')



while True:
    conn, addr = server_socket.accept()
    print(f"Connected to: {addr}")
    message_header = str(len())

    conn.send(welcome_msg())

    

    