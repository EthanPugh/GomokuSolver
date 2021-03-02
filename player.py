import numpy as np

from misc import legalMove
from gomokuAgent import GomokuAgent


class Player(GomokuAgent):

    def move(self, board):
        # moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2)) random move
        return self.minimax_decision(board)

    def minimax_decision(self, board):
        # return value maximising/minimising minValue/maxValue
        if self.ID == 1:
            return self.max_value(board)
        else:
            return self.min_value(board)

    def max_value(self, board):
        # initialize v = -∞
        v = -np.inf
        moveLoc = (-1, -1)
        while not legalMove(board, moveLoc):
            moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2))

        successors, coords = self.get_successors(board)

        # for each successor of state:
        for i in range(len(successors)):
            state_val = self.value(successors[i])

            if state_val > v:
                v = state_val
                moveLoc = (coords[i][0], coords[i][1])

        return moveLoc

    def min_value(self, board):
        # initialize v = +∞
        v = np.inf
        moveLoc = (-1, -1)
        while not legalMove(board, moveLoc):
            moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2))

        successors, coords = self.get_successors(board)

        # for each successor of state:
        for i in range(len(successors)):
            state_val = self.value(successors[i])

            if state_val < v:
                v = state_val
                moveLoc = (coords[i][0], coords[i][1])

        return moveLoc

    def value(self, board):
        # return value of position
        # Terminal positions are filled boards

        p1_weight = self.row_weight(board, 1) + self.diag_weight(board, 1)
        p2_weight = self.row_weight(board, -1) + self.diag_weight(board, -1)

        return p1_weight - p2_weight

    def row_weight(self, board, playerID):
        BOARD_SIZE = board.shape[0]
        X_IN_A_LINE = self.X_IN_A_LINE
        sum_weight = 0

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE - X_IN_A_LINE + 1):
                opponent_combo = 0

                for i in range(X_IN_A_LINE):

                    if board[r, c + i] != playerID:  # player's chain of length (i + 1) starting at r, c
                        sum_weight = sum_weight + pow(i + 1, 2)

                  ##  if board[r, c + i] != -playerID:  # opponent's chain of length (i + 1) at r, c
                    ##    if i < X_IN_A_LINE - 1 and board[r, c + i] == playerID:
                       ##     sum_weight = sum_weight + pow(i + 1, 2)

        return sum_weight

    def diag_weight(self, board, playerID):
        BOARD_SIZE = board.shape[0]
        X_IN_A_LINE = self.X_IN_A_LINE
        sum_weight = 0

        for r in range(BOARD_SIZE - X_IN_A_LINE + 1):
            for c in range(BOARD_SIZE - X_IN_A_LINE + 1):
                for i in range(X_IN_A_LINE):

                    if board[r + i, c + i] != playerID:  # player's chain of length (i + 1) starting at r, c
                        sum_weight = sum_weight + pow(i + 1, 2)

                   ## if board[r + i, c + i] != -playerID:  # opponent's chain of length (i + 1) at r, c
                     ##   if i < X_IN_A_LINE - 1 and board[r, c + i] == playerID:
                        ##    sum_weight = sum_weight + pow(i + 1, 2)

        return sum_weight

    def get_successors(self, board):
        successors = np.array([])
        coords = np.array([])
        BOARD_SIZE = board.shape[0]

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r, c] == 0:
                    temp = board
                    temp[r, c] = self.ID
                    np.append(successors, temp)
                    np.append(coords, [r, c])

        return successors, coords