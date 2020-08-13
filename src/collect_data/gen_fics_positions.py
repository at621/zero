import glob
import chess
from logging import getLogger
from os import getpid
import chess.pgn
import numpy as np
import pyodbc
import other.library as lib

logger = getLogger('createGames.fics')


def getFicsPositions(file):
    logger.info('Started process: %s', getpid())
    pgn = open(file)
    games = []
    i = 0
    while True:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break
        games.append(game)
        i = i+1
        if i % 10000 == 0:
            logger.info('Process %s processed %s games', getpid(), i)

    logger.info('Process %s collected %s games', getpid(), len(games))

    listGames = []
    for gameNum, game in enumerate(games):
        board = game.board()
        winlose = game.headers["Result"]

        for move in game.mainline_moves():
            board.push(move)
            fen = board.fen()
            MoveTensorBinary = bytes(lib.convertMove(str(move)))
            FenTensorBinary = bytes(lib.fenToTensor(fen))
            ResultTensor = lib.finalResult(winlose)

            # Store the result
            listGames.append([gameNum, board.fullmove_number, fen, winlose, str(move), 'FicsGames',
                              MoveTensorBinary, FenTensorBinary, ResultTensor])

        if (gameNum+1) % 5000 == 0:
            logger.info('Process %s has moves for %s games', getpid(), gameNum)

            conn = pyodbc.connect('Driver={SQL Server};'
                                  'Server=TOWER-BRIDGE;'
                                  'Database=chess;'
                                  'Trusted_Connection=yes;')
            cursor = conn.cursor()

            sql = "INSERT INTO chess.dbo.games (GameNum, MoveNum, Fen, Result, NextMove, Algo,MoveTensorBinary, FenTensorBinary, ResultTensor) VALUES(?,?,?,?,?,?,?,?,?)"

            cursor.executemany(sql, listGames)
            conn.commit()
            conn.close()
            listGames = []
            logger.info('Finished inserting results: %s', getpid())

    logger.info('Process %s has finished', getpid())

    return 1
