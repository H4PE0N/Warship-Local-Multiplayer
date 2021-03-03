
from socket import *
import sys as system
import os as terminal
import string
from copy import *

BOARD_HEIGHT = 10
BOARD_WIDTH = 10

def input_socket_information():
    address = str(input("ADDRESS: "))
    if(address.upper() == "EXIT"):
        print("address was exit")
        system.exit("")
    try:
        port = int(input("PORT: "))
    except:
        print("the port must be an integer")
        return input_socket_information()
    return [str(address), str(port)]
    #return ["192.168.1.113", "5555"]

def setup_client_information():
    information = input_socket_information()
    address = information[0]; port = int(information[1])
    sock_object = generate_client_socket(address, port)
    if(sock_object == None):
        system.exit("the address or port was wrong")
    return sock_object

def setup_server_information():
    information = input_socket_information()
    address = information[0]; port = int(information[1])
    sock_object = generate_server_socket(address, port)
    if(sock_object == None):
        print("the address or port was wrong")
        return setup_server_information()
    return sock_object

def generate_server_socket(address, port):
    serv_sock = socket(AF_INET, SOCK_STREAM)
    try:
        serv_sock.bind((address, port))
    except:
        return None
    serv_sock.listen(1)
    cli_sock, cli_addr = serv_sock.accept()
    return cli_sock

def generate_client_socket(address, port):
    cli_sock = socket(AF_INET, SOCK_STREAM)
    try:
        cli_sock.connect((address, port))
    except:
        return None
    return cli_sock

def input_battleships_position(def_board):
    ship_sizes = [2, 3, 3, 4, 5]
    battleships = []

    for index in range(len(ship_sizes)):
        terminal.system("clear")
        display_battleship_board(def_board)

        battleship = input_battleship_position(battleships, index + 1, ship_sizes[index])

        battleships.append(battleship)
        coordinates = all_battleship_coordinates(battleship)
        for cords_index in range(len(coordinates)):
            h_index = coordinates[cords_index][0]
            w_index = coordinates[cords_index][1]
            def_board[h_index][w_index] = "BATTLESHIP"

    return battleships, def_board

def battleship_position_valid(battleships, battleship):
    battleship_cords = all_battleship_coordinates(battleship)
    for index in range(len(battleships)):
        current_cords = all_battleship_coordinates(battleship[index])
        for cords_index in range(len(current_cords)):
            if(current_cords[cords_index] in battleship_cords):
                return False
    return True

def all_battleship_coordinates(battleship):
    coordinates = []
    first_cord = battleship[0]
    second_cord = battleship[1]
    for h_index in range(first_cord[0], second_cord[0] + 1):
        for w_index in range(first_cord[1], second_cord[1] + 1):
            coordinates.append([h_index, w_index])
    return coordinates

def input_battleship_position(battleships, ship_number, size):
    input_message = ("BATTLESHIP #%d [SIZE: %d]: " % (ship_number, size))
    battleship = str(input(input_message)).strip().split(" ")
    battleship = decode_board_coordinates(battleship)
    if(battleship == None):
        return input_battleship_position(battleships, ship_number, size)

    height_size = abs(battleship[0][0] - battleship[1][0])
    width_size = abs(battleship[0][1] - battleship[1][1])
    total_size = (height_size + 1) * (width_size + 1)

    if(total_size == size and battleship_position_valid(battleships, battleship)):
        return battleship

    return input_battleship_position(battleships, ship_number, size)

def decode_board_coordinates(coordinates):
    for index in range(len(coordinates)):
        coordinate = coordinates[index]
        coordinates[index] = decode_board_coordinate(coordinate)
        if(coordinates[index] == None):
            return None
    return coordinates

def decode_board_coordinate(coordinate):
    try:
        letter = coordinate[0].upper()
        w_index = int(string.ascii_uppercase.index(letter))
        h_index = int(coordinate[1:]) - 1
    except:
        return None

    height_valid = (h_index < BOARD_HEIGHT and h_index >= 0)
    width_valid = (w_index < BOARD_WIDTH and w_index >= 0)

    if(height_valid and width_valid):
        return [h_index, w_index]
    return None

def setup_battleship_information(socket_role):
    global BOARD_HEIGHT, BOARD_WIDTH
    terminal.system("clear")

    if(socket_role.upper() == "SERVER"):
        sock_object = setup_server_information()
    elif(socket_role.upper() == "CLIENT"):
        sock_object = setup_client_information()

    off_board = generate_battleship_board(BOARD_HEIGHT, BOARD_WIDTH)
    if(off_board == None):
        system.exit("OFF BOARD CREATION FAILED")
    def_board = generate_battleship_board(BOARD_HEIGHT, BOARD_WIDTH)
    if(off_board == None):
        system.exit("DEF BOARD CREATION FAILED")
    #battleships, def_board = input_battleships_position(def_board)

    battleships = [[[0, 0], [0, 1]], [[2, 1], [2, 3]], [[4, 3], [4, 5]], [[6, 1], [6, 4]], [[8, 3], [8, 7]]]
    for index in range(len(battleships)):
        all_cords = all_battleship_coordinates(battleships[index])
        for cords_index in range(len(all_cords)):
            h_index = all_cords[cords_index][0]
            w_index = all_cords[cords_index][1]
            def_board[h_index][w_index] = "BATTLESHIP"

    display_battleship_boards(def_board, off_board)
    if(socket_role == "SERVER"):
        server_battleship_game(sock_object, def_board, off_board, battleships)
    elif(socket_role == "CLIENT"):
        client_battleship_game(sock_object, def_board, off_board, battleships)

def generate_battleship_board(height, width):
    battleship_board = []
    for h_index in range(height):
        battleship_board.append([])
        for w_index in range(width):
            battleship_board[h_index].append("EMPTY")
    return battleship_board

def server_battleship_game(sock_object, def_board, off_board, battleships):
    defeated = False
    won = False

    while(not defeated and not won):
        terminal.system("clear")
        display_battleship_boards(def_board, off_board)
        off_board, won = attack_opponent_coordinate(sock_object, off_board, won)
        if(won == True):
            break

        terminal.system("clear")
        display_battleship_boards(def_board, off_board)
        def_board, defeated = register_opponents_damage(sock_object, def_board, battleships, defeated)

    if(defeated):
        print("defeated")
    elif(won):
        print("won")
    else:
        system.exit("NEITHER WON OR DEFEATED")

def client_battleship_game(sock_object, def_board, off_board, battleships):
    defeated = False
    won = False

    while(not defeated and not won):
        terminal.system("clear")
        display_battleship_boards(def_board, off_board)
        def_board, defeated = register_opponents_damage(sock_object, def_board, battleships, defeated)
        if(defeated == True):
            break

        terminal.system("clear")
        display_battleship_boards(def_board, off_board)
        off_board, won = attack_opponent_coordinate(sock_object, off_board, won)

    if(defeated):
        print("DEFEATED")
    elif(won):
        print("WON")
    else:
        system.exit("NEITHER WON OR DEFEATED")

def input_attacking_coordinate(off_board):
    coordinate = input("INPUT COORDINATE: ").strip()
    coordinate = decode_board_coordinate(coordinate)
    if(coordinate == None):
        return input_attacking_coordinate(off_board)

    marker = off_board[coordinate[0]][coordinate[1]]
    if(marker == "EMPTY"):
        return encode_coordinate_object(coordinate)

    return input_attacking_coordinate(off_board)

def extract_protocol_coordinates(protocol):
    coordinates = protocol.split(":")[1].split("-")
    for index in range(len(coordinates)):
        coordinate = coordinates[index]
        coordinates[index] = decode_coordinate_object(coordinate)
    return coordinates

def decode_coordinate_object(coordinate):
    decoded = coordinate.split(",")
    for index in range(len(decoded)):
        decoded[index] = int(decoded[index])
    return decoded

def encode_coordinate_object(coordinate):
    encoded = ",".join(map(str, coordinate))
    return encoded

def mark_battleship_sunken(board, battleship):
    all_cords = all_battleship_coordinates(battleship)
    for index in range(len(all_cords)):
        h_index = all_cords[index][0]
        w_index = all_cords[index][1]
        board[h_index][w_index] = "SUNKEN"
    return board

def mark_protocol_coordinates(off_board, action, coordinates):
    if(action == "SUNKEN" or action == "DEFEATED"):
        off_board = mark_battleship_sunken(off_board, coordinates)
        return off_board

    h_index = coordinates[0][0]
    w_index = coordinates[0][1]

    if(action == "HIT"):
        off_board[h_index][w_index] = "HIT"
    elif(action == "MISS"):
        off_board[h_index][w_index] = "MISS"

    return off_board

def attack_opponent_coordinate(sock_object, off_board, won):
    coordinate = input_attacking_coordinate(off_board)
    sock_object.send(coordinate.encode("utf-8"))

    protocol = sock_object.recv(1024).decode("utf-8")
    action = protocol.split(":")[0]
    coordinates = extract_protocol_coordinates(protocol)

    if(action == "DEFEATED"):
        won = True;

    off_board = mark_protocol_coordinates(off_board, action, coordinates)
    return off_board, won

def register_opponents_coordinate(def_board, battleships, coordinate):
    h_index = coordinate[0]
    w_index = coordinate[1]
    for index in range(len(battleships)):
        all_cords = all_battleship_coordinates(battleships[index])
        if(coordinate in all_cords):
            def_board[h_index][w_index] = "HIT"
            return def_board
    def_board[h_index][w_index] = "MISS"
    return def_board

def hit_defence_battleship(def_board, battleships, coordinate):
    for index in range(len(battleships)):
        all_cords = all_battleship_coordinates(battleships[index])
        if(coordinate in all_cords):
            return copy(battleships[index])
    return None

def receive_opponents_coordinate(sock_object):
    decoded = None
    try:
        coordinate = sock_object.recv(1024).decode("utf-8")
        decoded = decode_coordinate_object(coordinate)
    except:
        system.exit("error while receiving protocol")
    return decoded

def register_opponents_damage(sock_object, def_board, battleships, defeated):
    coordinate = receive_opponents_coordinate(sock_object)
    def_board = register_opponents_coordinate(def_board, battleships, coordinate)
    hit_ship = hit_defence_battleship(def_board, battleships, coordinate)

    if(hit_ship == None):
        protocol = generate_socket_protocol("MISS", [coordinate])
        sock_object.send(protocol.encode("utf-8"))
        return def_board, defeated

    if(not defence_ship_defeated(def_board, hit_ship)):
        protocol = generate_socket_protocol("HIT", [coordinate])
        sock_object.send(protocol.encode("utf-8"))
        return def_board, defeated

    def_board = mark_battleship_sunken(def_board, hit_ship)

    if(defence_board_defeated(def_board, battleships)):
        protocol = generate_socket_protocol("DEFEATED", hit_ship)
        sock_object.send(protocol.encode("utf-8"))
        defeated = True; return def_board, defeated

    print(battleships)
    protocol = generate_socket_protocol("SUNKEN", hit_ship)
    print(battleships)

    sock_object.send(protocol.encode("utf-8"))
    return def_board, defeated

def defence_ship_defeated(def_board, battleship):
    all_cords = all_battleship_coordinates(battleship)
    for index in range(len(all_cords)):
        h_index = all_cords[index][0]
        w_index = all_cords[index][1]
        marker = def_board[h_index][w_index]
        if(marker != "HIT" and marker != "SUNKEN"):
            return False
    return True

def defence_board_defeated(def_board, battleships):
    for index in range(len(battleships)):
        if(not defence_ship_defeated(def_board, battleships[index])):
            return False
    return True

def generate_socket_protocol(action, coordinates):
    protocol_cords = coordinates
    for index, coordinate in enumerate(protocol_cords):
        protocol_cords[index] = ",".join(map(str, coordinate))
    coordinates = "-".join(coordinates)
    protocol = ":".join([action, coordinates])
    return protocol

def display_battleship_boards(def_board, off_board):
    global BOARD_HEIGHT, BOARD_WIDTH
    print("  1 2 3 4 5 6 7 8 9 10\t1 2 3 4 5 6 7 8 9 10")
    for h_index in range(BOARD_HEIGHT):
        print(string.ascii_uppercase[h_index], end=" ")
        display_board_width(def_board, h_index)
        print("\t", end="")
        display_board_width(off_board, h_index)
        print()
    return True

def display_board_width(board, h_index):
    for w_index in range(len(board[h_index])):
        string = board[h_index][w_index]
        marker = convert_string_marker(string)
        print(marker, end=" ")

def display_battleship_board(board):
    global BOARD_HEIGHT, BOARD_WIDTH
    print("   1 2 3 4 5 6 7 8 9 10")
    for h_index in range(len(board)):
        print(string.ascii_uppercase[h_index], end=" ")
        display_board_width(board, h_index)
        print()
    return True

markers = [["BATTLESHIP", "#"], ["EMPTY", "."], ["MISS", "%"], ["HIT", "X"], ["SUNKEN", "$"]]

def convert_string_marker(string):
    for index in range(len(markers)):
        if(string == markers[index][0]):
            return markers[index][1]
    return None

if(__name__ == "__main__"):
    try:
        socket_role = system.argv[1].upper()
    except:
        system.exit("TO FEW ARGUMENTS")
    setup_battleship_information(socket_role)
