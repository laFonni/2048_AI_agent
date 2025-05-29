# expectimax_agent.pyx
import numpy as np
cimport numpy as cnp
from libc.math cimport fmax

cdef class ExpectimaxAgent:
    cdef int max_depth

    def __init__(self, int max_depth=3):
        self.max_depth = max_depth

    cpdef get_move(self, game):
        cdef float best_score = -1e10
        cdef best_move = None
        for move in game.get_valid_moves():
            clone = game.copy()
            clone.move(move)
            score = self.expectimax(clone, 1, False)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    cpdef expectimax(self, game, int depth, bint is_player):
        cdef float val, best, total
        if depth >= self.max_depth or game.is_game_over():
            return self.evaluate(game)

        if is_player:
            best = -1e10
            for move in game.get_valid_moves():
                clone = game.copy()
                clone.move(move)
                val = self.expectimax(clone, depth + 1, False)
                best = fmax(best, val)
            return best
        else:
            empty = list(zip(*np.where(game.board == 0)))
            if not empty:
                return self.evaluate(game)
            total = 0.0
            for pos in empty:
                for val_, prob in [(2, 0.9), (4, 0.1)]:
                    clone = game.copy()
                    clone.board[pos] = val_
                    total += prob * self.expectimax(clone, depth + 1, True)
            return total / (len(empty) * 2)

    cpdef float evaluate(self, game):
        cdef cnp.ndarray[cnp.int_t, ndim=2] board = game.get_board()
        cdef int empty = np.sum(board == 0)
        cdef int max_tile = np.max(board)
        cdef int smooth = self._smoothness(board)
        return empty * 100 + max_tile + smooth

    cpdef int _smoothness(self, cnp.ndarray[cnp.int_t, ndim=2] board):
        cdef int score = 0
        cdef int x, y
        for x in range(4):
            for y in range(3):
                if board[x][y] == board[x][y+1]:
                    score += board[x][y]
                if board[y][x] == board[y+1][x]:
                    score += board[y][x]
        return score
