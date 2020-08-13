from collections import defaultdict
import random
import chess
from game.game import Game
import other.library as lib
from pathlib import WindowsPath
from enum import Enum
import numpy as np
from logging import getLogger
from pathlib import Path
import onnxruntime
import chess.engine

logger = getLogger('main.mcts')

finalDict, enumDict = lib.createMoveDict()
onnxModel = '..//models//model_v1.onnx'
session = onnxruntime.InferenceSession(onnxModel, None)


class MctsTree:
    """
    The node that stores move and state information required for MCTS
    """

    def __init__(self, session2, fen, prior_prob=0, move=None, parent=None, board_value=None,    old_value=0):
        self.fen = fen  # chess.Board(fen)
        self.children = []
        self.session2 = session2
        self.parent = parent
        self.move = move
        self.old_value = old_value
        self.bestMove = None

        self.white_to_move = self.whoMoves()

        self.prior_prob = prior_prob
        self.board_value = board_value
        self.terminal_node_value = 0
        self.num_visits = 0
        self.total_value = 1 * -self.white_to_move
        self.mean_value = self.total_value / (self.num_visits + 1)
        self.adjust_value = (self.mean_value + (1.5 * self.prior_prob *
                            np.sqrt(self.num_visits + 1) / (1 + self.num_visits)))

    def __repr__(self):
        s0 = str(self.move)
        s1 = str(self.prior_prob)
        s2 = str(self.num_visits)
        s3 = str(self.adjust_value)
        s4 = str(self.terminal_node_value)
        s5 = str(self.total_value)
        s6 = str(self.board_value)
        s7 = str(self.mean_value)
        return 'Move: '+s0+', prior_prob: '+s1+', num_visits: '+s2 + \
            ', adjust_value: '+s3+', terminal_node_value: '+s4 + \
            ', total_value: '+s5 + ', board_value: '+s6 +\
            ', mean_value: '+s7

    def whoMoves(self):
        splits = self.fen.split()
        if splits[1] == "b":
            who = -1
        else:
            who = 1
        return who

    def calcValue(self, terminal_node_value=0):
        self.terminal_node_value = terminal_node_value
        self.num_visits += 1
        self.total_value = terminal_node_value + self.total_value
        self.mean_value = self.total_value / self.num_visits

        add_on = (1.5 * self.prior_prob *
                  np.sqrt(self.num_visits + 1) / (1 + self.num_visits)) * self.white_to_move
        self.adjust_value = (self.mean_value + add_on * self.white_to_move)

    def addChildren(self, parent, enumDict):
        board = chess.Board(self.fen)
        moves = [str(x) for x in list(board.legal_moves)]

        gameState = lib.fenToTensor(self.fen)
        inputState = np.expand_dims(gameState, axis=0)
        inputState = inputState.astype(np.float32)

        input_name = session.get_inputs()[0].name
        output_1 = session.get_outputs()[0].name
        output_2 = session.get_outputs()[1].name

        policy, value = session.run([output_1, output_2], {
                                    input_name: inputState})
        values = {move: policy[0][enumDict[move].value] for move in moves}

        self.board_value = value
        self.old_value = value

        for move in values.keys():
            brd = chess.Board(self.fen)
            brd.push(chess.Move.from_uci(move))
            prior_probability = values[move]
            node = MctsTree(session2=1, fen=brd.fen(),
                            prior_prob=prior_probability, move=move,
                            parent=parent, board_value=0)
            node.calcValue()
            node.num_visits = node.num_visits-1
            self.children.append(node)
