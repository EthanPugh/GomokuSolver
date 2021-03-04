# Minimax Gomoku Agent
#
# Mitchell James 981988
# Ethan Pugh 985094
# Swansea University

import numpy as np
from gomokuAgent import GomokuAgent
from misc import legalMove


class Player(GomokuAgent):

    def move(self, board):
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

        coords = self.get_successors(board)

        # for each successor of state:
        for i in range(len(coords)):
            temp = np.array(board)
            r = coords[i][0]
            c = coords[i][1]

            temp[r, c] = self.ID

            state_val = self.value(temp)

            if state_val > v and legalMove(board, (r, c)):
                v = state_val
                moveLoc = (r, c)

        return moveLoc

    def min_value(self, board):
        # initialize v = +∞
        v = np.inf

        coords = self.get_successors(board)

        # for each successor of state:
        for i in range(len(coords)):

            temp = np.array(board)
            r = coords[i][0]
            c = coords[i][1]

            temp[r, c] = self.ID

            state_val = self.value(temp)

            if state_val < v and legalMove(board, (r, c)):
                v = state_val
                moveLoc = (r, c)

        return moveLoc

    def value(self, board):
        # return value of position
        # Terminal positions are filled boards
        return self.row_weight(board) + self.diag_weight(board)

    def row_weight(self, board):
        BOARD_SIZE = self.BOARD_SIZE
        X_IN_A_LINE = self.X_IN_A_LINE
        sum_weight = 0

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE - X_IN_A_LINE + 1):

                for i in range(X_IN_A_LINE):

                    if board[r, c + i] != 1:  # player 1's vertical chain of length (i + 1) starting at r, c
                        sum_weight = sum_weight + pow(i, 2)

                    if board[r, c + i] != -1:  # player 2's vertical chain of length (i + 1) starting at r, c
                        sum_weight = sum_weight - pow(i, 2)

        return sum_weight

    def diag_weight(self, board):
        BOARD_SIZE = self.BOARD_SIZE
        X_IN_A_LINE = self.X_IN_A_LINE
        sum_weight = 0

        for r in range(BOARD_SIZE - X_IN_A_LINE + 1):
            for c in range(BOARD_SIZE - X_IN_A_LINE + 1):
                for i in range(X_IN_A_LINE):

                    if board[r + i, c + i] != 1:  # player 1's chain of length (i + 1) starting at r, c
                        sum_weight = sum_weight + pow(i + 1, 2)

                    if board[r + i, c + i] != -1:  # player 2's chain of length (i + 1) starting at r, c
                        sum_weight = sum_weight - pow(i + 1, 2)

        return sum_weight

    def get_successors(self, board):
        coords = np.array([[0, 0]])
        BOARD_SIZE = self.BOARD_SIZE

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r, c] == 0:
                    coords = np.append(coords, np.array([[r, c]]), axis=0)

        return np.delete(coords, 0, 0)
