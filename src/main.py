import chess
import math

def legal_moves_from_give_board_config(board, fen):
    board.set_fen(fen)
    print(board)


def read_x_bits(bits, x):

    mask = (0b1 << x) - 1
    return bits >> x, bits & mask


def encode_chess_game(bits):
    board = chess.Board()
    legal_moves = list(board.legal_moves)

    num_moves = len(legal_moves)

    num_bits = math.log2(num_moves)

    print(bits)
    
    # return
    board.push(legal_moves[0])
    print(board)
    pass

def main():

    # legal_moves_from_give_board_config(board, "r1bqkbnr/ppp2ppp/2n5/4p3/3P1B2/2N2N2/PPP1Q1PP/R3KB1R b KQkq - 0 1")
    encode_chess_game(101011100)
    bits = 0b111101

    bits, read_bits = read_x_bits(bits, 2)
    print(f"{bin(bits)}")
    print(f"{bin(read_bits)}")
    
    # legal_moves = list(board.legal_moves)
    # print(legal_moves)


if __name__ == "__main__":
    main()
