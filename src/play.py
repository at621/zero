from game.game import Game
from game.player import Player
import time
import onnxruntime
import chess
import logging.config
from logging import getLogger

logging.config.fileConfig('config//logging.conf')
logger = logging.getLogger('main')

startBoard = chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

t0 = time.time()
for i in range(1):
    white = Player(ai=True)
    black = Player(ai=False)
    game = Game(white, black, startBoard)
    game.play_game()
t1 = time.time()

total_n = t1-t0
print("Cumulative time:", total_n)
