import random
import numpy as np
import math

MOVES = ['up', 'down', 'left', 'right']

# — konwersje wartość↔wykładnik↔kod
def encode_row_from_value(row):
    exps = [(0 if v==0 else int(math.log2(v))) for v in row]
    code = 0
    for i,e in enumerate(exps):
        code |= (e << (4*i))
    return code

def decode_row_to_value(code):
    vals = []
    for i in range(4):
        e = (code >> (4*i)) & 0xF
        vals.append(0 if e==0 else 2**e)
    return vals

# — precompute wszystkich 2^16 możliwych wierszy (kodowanych wykładnikami)
def _move_row_exps(exps):
    res = [e for e in exps if e!=0]
    score = 0
    i=0
    while i < len(res)-1:
        if res[i]==res[i+1]:
            res[i] += 1
            score += 2**res[i]
            res.pop(i+1)
            i+=1
        i+=1
    return res + [0]*(4-len(res)), score

def precompute_row_transforms():
    ROW_CACHE   = {}
    SCORE_CACHE = {}
    for code in range(1<<16):
        exps = [(code >> (4*i)) & 0xF for i in range(4)]
        moved, sc = _move_row_exps(exps)
        new_code = 0
        for i,e in enumerate(moved):
            new_code |= (e << (4*i))
        ROW_CACHE[code]   = new_code
        SCORE_CACHE[code] = sc
    return ROW_CACHE, SCORE_CACHE

ROW_CACHE, SCORE_CACHE = precompute_row_transforms()

# — ruchy na cache
def move_left_cached(board):
    newb  = np.zeros((4,4), dtype=int)
    total = 0
    for i in range(4):
        row = board[i]
        code = encode_row_from_value(row)
        new_code = ROW_CACHE[code]
        total   += SCORE_CACHE[code]
        newb[i]  = decode_row_to_value(new_code)
    return newb, total

def move_right_cached(board):
    newb, total = move_left_cached(board[:, ::-1])
    return newb[:, ::-1], total

def move_up_cached(board):
    newb, total = move_left_cached(board.T)
    return newb.T, total

def move_down_cached(board):
    newb, total = move_right_cached(board.T)
    return newb.T, total

# — klasa gry
class Game2048:
    def __init__(self):
        self.reset()

    def copy(self):
        g = Game2048()
        g.board = self.board.copy()
        return g

    def reset(self):
        self.board = np.zeros((4,4), dtype=int)
        self.add_random_tile()
        self.add_random_tile()
        return self.board

    def add_random_tile(self):
        empties = list(zip(*np.where(self.board==0)))
        if not empties: return
        x,y = random.choice(empties)
        self.board[x,y] = 2 if random.random()<0.9 else 4

    def move(self, direction):
        orig = self.board.copy()
        if   direction=='left':  self.board = move_left_cached(self.board)[0]
        elif direction=='right': self.board = move_right_cached(self.board)[0]
        elif direction=='up':    self.board = move_up_cached(self.board)[0]
        elif direction=='down':  self.board = move_down_cached(self.board)[0]
        else: raise ValueError
        if not np.array_equal(orig, self.board):
            self.add_random_tile()
            return True
        return False

    def move_with_cache(self, direction):
        # identycznie jak move()
        return self.move(direction)

    def get_valid_moves(self):
        moves = []
        for m in MOVES:
            tmp = Game2048(); tmp.board = self.board.copy()
            if tmp.move(m):
                moves.append(m)
        return moves

    def is_game_over(self):
        if np.any(self.board==0):
            return False
        return len(self.get_valid_moves())==0

    def get_score(self):
        return np.sum(self.board)

    def get_max_tile(self):
        return np.max(self.board)
