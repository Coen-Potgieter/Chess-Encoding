import chess
import math
import chess.pgn
import io
import json


def print_bin(bin_num):
    return str(bin(bin_num))[2:]


def legal_moves_from_given_board_config(board, fen):
    board.set_fen(fen)
    print(board)


def read_x_bits(bits, x):

    mask = (0b1 << x) - 1
    return bits >> x, bits & mask


def save_game_for_bots(encoded_moves):
    json_to_save = {}
    for game_idx, game in enumerate(encoded_moves):

        white_moves = []
        black_moves = []

        for idx, move in enumerate(game):
            if idx % 2 == 0:
                white_moves.append(move)
            else:
                black_moves.append(move)

        json_to_save[f"Game {game_idx + 1}"] = {
            "white": white_moves,
            "black": black_moves
        }

    with open("src/data/predefinedMoves/message1.json", "w") as tf:
        json.dump(json_to_save, tf, indent=4)


def encode_chess_game(bits):
    print("Encoding: ", print_bin(bits), "\n")

    # init a board, from starting pos
    board = chess.Board()

    # create a list to store game in uci moves
    encoded_game = []
    # create a list to hold all the encoded games (in case multiple games are needed to encode a message)
    games = []
    while bits > 0:
        # get all legal moves from given board config
        legal_moves = [move.uci() for move in list(board.legal_moves)]

        # get number of legal moves (-1 for legal indices)
        num_moves = len(legal_moves) - 1
        
        # If less than two available moves, then new game since we need at least 2 moves to encode binary 1 or 0
        if num_moves <= 1:
            board = chess.Board()
            games.append(encoded_game)
            encoded_game = []
            continue

        # number of bits a given move in this position can store
        num_bits = math.floor(math.log2(num_moves))
        print("Number of bits to extract: ", num_bits)

        # Extract this bits from our bits to encode
        bits, info_for_move = read_x_bits(bits, num_bits)

        print("Extracted bits: ", print_bin(info_for_move))
        print("Leaving us with: ", print_bin(bits))

        # choose move that corresponds with extracted info
        move_to_play = legal_moves[info_for_move]
        print("Thus, from the legal moves: ", legal_moves)
        print("We choose move: ", move_to_play)

        # append our game
        encoded_game.append(move_to_play)

        # Play the move
        board.push_uci(move_to_play)
        print(board, "\n")
    
    games.append(encoded_game)
    return games


def decode_chess_game(pgn):

    # Read pgn and get game board
    pgn_io = io.StringIO(pgn)
    game = chess.pgn.read_game(pgn_io)
    board = game.board()

    # get played moves in UCI format
    played_moves = []
    for move in game.mainline_moves():
        played_moves.append(move.uci())

    # Then play out this game recording the bits using the same encoding scheme
    #   as before

    num_moves = len(played_moves)
    move_idx = 0
    bin_packets = []

    while move_idx < num_moves:
        # Extract the move played
        move_played = played_moves[move_idx]

        # get all legal moves from given board config in list of uci moves
        legal_moves = [move.uci() for move in list(board.legal_moves)]
        num_legal_moves = len(legal_moves) - 1
        # number of bits we are going to decode
        num_bits = math.floor(math.log2(num_legal_moves))

        info_from_move = str(bin(legal_moves.index(move_played)))[2:]
        num_missing_0s = num_bits - len(info_from_move)
        for _ in range(num_missing_0s):
            print("Appending")
            info_from_move = "0" + info_from_move

        bin_packets.append(info_from_move)

        # play uci move on board to get next board config
        board.push_uci(move_played)
        move_idx += 1
        print(board, "\n")

    # now take our packets and reverse to construct original binary
    bin_packets.reverse()
    decoded_bits = int("".join(bin_packets), 2)

    return decoded_bits


# Returns binary number
def my_string_encryption(input_string):
    bit_packets = []
    for char in input_string:
        string_representation = str(bin(ord(char)))[2:]
        if len(string_representation) < 8:
            for _ in range(8 - len(string_representation)):
                string_representation = "0" + string_representation
        bit_packets.append(string_representation)

    bin_as_string = "".join(bit_packets)
    encrypted_bin = int(bin_as_string, 2)

    return encrypted_bin


# input must a binary number (example: `0b0101001`)
def my_string_decrypt(bits):

    message = ""
    # start with least bytes
    while bits > 0:
        target_bin = bits & 0b11111111
        message = chr(target_bin) + message
        bits = bits >> 8

    return message


def bin_to_string(binary_string):
    # Remove the '0b' prefix if it exists
    if binary_string.startswith('0b'):
        binary_string = binary_string[2:]

    # Split the binary string into chunks of 8 bits
    byte_chunks = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]

    # Convert each 8-bit chunk to its corresponding ASCII character
    characters = [chr(int(byte, 2)) for byte in byte_chunks]

    # Join all the characters to form the original string
    original_string = ''.join(characters)

    return original_string


def main():

    binary_message = my_string_encryption("Hello World!")

    games = encode_chess_game(binary_message)
    save_game_for_bots(games)
    return
    with open("src/data/PlayedGames/game1.pgn", "r") as tf:
        pgn = tf.read()
    bits = decode_chess_game(pgn)
    print(my_string_decrypt(bits))
    return


if __name__ == "__main__":
    main()
