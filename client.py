import socket
from Battleship import *

IP = "127.0.0.1"
PORT = 2222
HEADER = 4

# initialize IPv4 with TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP, PORT))


def send_message(conn, message = None) -> str:
    """
    Function to send messages within chat. Ensures a strict 4096 byte limit, including header
    """
    while True:
        to_send = input("Enter Input > ") if not message else message
        message_header = f'{len(to_send):<{HEADER}}'.encode('utf-8')
        message_body = to_send.encode('utf-8')
        # ensure that the header and message don't exceed our 4096 byte sending limit
        if len(message_header + message_body) > 4096:
            print("Message is too long, try again.")
        else:
            break

    conn.send(message_header + message_body)
    return to_send

def receive_message(conn) -> str:
    """
    Function to send messages within chat. Only receives as much as it needs
    """
    message_header = conn.recv(HEADER)
    if not message_header:
        return "(empty message)"
    message_length = int(message_header.decode('utf-8').strip())
    message_body = conn.recv(message_length)
    return message_body.decode('utf-8')

while True:
    # communication initiated by the server
    received = receive_message(client_socket)
    if received == '/q':
        print("Connection shutting down!")
        break
    
    print(f'Server: {received}')

    sent = send_message(client_socket)
    if sent == '/q':
        print("Connection shutting down!")
        break
    elif sent == '/battle':
        start = Battleship(1)
        start.play_game(client_socket, send_message, receive_message)

    
client_socket.close()



