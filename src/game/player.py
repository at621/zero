from logging import getLogger
import chess
import numpy as np
import random
from pathlib import WindowsPath
import other.library as lib
from enum import Enum
from game.mcts import MctsTree
import onnxruntime
import pickle

logger = getLogger('main.player')


class Player:
    """
    Plays the actual game of chess, choosing moves based on policy and value network predictions
    """

    def __init__(self, ai=False):
        self.ai = ai
        self.moves = []

    def createNodes(self, fen, enumDict):
        root = MctsTree(12, fen)
        root.addChildren(root, enumDict)
        return root

    def mtscMove(self, fen, enumDict):
        for i in range(10000):
            if i == 0:
                node = self.createNodes(fen, enumDict)

            finished, result = self.game_over(node.fen)

            if finished:  # recursion to the top, update values based on result
                terminal_node_value = result # replace with the actual result
                node = self.update_values(
                    node, terminal_node_value)

            elif not node.children:  # Spawn a child and recursion to the top
                node.addChildren(node, enumDict)
                terminal_node_value = node.board_value
                node = self.update_values(node, terminal_node_value)

            else:  # pick a child and go deeper
                node = self.next_step(node)

        terminal_node_value = node.board_value
        node = self.update_values(node, terminal_node_value)
        move = self.returnBestMove(node.children)
        value = node.mean_value

        return move, value

    def game_over(self, fen):  # place all your conditions here
        board = chess.Board(fen)
        finished = board.is_game_over()
        result = self.finalResult(board.result())
        # add actual outcome
        return finished, result

    def finalResult(self, result):
        outcomes = {'0-1': -1, '1-0': 2, '1/2-1/2': 0.5, '*':1000}
        win = outcomes[result]
        return win

    def next_step(self, node):
        best_value = -np.inf if node.white_to_move==1 else np.inf
        for child in node.children:            
            if node.white_to_move == 1: 
                value = child.adjust_value           
                if value > best_value:
                    best_value = value
                    best_node = child
            elif node.white_to_move == -1:
                value = child.adjust_value
                if value < best_value:
                    best_value = value
                    best_node = child
        node.bestMove = best_node.move
        return best_node


    def randomChoice(self, node):
        probs = [child.adjust_value+1 for child in node.children]
        probs = np.array(probs)
        probs /= probs.sum()
        node = np.random.choice(node.children, p=probs)
        best_node = node
        return best_node

    def returnBestMove(self, children):
        maxVisits = 0 
        for child in children:
            a = child.num_visits                       
            if a > maxVisits:
                maxVisits = a
                best_move = child.move  
        return best_move   


    def update_values(self, node, terminal_node_value):  # recursion
        if node.parent:
            node.calcValue(terminal_node_value)
            parent = node.parent
            parent.calcValue(terminal_node_value)
            return(self.update_values(parent, terminal_node_value))
        else:
            return node

    def moveSimple(self, fen, enumDict):  # Create legitimate moves and pick one
        board = chess.Board(fen)
        moves = list(board.legal_moves)
        move = random.choice(moves)
        self.moves.append(move)
        value = np.nan

        return move, value

    def makeMove(self, fen, enumDict):
        if self.ai:
            move, value = self.mtscMove(fen, enumDict)
        else:
            move, value = self.moveSimple(fen, enumDict)

        return move, value