import socket
from Battleship import *
from Colors import ColorsFg

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
print(f'Server running on: ({IP, PORT})')

def welcome_msg() -> bytes:
    """
    Welcome message and first communication by the server
    """
    message = '\n############################\nYou have connected with the server! Enter /q to quit anytime.\nYou will be prompted to enter message.\nEnter /battle to play ShipBattle, the Un-BattleShip!\n############################\n'.encode('utf-8')
    message_header = f'{len(message):<{HEADER}}'.encode('utf-8')
    return message_header + message

def send_message(conn, message = None) -> str:
    """
    Function to send messages within chat. Ensures a strict 4096 byte limit, including header
    """
    while True:
        to_send = input(f"{ColorsFg.green}Enter Input >{ColorsFg.reset} ") if not message else message
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
    conn, addr = server_socket.accept()
    print(f"Connected to client: {addr}")
    # initial contact by the server, welcoming the client
    conn.send(welcome_msg())
    print("Waiting on client...")

    while True:
        received = receive_message(conn)
        if received == '/q':
            print(f"{ColorsFg.yellow}Connection shutting down!{ColorsFg.reset}")
            break
        elif received == '/battle':
            start = Battleship(2)
            start.play_game(conn, send_message, receive_message)
            print("\nWelcome back to chat! Send a message...\n")
        
        else:
            print(f"{ColorsFg.lightcyan}Client:{ColorsFg.reset} {received}")

        sent = send_message(conn)
        if sent == '/q':
            print(f"{ColorsFg.yellow}Connection shutting down!{ColorsFg.reset}")
            break

    conn.close()
    break

server_socket.close()

    

    