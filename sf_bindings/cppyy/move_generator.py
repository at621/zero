from datetime import datetime
from stockfish import UCI, Stockfish

s = Stockfish()

LOOP_COUNT = 1000000
POSITION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

start = datetime.now()
for i in range(LOOP_COUNT):
    print(f'LEGAL Iteration {i}')
    s.position(POSITION)

    #for m in s.legal_moves():
    #    print(UCI.move(m.move, s.is_chess960()), end=' ')

    print(f'LEGAL : {s.legal_moves_str()}')

end = datetime.now()

print(f'List of legal moves for position({POSITION}) : {s.legal_moves_str()}')

print(f'Time taken for {LOOP_COUNT} iterations: {end-start}')
