import copy
import os
import sys


class GamePosition:
    def __init__(self, board, player, whiteCastling, blackCastling):
        self.board = board
        self.player = player
        self.whiteCastling = whiteCastling
        self.blackCastling = blackCastling
        self.castlingRights = [self.whiteCastling, self.blackCastling]
    def getPeice(self, x, y):
        return self.board[x][y]
    def getBoard(self):
        return self.board
    def getWhiteCastlingRight(self):
        return whiteCastling
    def getBlackCastlingRight(self, board):
        return blackCastling
    def drawPos(self):
        for i in range(0, 8):
            print(i)
    def clone(self):
        return GamePosition(copy.deepcopy(self.board), copy.deepcopy(self.player), 
            copy.deepcopy(self.whiteCastling), copy.deepcopy(self.blackCastling))
