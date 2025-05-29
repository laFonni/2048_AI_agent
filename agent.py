import numpy as np
from game2048 import Game2048, MOVES
import math

def monotonicity(board):
    score = 0
    # poziomo
    for i in range(4):
        for j in range(3):
            if board[i, j] > board[i, j + 1]:
                score += board[i, j] - board[i, j + 1]
            else:
                score += board[i, j + 1] - board[i, j]
    # pionowo
    for j in range(4):
        for i in range(3):
            if board[i, j] > board[i + 1, j]:
                score += board[i, j] - board[i + 1, j]
            else:
                score += board[i + 1, j] - board[i, j]
    return -score  # mniejsza różnica = większa monotoniczność


def corner_score(board):
    corners = [board[0, 0], board[0, 3], board[3, 0], board[3, 3]]
    return max(corners) * 2  # podbij wagę


def clustering(board):
    penalty = 0
    for i in range(4):
        for j in range(4):
            if board[i, j] == 0: continue
            # suma odległości do sąsiadów o podobnej wartości
            neighbours = []
            if i < 3: neighbours.append(board[i + 1, j])
            if j < 3: neighbours.append(board[i, j + 1])
            penalty += sum(abs(board[i, j] - n) for n in neighbours)
    return -penalty

def smoothness(board):
    def log2(v): return 0 if v==0 else math.log2(v)
    s = 0
    for i in range(4):
        for j in range(3):
            if board[i,j] and board[i,j+1]:
                s -= abs(log2(board[i,j]) - log2(board[i,j+1]))
    for i in range(3):
        for j in range(4):
            if board[i,j] and board[i+1,j]:
                s -= abs(log2(board[i,j]) - log2(board[i+1,j]))
    return s

def dynamic_depth(board):
    e = np.sum(board==0)
    if e>=8: return 2
    if e>=6: return 3
    if e>=4: return 4
    if e>=2: return 5
    return 6



class ExpectimaxAgent:
    def __init__(self, max_depth=6):
        self.max_depth = max_depth

    def get_move(self, game):
        best, bm = -1e9, None
        for m in game.get_valid_moves():
            tmp = game.copy()
            tmp.move_with_cache(m)
            val = self.expectimax(tmp,1,False)
            if val>best:
                best, bm = val, m
        return bm

    def expectimax(self, game, depth, player):
        board = game.board
        if depth>=dynamic_depth(board) or game.is_game_over():
            return self.evaluate(board)

        if player:
            best = -1e9
            for m in game.get_valid_moves():
                tmp = game.copy(); tmp.move_with_cache(m)
                best = max(best, self.expectimax(tmp, depth+1, False))
            return best
        else:
            empties = list(zip(*np.where(board==0)))
            if not empties: return self.evaluate(board)
            s = 0
            spawns = [(2,0.9),(4,0.1)] if depth==1 else [(2,1.0)]
            for x,y in empties:
                for v,p in spawns:
                    tmp = game.copy()
                    tmp.board[x,y] = v
                    s += p*self.expectimax(tmp, depth+1, True)
            return s/len(empties)

    def evaluate(self, board):
        empt = np.sum(board == 0)
        mx = np.max(board)
        smo = smoothness(board)
        mono = monotonicity(board)
        corner = corner_score(board)
        cluster = clustering(board)
        return (
                empt * 200 +
                mx * 5 +
                smo * 1 +
                mono * 1 +
                corner * 2 +
                cluster * 1
        )

