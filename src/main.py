import chess
import math
import chess.pgn
import io
import json

def legal_moves_from_give_board_config(board, fen):
    board.set_fen(fen)
    print(board)


def read_x_bits(bits, x):

    mask = (0b1 << x) - 1
    return bits >> x, bits & mask


def save_game_to_json(encoded_moves):

    with open("src/data/predefinedMoves/game1.json", "w") as tf:
        json.dump(encoded_moves, tf)


def encode_chess_game(bits):

    # init a board, from starting pos
    board = chess.Board()
    # create a list to store game in uci moves
    encoded_game = []
    while bits > 0:
        # get all legal moves from given board config
        legal_moves = list(board.legal_moves)

        # get number of leagl moves
        num_moves = len(legal_moves)

        # number of bits a given move in this position can store
        num_bits = math.floor(math.log2(num_moves))

        # Extract this bits from our bits to encode
        bits, info_for_move = read_x_bits(bits, num_bits)

        # choose move that corresponds with extarcted info
        move_to_play = legal_moves[info_for_move]

        # append our game converting move to string using `.uci()`
        encoded_game.append(move_to_play.uci())

        # Play the move
        board.push(move_to_play)

        print(board, "\n")

    return encoded_game


def decode_chess_game(pgn):
    pgn_io = io.StringIO(pgn)
    game = chess.pgn.read_game(pgn_io)
    board = game.board()
    for move in game.mainline_moves():
        board.push(move)
        print(board, "\n")
    return board


def main():

    # with open("game1.pgn", "r") as tf:
    #     pgn = tf.read()

    # decode_chess_game(pgn)
    # return

    game = encode_chess_game(101011100)
    print(game)
    save_game_to_json(game)
    
    # legal_moves = list(board.legal_moves)
    # print(legal_moves)


if __name__ == "__main__":
    main()
