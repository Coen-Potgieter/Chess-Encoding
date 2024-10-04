import chess
import math
import chess.pgn
import io

def legal_moves_from_give_board_config(board, fen):
    board.set_fen(fen)
    print(board)


def read_x_bits(bits, x):

    mask = (0b1 << x) - 1
    return bits >> x, bits & mask


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

    with open("game1.pgn", "r") as tf:
        pgn = tf.read()

    decode_chess_game(pgn)
    return
    # legal_moves_from_give_board_config(board, "r1bqkbnr/ppp2ppp/2n5/4p3/3P1B2/2N2N2/PPP1Q1PP/R3KB1R b KQkq - 0 1")
    game = encode_chess_game(101011100)
    print(game)
    bits = 0b111101
    
    # legal_moves = list(board.legal_moves)
    # print(legal_moves)


if __name__ == "__main__":
    main()
