import argparse
import sys

import sf_chess as sf


START_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'


def parse_args():
    '''
    Parse command line arguments.
    The only argument is a FEN string. It is up to the user to ensure that the FEN string is valid.
    If the FEN string isn't provided the chess starting position is used by default.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-fen',
        default=START_FEN,
        required=False,
        help='A FEN string defining a chess position enclosed in quotes'
    )
    return parser.parse_args()


def legal_moves(fen):
    '''
    Print all of the legal moves for the given position.
    '''
    sf._init()
    pos = sf.SFPosition(fen)

    print('pos = {}'.format(pos.fen()))

    legal_moves = pos.legal_moves()

    for move in legal_moves:
        print(move)


if __name__ == '__main__':
    fen = parse_args()
    legal_moves(fen.fen)

    sys.exit(0)

