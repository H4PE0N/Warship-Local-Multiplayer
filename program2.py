
from socket import *
import sys as system
import os as terminal
import string
from copy import *
from random import *

#############################################################

def check_input_exit(input_string, exit_message):
    exit_strings = ["QUIT", "EXIT", "LEAVE"]
    if(input_string.upper() in exit_strings):
        throw_error_quit(exit_message)

def send_socket_string(sock_object, sending_string):
    try:
        sock_object.send(sending_string.encode("utf-8"))
    except:
        return False
    return True

def throw_error_quit(error_message):
    system.exit(error_message)

def get_user_input(input_message):
    user_input = str(input(input_message)).strip()
    return user_input

#############################################################
def board_coordinates_keyword(board, coordinates, keyword):
    for index in range(len(coordinates)):
        coordinate = coordinates[index]
        board = board_coordinate_keyword(board, coordinate, keyword)
    return board

def board_coordinate_keyword(board, coordinate, keyword):
    h_index = coordinate[0]
    w_index = coordinate[1]
    board[h_index][w_index] = keyword
    return board

#############################################################
def input_battleships_position(def_board):
    ship_sizes = [2, 3, 3, 4, 5]
    battleships = []
    for index in range(len(ship_sizes)):
        display_battleship_board(def_board)
        battleship = input_battleship_position(battleships, index + 1, ship_sizes[index])
        battleships.append(battleship)
        coordinates = all_battleship_coordinates(battleship)
        def_board = board_coordinates_keyword(def_board, coordinates, "BATTLESHIP")
    return battleships, def_board

def battleship_position_valid(battleships, battleship):
    battleship_cords = all_battleship_coordinates(battleship)
    for index in range(len(battleships)):
        current_cords = all_battleship_coordinates(battleships[index])
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

def flip_battleship_coordinates(battleship):
    height_result = (battleship[0][0] > battleship[1][0])
    width_result = (battleship[0][1] > battleship[1][1])
    if(height_result == True or width_result == True):
        temp_coordinate = battleship[0]
        battleship[0] = battleship[1]
        battleship[1] = temp_coordinate
    return battleship

def generate_inputed_battleship(battleships, ship_number, size, battleship):

    battleship = decode_board_coordinates(battleship)

    if(battleship == None):
        return input_battleship_position(battleships, ship_number, size)

    battleship = flip_battleship_coordinates(battleship)

    height_size = (battleship[1][0] - battleship[0][0])
    width_size = (battleship[1][1] - battleship[0][1])
    total_size = (height_size + 1) * (width_size + 1)

    valid_pos = battleship_position_valid(battleships, battleship)
    if(total_size != size or valid_pos == False):
        return input_battleship_position(battleships, ship_number, size)

    return battleship

def generate_random_battleship(battleships, size):
    height_range = (10 - size - 1)
    width_range = (10 - size - 1)

    first_cord = [randint(0, height_range), randint(0, width_range)]

    if(randint(1, 2) == 1): # flipping a coin (horizontal or vertical)
        second_cord = [first_cord[0], first_cord[1] + size - 1]
    else:
        second_cord = [first_cord[0] + size - 1, first_cord[1]]

    battleship = [first_cord, second_cord]

    if(battleship_position_valid(battleships, battleship) == False):
        return generate_random_battleship(battleships, size)

    return battleship

def input_battleship_position(battleships, ship_number, size):
    input_message = ("BATTLESHIP #%d [SIZE: %d]: " % (ship_number, size))

    user_input = get_user_input(input_message)
    check_input_exit(user_input, "EXETING")

    if(user_input.upper() == "RANDOM"):
        battleship = generate_random_battleship(battleships, size)
    else:
        battleship = user_input.split(" ", 1)

        if(len(battleship) != 2):
            return input_battleship_position(battleships, ship_number, size)

        battleship[0] = battleship[0].strip()
        battleship[1] = battleship[1].strip()
        battleship = generate_inputed_battleship(battleships, ship_number, size, battleship)

    return battleship

def decode_board_coordinates(coordinates):
    for index in range(len(coordinates)):
        coordinate = coordinates[index].upper()
        coordinates[index] = decode_board_coordinate(coordinate)
        if(coordinates[index] == None):
            return None
    return coordinates

def decode_board_coordinate(coordinate):
    try:
        letter = coordinate[0].upper()
        h_index = int(string.ascii_uppercase.index(letter))
        w_index = int(coordinate[1:]) - 1
    except:
        return None

    height_valid = (h_index < 10 and h_index >= 0)
    width_valid = (w_index < 10 and w_index >= 0)

    if(height_valid and width_valid):
        return [h_index, w_index]
    return None
##########################################################################
def input_socket_information():
    address = get_user_input("ADDRESS: ")
    check_input_exit(address, "EXCETING ADDRESS")
    try:
        port = int(get_user_input("PORT: "))
    except:
        print("the port must be an integer")
        return input_socket_information()
    return [str(address), str(port)]
    #return ["192.168.1.113", "5555"]

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

def setup_client_information():
    information = input_socket_information()
    address = information[0]; port = int(information[1])
    sock_object = generate_client_socket(address, port)
    if(sock_object == None):
        throw_error_quit("the address or port was wrong")
    return sock_object

def setup_server_information():
    information = input_socket_information()
    address = information[0]; port = int(information[1])
    sock_object = generate_server_socket(address, port)
    if(sock_object == None):
        print("the address or port was wrong")
        return setup_server_information()
    return sock_object

def setup_battleship_information(socket_role):
    sock_object = None
    if(socket_role == "SERVER"):
        sock_object = setup_server_information()
    elif(socket_role == "CLIENT"):
        sock_object = setup_client_information()

    off_board = generate_battleship_board(10, 10)
    if(off_board == None):
        throw_error_quit("OFF BOARD CREATION FAILED")
    def_board = generate_battleship_board(10, 10)
    if(off_board == None):
        throw_error_quit("DEF BOARD CREATION FAILED")
    battleships, def_board = input_battleships_position(def_board)

    # battleships = [[[0, 0], [0, 1]], [[2, 1], [2, 3]], [[4, 3], [4, 5]], [[6, 1], [6, 4]], [[8, 3], [8, 7]]]
    # for index in range(len(battleships)):
    #     all_cords = all_battleship_coordinates(battleships[index])
    #     def_board = board_coordinates_keyword(def_board, all_cords, "BATTLESHIP")

    return sock_object, def_board, off_board, battleships

##########################################################################

def generate_battleship_board(height, width):
    battleship_board = []
    for h_index in range(height):
        battleship_board.append([])
        for w_index in range(width):
            battleship_board[h_index].append("EMPTY")
    return battleship_board

def server_battleship_game(sock_object, def_board, off_board, battleships, defeated, won):
    while(defeated == False and won == False):
        display_battleship_boards(def_board, off_board)
        off_board, won = attack_opponent_coordinate(sock_object, off_board, won)
        if(won == True):
            break
        display_battleship_boards(def_board, off_board)
        def_board, defeated = register_opponents_damage(sock_object, def_board, battleships, defeated)
    return def_board, off_board, defeated, won

def client_battleship_game(sock_object, def_board, off_board, battleships, defeated, won):
    while(defeated == False and won == False):
        display_battleship_boards(def_board, off_board)
        def_board, defeated = register_opponents_damage(sock_object, def_board, battleships, defeated)
        if(defeated == True):
            break
        display_battleship_boards(def_board, off_board)
        off_board, won = attack_opponent_coordinate(sock_object, off_board, won)
    return def_board, off_board, defeated, won

def display_game_result(def_board, off_board, defeated, won):
    display_battleship_boards(def_board, off_board)
    if(defeated):
        print("DEFEATED")
    elif(won):
        print("WON")
    else:
        throw_error_quit("NEITHER WON OR DEFEATED")

def extract_protocol_coordinates(protocol):
    coordinates = protocol.split(":")[1].split("-")
    for index in range(len(coordinates)):
        coordinate = coordinates[index]
        coordinates[index] = decode_coordinate_object(coordinate)
    return coordinates

def decode_coordinate_object(coordinate):
    try:
        decoded = coordinate.split(",")
    except:
        return None

    for index in range(len(decoded)):
        decoded[index] = int(decoded[index])
    return decoded

def encode_coordinate_object(coordinate):
    encoded = ",".join(map(str, coordinate))
    return encoded

def mark_battleship_sunken(board, battleship):
    all_cords = all_battleship_coordinates(battleship)
    board = board_coordinates_keyword(board, all_cords, "SUNKEN")
    return board

def mark_coordinate_hit_miss(off_board, action, coordinate):
    if(action == "HIT"):
        off_board[coordinate[0]][coordinate[1]] = "HIT"
    elif(action == "MISS"):
        off_board[coordinate[0]][coordinate[1]] = "MISS"
    return off_board

def mark_protocol_coordinates(off_board, action, coordinates):
    if(action == "SUNKEN" or action == "DEFEATED"):
        off_board = mark_battleship_sunken(off_board, coordinates)
    else:
        off_board = mark_coordinate_hit_miss(off_board, action, coordinates[0])
    return off_board

######################################################################

def input_attacking_coordinate():
    coordinate = get_user_input("INPUT COORDINATE: ")
    check_input_exit(coordinate, "COORDINATE EXIT")
    coordinate = decode_board_coordinate(coordinate)
    try:
        keyword = off_board[coordinate[0]][coordinate[1]]
        if(keyword == "EMPTY"):
            return coordinate
    except:
        return None

def send_attacking_coordinate(sock_object):
    coordinate = None
    while(coordinate == None):
        coordinate = input_attacking_coordinate()

    encoded = encode_coordinate_object(coordinate)
    if(send_socket_string(sock_object, encoded) == False):
        throw_error_quit("Error while sending attacking coordinate")

def receive_opponents_protocol(sock_object):
    action = None; coordinates = None
    try:
        protocol = sock_object.recv(1024).decode("utf-8")
        action = protocol.split(":")[0]
        coordinates = extract_protocol_coordinates(protocol)
    except:
        throw_error_quit("error while receiving protocol")
    return action, coordinates

def attack_opponent_coordinate(sock_object, off_board, won):
    send_attacking_coordinate(sock_object)
    action, coordinates = receive_opponents_protocol(sock_object)

    if(action == "DEFEATED"):
        won = True;

    off_board = mark_protocol_coordinates(off_board, action, coordinates)
    return off_board, won

def hit_defence_battleship(def_board, battleships, coordinate):
    for index in range(len(battleships)):
        all_cords = all_battleship_coordinates(battleships[index])
        if(coordinate in all_cords):
            return copy(battleships[index])
    return None

###################################################################################################
def receive_opponents_coordinate(sock_object):
    decoded = None
    try:
        coordinate = sock_object.recv(1024).decode("utf-8")
        decoded = decode_coordinate_object(coordinate)
    except:
        throw_error_quit("error while receiving protocol")
    return decoded

def register_opponents_coordinate(def_board, battleships, coordinate):
    if(coordinates_in_battleships(battleships, coordinate)):
        def_board[coordinate[0]][coordinate[1]] = "HIT"
    else:
        def_board[coordinate[0]][coordinate[1]] = "MISS"
    return def_board

def coordinates_in_battleships(battleships, coordinate):
    for ship_index in range(len(battleships)):
        battleship = battleships[ship_index]
        all_cords = all_battleship_coordinates(battleship)
        if(coordinate in all_cords):
            return True
    return False

def battleship_with_coordinate(battleships, coordinate):
    for ship_index in range(len(battleships)):
        battleship = battleships[ship_index]
        all_cords = all_battleship_coordinates(battleship)
        if(coordinate in all_cords):
            return battleship
    return None

def register_opponents_damage(sock_object, def_board, battleships, defeated):
    coordinate = receive_opponents_coordinate(sock_object)
    def_board = register_opponents_coordinate(def_board, battleships, coordinate)
    return send_registerd_damage(sock_object, def_board, battleships, coordinate, defeated)

def send_miss_protocol(sock_object, def_board, defeated, coordinate):
    protocol = generate_socket_protocol("MISS", [coordinate])
    if(send_socket_string(sock_object, protocol) == False):
        throw_error_quit("error while sending protocol")
    return def_board, defeated

def send_hit_protocol(sock_object, def_board, defeated, coordinate):
    protocol = generate_socket_protocol("HIT", [coordinate])
    if(send_socket_string(sock_object, protocol) == False):
        throw_error_quit("error while sending protocol")
    return def_board, defeated

def send_defeated_protocol(sock_object, def_board, defeated, hit_ship):
    protocol = generate_socket_protocol("DEFEATED", hit_ship)
    if(send_socket_string(sock_object, protocol) == False):
        throw_error_quit("error while sending protocol")
    defeated = True; return def_board, defeated

def send_sunken_protocol(sock_object, def_board, defeated, hit_ship):
    protocol = generate_socket_protocol("SUNKEN", hit_ship)
    if(send_socket_string(sock_object, protocol) == False):
        throw_error_quit("error while sending protocol")
    return def_board, defeated

def send_registerd_damage(sock_object, def_board, battleships, coordinate, defeated):
    hit_ship = hit_defence_battleship(def_board, battleships, coordinate)
    if(hit_ship == None):
        return send_miss_protocol(sock_object, def_board, defeated, coordinate)

    if(defence_ship_defeated(def_board, hit_ship) == False):
        return send_hit_protocol(sock_object, def_board, defeated, coordinate)

    def_board = mark_battleship_sunken(def_board, hit_ship)
    if(defence_board_defeated(def_board, battleships) == True):
        return send_defeated_protocol(sock_object, def_board, defeated, hit_ship)

    return send_sunken_protocol(sock_object, def_board, defeated, hit_ship)
###################################################################################################

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
        battleship = battleships[index]
        if(defence_ship_defeated(def_board, battleship) == False):
            return False
    return True

def generate_socket_protocol(action, coordinates):
    protocol_cords = coordinates
    for index, coordinate in enumerate(protocol_cords):
        protocol_cords[index] = ",".join(map(str, coordinate))
    coordinates = "-".join(coordinates)
    protocol = ":".join([action, coordinates])
    return protocol

display_numbers = "  1 2 3 4 5 6 7 8 9 10"

def display_battleship_boards(def_board, off_board):
    terminal.system("clear")
    print("%s\t%s" % (display_numbers, display_numbers))
    for h_index in range(len(def_board)):
        display_board_width(def_board, h_index)
        print("\t", end="")
        display_board_width(off_board, h_index)
        print()
    return True

def display_board_width(board, h_index):
    print(string.ascii_uppercase[h_index], end=" ")
    for w_index in range(len(board[h_index])):
        keyword = board[h_index][w_index]
        marker = convert_keyword_marker(keyword)
        print(marker, end=" ")

def display_battleship_board(board):
    terminal.system("clear")
    print("%s" % display_numbers)
    for h_index in range(len(board)):
        display_board_width(board, h_index)
        print()
    return True

def convert_keyword_marker(string):
    for index in range(len(markers)):
        if(string == markers[index][0]):
            return markers[index][1]
    return None

def generate_keyword_markers(filename):
    file_lines = None; markers = []
    with open(filename, "r") as file_object:
        file_lines = file_object.read().splitlines()
    for index in range(len(file_lines)):
        markers.append(file_lines[index].strip().split("=", 1))
    return markers

def extract_socket_role(arguments):
    try:
        socket_role = str(arguments[1]).upper()
    except:
        throw_error_quit("TO FEW ARGUMENTS")

    if(socket_role == "SERVER" or socket_role == "CLIENT"):
        return socket_role

    throw_error_quit("EITHER SERVER OR CLIENT")

if(__name__ == "__main__"):
    markers = generate_keyword_markers("markers.txt")
    socket_role = extract_socket_role(system.argv)
    defeated = False; won = False

    sock_object, def_board, off_board, battleships = setup_battleship_information(socket_role)

    if(socket_role == "SERVER"):
        def_board, off_board, defeated, won = server_battleship_game(sock_object, def_board, off_board, battleships, defeated, won)
    elif(socket_role == "CLIENT"):
        def_board, off_board, defeated, won = client_battleship_game(sock_object, def_board, off_board, battleships, defeated, won)

    display_game_result(def_board, off_board, defeated, won)
