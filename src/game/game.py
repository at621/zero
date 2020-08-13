import chess.pgn
import numpy as np
import copy
import chess
import other.library as lib
import onnxruntime
from IPython.display import display, HTML, clear_output
import time
from logging import getLogger

logger = getLogger('main.game')

finalDict, enumDict = lib.createMoveDict()


class Game:
    """
    Represents a chess environment where a chess game is played/
    """

    def __init__(self, player1=None, player2=None, game=None):
        self.board = game 
        self.num_halfmoves = 0
        self.result = None
        self.white_to_move = 1
        self.finished = False
        self.Player1 = player1
        self.Player2 = player2
        self.enumDict = self.createMoveDict()

    def createMoveDict(self):
        kala, enumDict = lib.createMoveDict()
        return enumDict

    def step(self, move):
        kala = chess.Move.from_uci(str(move))
        self.board.push(kala)
        self.num_halfmoves += 1
        self.white_to_move = 1 - self.white_to_move

    def game_over(self):
        self.finished = self.board.is_game_over()
        self.result = self.board.result()

    def display_pgn(self):
        pgn = chess.pgn.Game.from_board(self.board)
        print(pgn)

    def display_board(self, board):
        return board._repr_svg_()

    def display_game(self, value):
        board_stop = self.display_board(self.board)
        html = "<b>Move %s, Value: %s </b><br/>%s" % (
            len(self.board.move_stack), value, board_stop)
        # time.sleep(0.5)
        clear_output(wait=True)
        display(HTML(html))

    def save_pics(self):
        boardsvg = chess.svg.board(self.board)
        fileName = 'Move_' + str(self.num_halfmoves) + '.svg'
        with open(fileName, 'w') as writer:
            writer.write(boardsvg)
    
    def play_game(self):
        while not self.finished:
            fen = self.board.fen()
            if self.white_to_move:
                move, value = self.Player1.makeMove(fen, enumDict)
            else:
                move, value = self.Player2.makeMove(fen, enumDict) #todo

            self.step(move)
            self.game_over()
            self.display_game(value)
            # self.save_pics()
            
        self.display_pgn()

