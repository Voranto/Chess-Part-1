from chessboard import Chessboard
from graphics import Graphics
from interface import Interface


FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
board = Chessboard(8,8)
print(chr(97))
board.FENToBoard(FEN)
print(board.boardToFEN())
graphics = Graphics(1000,800,board) 
print(board.printBoardInfo())

interface = Interface(board,graphics)
while True:
    interface.main()
    
    
