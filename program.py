
from socket import *
import sys as system

address = "127.0.0.1"
port = 5555

height = 10
width = 10

def main(argc, argv):
    if(argv[1] == "server"):
        sock_object = generate_server_socket(address, port)
    if(argv[1] == "client"):
        sock_object = generate_client_socket(address, port)

    boats = [[[0, 0], [0, 1]], [[2, 0], [2, 1]]]
    def_board = generate_defence_board(height, width)
    off_board = generate_offence_board(height, width)

    def_board = insert_boats_def_board(def_board, boats)

    if(argv[1] == "server"):
        server_game_loop(sock_object, boats, def_board, off_board)
    if(argv[1] == "client"):
        client_game_loop(sock_object, boats, def_board, off_board)

defeated = False

def server_game_loop(sock_object, boats, def_board, off_board):
    global defeated
    while(not defeated):
        display_playing_boards(def_board, off_board)

        position = input_shooting_position("INPUT")
        sock_object.send(position.encode("utf-8"))

        protocol = sock_object.recv(1024).decode("utf-8")
        if(protocol == "defeated"):
            break

        off_board = mark_protocol_positions(off_board, protocol)

    display_playing_boards(def_board, off_board)

    if(defeated):
        print("defeated")
    else:
        print("won")

def mark_protocol_positions(off_board, protocol):
    action = protocol.split(":")[0]
    positions = extract_protocol_positions(protocol)
    for position in positions:
        h_index = position[0]
        w_index = position[1]
        off_board[h_index][w_index] = '?'
    return off_board

def extract_protocol_positions(protocol):
    positions = protocol.split(":")[1].split("-")

    for index, position in enumerate(positions):
        positions[index] = decode_position_object(position)
    return positions

def client_game_loop(sock_object, boats, def_board, off_board):
    global defeated
    while(not defeated):
        display_playing_boards(def_board, off_board)

        position = sock_object.recv(1024).decode("utf-8")
        position = decode_position_object(position)

        def_board = mark_board_postion(def_board, boats, position)

        hit_boat = hit_defence_boat(def_board, boats, position)

        if(hit_boat):
            if(defence_boat_defeated(def_board, hit_boat)):
                def_board = mark_boat_sunken(def_board, hit_boat)

                if(defence_board_defeated(def_board, boats)):
                    sock_object.send("defeated".encode("utf-8"))
                    defeated = True; break

                else:
                    protocol = generate_protocol(hit_boat, position, "sunken")
                    sock_object.send(protocol.encode("utf-8"))

            else:
                protocol = generate_protocol(hit_boat, position, "hit")
                sock_object.send(protocol.encode("utf-8"))

        else:
            protocol = generate_protocol(hit_boat, position, "miss")
            sock_object.send(protocol.encode("utf-8"))


    display_playing_boards(def_board, off_board)

    if(defeated):
        print("defeated")
    else:
        print("won")

def generate_protocol(boat, position, action):
    if(action == "sunken"):
        positions = []
        for coordinate in boat:
            positions.append(",".join(map(str, coordinate)))
        protocol = ":".join([action, "-".join(positions)])
    else:
        protocol = ":".join([action, ",".join(map(str, position))])
    return protocol

def defence_boat_defeated(def_board, boat):
    for coordinate in boat:
        h_index = coordinate[0]
        w_index = coordinate[1]
        if(def_board[h_index][w_index] != 'X'):
            return False
    return True

def hit_defence_boat(def_board, boats, position):
    for boat in boats:
        for coordinate in boat:
            if(coordinate == position):
                return boat
    return None

def input_shooting_position(input_message):
    position = input("[%s]: " % input_message).strip()
    position = position.split(",")
    return encode_position_object(position)

def defence_board_defeated(def_board, boats):
    for boat in boats:
        for coordinate in boat:
            h_index = coordinate[0]
            w_index = coordinate[1]
            if(def_board[h_index][w_index] != '$'): # SUNKEN
                return False
    return True

def mark_boat_sunken(def_board, boat):
    for coordinate in boat:
        h_index = coordinate[0]
        w_index = coordinate[1]
        def_board[h_index][w_index] = '$' # SUNKEN
    return def_board

def mark_board_postion(def_board, boats, position):
    h_index = position[0]
    w_index = position[1]
    for boat in boats:
        for coordinate in boat:
            if(coordinate == position):
                def_board[h_index][w_index] = "X" # HIT
                return def_board
    def_board[h_index][w_index] = "¤" # HIT
    return def_board

def encode_position_object(position):
    encoded = ",".join(position)
    return encoded

def decode_position_object(position):
    decoded = position.split(",")
    for index, integer in enumerate(decoded):
        decoded[index] = int(integer)
    return decoded

def display_playing_boards(def_board, off_board):
    for h_index in range(height):
        for w_index in range(width):
            print(def_board[h_index][w_index], end=" ")

        print("\t", end="")

        for w_index in range(width):
            print(off_board[h_index][w_index], end=" ")

        print()
    print(); return True

def insert_boats_def_board(def_board, boats):
    for boat in boats:
        for coordinate in boat:
            h_index = coordinate[0]
            w_index = coordinate[1]
            def_board[h_index][w_index] = "#" # BOAT
    return def_board

def generate_offence_board(height, width):
    off_board = []
    for h_index in range(height):
        off_board.append([])
        for w_index in range(width):
            off_board[h_index].append(".") # NONE
    return off_board

def generate_defence_board(height, width):
    def_board = []
    for h_index in range(height):
        def_board.append([])
        for w_index in range(width):
            def_board[h_index].append(".") # NONE
    return def_board

def generate_server_socket(address, port):
    serv_sock = socket(AF_INET, SOCK_STREAM)
    serv_sock.bind((address, port))
    serv_sock.listen(1)
    cli_sock, cli_addr = serv_sock.accept()
    return cli_sock

def generate_client_socket(address, port):
    cli_sock = socket(AF_INET, SOCK_STREAM)
    cli_sock.connect((address, port))
    return cli_sock

if(__name__ == "__main__"):
    main(len(system.argv), system.argv)
