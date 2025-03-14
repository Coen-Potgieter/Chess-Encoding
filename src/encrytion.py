import chess
import math
import chess.pgn
import io
import json
import os


def legal_moves_from_given_board_config(board, fen):
    board.set_fen(fen)
    print(board)


def save_game_for_bots(encoded_moves, path_to_save):
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

    with open(path_to_save, "w") as tf:
        json.dump(json_to_save, tf, indent=4)


# Encodes a string variable of bits
def encode_chess_game(bits):

    print("Encoding: ", bits, "\n")

    # init a board, from starting pos
    board = chess.Board()

    # create a list to store game in uci moves
    encoded_game = []
    # create a list to hold all the encoded games (in case multiple games are needed to encode a message)
    games = []
    while len(bits) > 0:
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
        
        info_for_move = bits[:num_bits]
        bits = bits[num_bits:]

        print("Extracted bits: ", info_for_move)
        print("Leaving us with: ", bits)

        # choose move that corresponds with extracted info
        move_to_play = legal_moves[int(info_for_move, 2)]
        print("Thus, from the legal moves: ", legal_moves)
        print("We choose move: ", move_to_play)

        # append our game
        encoded_game.append(move_to_play)

        # Play the move
        board.push_uci(move_to_play)
        print(board, "\n")
    
    games.append(encoded_game)
    return games


def decode_single_chess_game(pgn, quiet=False):

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

        # Use idx of possible moves and move played to figure out bits
        info_from_move = str(bin(legal_moves.index(move_played)))[2:]
        # Ensure we keep bit length in tact by pre-padding with 0s
        num_missing_0s = num_bits - len(info_from_move)
        for _ in range(num_missing_0s):

            if not quiet:
                print("Pre-padding")
            info_from_move = "0" + info_from_move

        bin_packets.append(info_from_move)

        # play uci move on board to get next board config
        board.push_uci(move_played)
        move_idx += 1
        if not quiet:
            print(board, "\n")

    decoded_bits = "".join(bin_packets)

    return decoded_bits


# Converts a string message into binary numbers as a string type
def secret_to_bin(secret_mssg):
    bin_representation = ""
    for char in secret_mssg:
        # ASCII conversion always has leading dead bit of 0, python trims this off
        #   so I am fixing the format here to ensure that the 0 shows in the string
        # Note the indexing of temp_repr to skim off the "0b" at the start
        temp_repr = str(bin(ord(char)))[2:]
        
        # Pre-pad string with needed 0s to ensure 8 bit-width (Also note dead but is 1)
        needed_0s = 8 - len(temp_repr)
        proper_repr = "1"
        for _ in range(needed_0s - 1):
            proper_repr += "0"
        proper_repr += temp_repr
        bin_representation += proper_repr

    return bin_representation


# Converts binary number of string type and converts it to out secret message text
def bin_to_secret(bin_secret):

    running_secret = ""
    # Break up into 8 bit packets and convert using ascii
    num_chars = int(len(bin_secret) / 8)
    for _ in range(num_chars):
        # Pop first byte and leave remaining bytes
        popped_byte = bin_secret[:8]
        bin_secret =  bin_secret[8:]
        
        # Change first bit back to `0` and change to binary number
        popped_byte = "0" + popped_byte[1:]
        decoded_char = chr(int(popped_byte, 2))
        running_secret += decoded_char
    return running_secret


# Takes in path to a directory and converts `secret.txt` file to a chess game and saves the games
def encode_secret(path_to_dir):
    
    files = os.listdir(path_to_dir)
    if "secret.txt" not in files:
        print("Valid file to encode not found | target file must `secret.txt`")
        raise
        
    # Convert Secret to bits
    with open(path_to_dir + "/secret.txt", "r") as tf:
        secret_string = tf.read()
    bin_secret = secret_to_bin(secret_string)   

    # Convert bits string to a chess game
    games = encode_chess_game(bin_secret) 
    save_game_for_bots(games, path_to_save=path_to_dir + "/predefined-moves/moves.json")


def decode_pgns(dir_path):
    
    pgn_dir_path = dir_path + "/played-games"
    pgn_files = []
    for filename in os.listdir(pgn_dir_path):
        pgn_files.append(filename)

    pgn_files.remove("ids.json")

    # This line is from chatGPT
    pgn_files = sorted(pgn_files, key=lambda x: int(x.split('-')[1].split('.')[0]))

    running_bits = "";
    for game_dir in pgn_files:
        with open(f"{pgn_dir_path}/{game_dir}", "r") as tf:
            pgn = tf.read()

        print("Decoding " + game_dir)
        decoded_bits = decode_single_chess_game(pgn, quiet=True)
        running_bits += decoded_bits

    with open(dir_path + "/outp.txt", "w") as tf:
        original_message = bin_to_secret(running_bits)
        tf.write(original_message)


def main():
    
    # encode_secret("src/data/test3")
    decode_pgns("src/data/test3")

if __name__ == "__main__":
    main()


