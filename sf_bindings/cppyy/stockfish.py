import cppyy

def replace_getstr(klass, name):
    try:
        klass.__str__ = klass.__dict__['get_str']
    except KeyError:
        pass

cppyy.py.add_pythonization(replace_getstr, 'UCI')

cppyy.include('./main.hpp')
cppyy.load_library('stock.dll')

from cppyy.gbl import engine_info, UCI, Tune, PSQT, Bitboards, \
    Position, Bitbases, Endgames, Threads, Search, Options, std, \
    StateListPtr, StateInfo, generate, MAX_MOVES, ExtMove, \
    MoveList, LEGAL, MoveList_LEGAL
from cppyy.gbl.UCI import Option

class Moves(object):

    def __init__(self, movelist):
        self.movelist = movelist
        
    def __iter__(self):
        self.idx = -1
        self.end = self.movelist.size()
        return self
    
    def __next__(self):
        self.idx += 1
        if self.idx not in range(self.end):
            raise StopIteration

        return self.movelist.item(self.idx)

    def __del__(self):
        del self.movelist
        
class Stockfish(object):

    def __init__(self):
        UCI.init(Options)
        Tune.init()
        PSQT.init()
        Bitboards.init()
        Position.init()
        Bitbases.init()
        Endgames.init()
        Threads.set(int(Options['Threads'].__float__()))
        Search.clear()

        self.pos = Position()
        for name,val in Options:
            print(name, val)
        
    def __del__(self):
        del self.pos
        Threads.set(0)

    def position(self, position_str):
        #UCI.loop_next('position '+cmd)
        UCI.set_position(self.pos, position_str)

    def is_chess960(self):
        return self.pos.is_chess960()
    
    def legal_moves(self):
        return Moves(MoveList_LEGAL(self.pos))

    def legal_moves_str(self):
        is_chess960 = self.is_chess960()
        return [UCI.move(m.move, is_chess960) for m in self.legal_moves()]
