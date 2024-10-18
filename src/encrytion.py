import chess
import math
import chess.pgn
import io
import json


def bin_as_string(bin_num):
    return str(bin(bin_num))[2:]


def legal_moves_from_given_board_config(board, fen):
    board.set_fen(fen)
    print(board)


def read_x_bits(bits, x):

    mask = (0b1 << x) - 1
    return bits >> x, bits & mask


def save_game_for_bots(encoded_moves):
    white_moves = []
    black_moves = []

    for idx, move in enumerate(encoded_moves):
        if idx % 2 == 0:
            white_moves.append(move)
        else:
            black_moves.append(move)

    json_to_save = {
        "white": white_moves,
        "black": black_moves
    }
    with open("src/data/predefinedMoves/game1.json", "w") as tf:
        json.dump(json_to_save, tf, indent=4)


def encode_chess_game(bits):
    print("Encoding: ", bin_as_string(bits), "\n")

    # init a board, from starting pos
    board = chess.Board()
    # create a list to store game in uci moves
    encoded_game = []
    # print(str(bits))
    # return
    while bits > 0:
        # get all legal moves from given board config
        legal_moves = [move.uci() for move in list(board.legal_moves)]

        # get number of legal moves (-1 for legal indices)
        num_moves = len(legal_moves) - 1

        # number of bits a given move in this position can store
        num_bits = math.floor(math.log2(num_moves))
        print("Number of bits to extract: ", num_bits)

        # Extract this bits from our bits to encode
        bits, info_for_move = read_x_bits(bits, num_bits)

        print("Extracted bits: ", bin_as_string(info_for_move))
        print("Leaving us with: ", bin_as_string(bits))

        # choose move that corresponds with extracted info
        move_to_play = legal_moves[info_for_move]
        print("Thus, from the legal moves: ", legal_moves)
        print("We choose move: ", move_to_play)

        # append our game
        encoded_game.append(move_to_play)

        # Play the move
        board.push_uci(move_to_play)
        print(board, "\n")

    return encoded_game



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

        print(num_bits)
        print(info_from_move)
        num_missing_0s = num_bits - len(info_from_move)
        for _ in range(num_missing_0s):
            print("Appending")
            info_from_move = "0" + info_from_move

        bin_packets.append(info_from_move)

        # play uci move on board to get next board config
        board.push_uci(move_played)
        move_idx += 1
        print(board, "\n")

    # now take our packets and construct original binary
    
    print(bin_packets)
    bin_packets.reverse()
    decoded_bits = int("".join(bin_packets), 2)
    print(bin_as_string(decoded_bits))


def string_to_bin(input_string):

    # This converts our string into a class `bytes`. This class is
    #   immutable, indexable and iterable
    byte_array = input_string.encode("utf-8")

    binary_string = ''.join(format(byte, '08b') for byte in byte_array)

    return binary_string

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
    bin_mssg = string_to_bin("Hello World")
    print(bin_mssg)
    print(bin_to_string(str(bin_mssg)))
    return
    # for i in range(1):
    #     print(i)
    # return
    # game = encode_chess_game(0b101011100)
    # save_game_for_bots(game)
    # return
    with open("src/data/PlayedGames/game1.pgn", "r") as tf:
        pgn = tf.read()
    decode_chess_game(pgn)
    return
    # decode_chess_game(pgn)
    # return

    save_game_to_json(game)

    # legal_moves = list(board.legal_moves)
    # print(legal_moves)


if __name__ == "__main__":
    main()
