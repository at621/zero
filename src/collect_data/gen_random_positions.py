import chess
import random
from tqdm import tqdm
import pyodbc
import other.library as lib


def createLastPositions(num):
    gamenum = 0

    list = []
    for _ in tqdm(range(100_000), mininterval=100):
        board = chess.Board()
        while not board.is_game_over():
            moves = random.choice([move for move in board.legal_moves])
            move = moves.uci()
            board.push_uci(move)

            if board.is_game_over() and board.result() in ['1-0', '0-1']:
                gamenum += 1
                result = board.result()
                board.pop()
                MoveTensorBinary = bytes(lib.convertMove(str(move)))
                FenTensorBinary = bytes(lib.fenToTensor(board.fen()))
                ResultTensor = lib.finalResult(result)
                list.append([gamenum, board.fullmove_number, board.fen(
                ), result, move, 'RandomEndGame', MoveTensorBinary, FenTensorBinary, ResultTensor])
                break

    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=TOWER-BRIDGE;'
                          'Database=chess;'
                          'Trusted_Connection=yes;')

    cursor = conn.cursor()
    sql = "INSERT INTO chess.dbo.games (GameNum, MoveNum, Fen, Result, NextMove, Algo,MoveTensorBinary, FenTensorBinary, ResultTensor) VALUES(?,?,?,?,?,?,?,?,?)"

    cursor.executemany(sql, list)
    conn.commit()
    conn.close()
