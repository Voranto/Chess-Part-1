from chessboard import Chessboard
from graphics import Graphics
from interface import Interface
import pygame


FEN = "rnbnqb2/pp1pkrpp/4pp2/1BP5/8/3Q4/PPP1PPPP/RNB1K1NR b KQkq - 0 1"
board = Chessboard(8,8)
print(chr(97))
board.FENToBoard(FEN)
print(board.boardToFEN())
graphics = Graphics(1000,800,board) 
print(board.printBoardInfo())

interface = Interface(board,graphics)
while True:
    interface.main()
    
    
