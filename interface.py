import pygame
import copy
from pieces import Piece,King,Night,Bishop,Queen,Rook,Pawn
from location import Square
class Interface:
    def __init__(self,board,graphics):
        self.chessboard = board
        self.graphics = graphics
        self.selectedPiece = None

    def rookPossiblities(self,currentPosX,currentPosY,draw,piece,board,renderAllPossibilities):
        #Horizontal axis
        for i in range(currentPosX+1,len(board)):
            
            #no hace falta simular el tablero
            if not renderAllPossibilities:
                validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(i,currentPosY)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
            if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                if not board[currentPosY][i] or board[currentPosY][i].pieceType.color != piece.pieceType.color:
                    piece.currentPossibilities.add((i,currentPosY))
                    if draw:
                        self.graphics.drawPossibilityCircle(currentPosY,i)
            if board[currentPosY][i] != None:
                break
            
            
        for i in range(currentPosX-1,-1,-1):
            if not renderAllPossibilities:
                validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(i,currentPosY)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
            if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                if not board[currentPosY][i]or board[currentPosY][i].pieceType.color != piece.pieceType.color:
                    if draw:
                        self.graphics.drawPossibilityCircle(currentPosY,i)
                    piece.currentPossibilities.add((i,currentPosY))
            if board[currentPosY][i] != None:
                break
            
        
        #Vertical axis
        for i in range(currentPosY+1,len(board[0])):
            if not renderAllPossibilities:
                validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX,i)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
            if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                if not board[i][currentPosX] or board[i][currentPosX].pieceType.color != piece.pieceType.color:
                    if draw:
                        self.graphics.drawPossibilityCircle(i,currentPosX)
                    piece.currentPossibilities.add((currentPosX,i))
            if board[i][currentPosX] != None:
                break
            
        for i in range(currentPosY-1,-1,-1):
            if not renderAllPossibilities:
                validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX,i)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
            if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                if not board[i][currentPosX] or board[i][currentPosX].pieceType.color != piece.pieceType.color:
                    if draw:
                        self.graphics.drawPossibilityCircle(i,currentPosX)
                    piece.currentPossibilities.add((currentPosX,i))
            if board[i][currentPosX] != None:
                break
                  
    def bishopPossiblities(self,currentPosX,currentPosY,draw,piece,board,renderAllPossibilities):
        #Top left
        for dx,dy in [(1,1),(1,-1),(-1,1),(-1,-1)]:
            p = 1
            while currentPosX  + p*dx < len(board) and currentPosY  + p*dy < len(board[0]):
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX+p*dx,currentPosY+p*dy)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[currentPosY+p*dy][currentPosX+p*dx] or  board[currentPosY+p*dy][currentPosX+p*dx].pieceType.color != piece.pieceType.color:
                        piece.currentPossibilities.add((currentPosX+p*dx,currentPosY+p*dy))
                        if draw:
                            self.graphics.drawPossibilityCircle(currentPosY+p*dy,currentPosX+p*dx)
                if board[currentPosY+p*dy][currentPosX+p*dx] != None:
                    break
                
                p+= 1
        
    def kingPossibilities(self,currentPosX,currentPosY,draw,piece,board,renderAllPossibilities):
        #normal moves
        for x,y in [(-1,0),(-1,1),(1,-1),(0,-1),(1,0),(0,1),(1,1),(-1,-1)]:
            dx = currentPosX + x
            dy = currentPosY + y
            if 0 <= dy < len(board) and 0 <= dx < len(board[0]):
                if not renderAllPossibilities:
                    if self.selectedPiece.pieceType.color == "white":
                        validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(dx,dy)),(dx,dy),self.chessboard.blackKingPos,True)
                    else:
                        validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(dx,dy)),self.chessboard.whiteKingPos,(dx,dy),True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[dy][dx] or board[dy][dx].pieceType.color != piece.pieceType.color:
                        piece.currentPossibilities.add((dx,dy))
                        if draw:
                            self.graphics.drawPossibilityCircle(dy,dx)
                    
                    
        #Check for castling
        if piece.pieceType.color == "white":
            if self.chessboard.whiteQueenCastling and self.chessboard.board[7][1] == self.chessboard.board[7][2]  == self.chessboard.board[7][3] == None:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(2,7)),(2,7),self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[2][7] or board[2][7].pieceType.color != piece.pieceType.color:
                        piece.currentPossibilities.add((2,7))
                        if draw:
                            self.graphics.drawPossibilityCircle(7,2)
                                
            if self.chessboard.whiteKingCastling and self.chessboard.board[7][5] == self.chessboard.board[7][6]  == None:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(6,7)),(6,7),self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[7][6] or board[7][6].pieceType.color != piece.pieceType.color:
                        
                        piece.currentPossibilities.add((6,7))
                        if draw:
                            self.graphics.drawPossibilityCircle(7,6)
                    
        else:
            if self.chessboard.blackQueenCastling and self.chessboard.board[0][1] == self.chessboard.board[0][2]  == self.chessboard.board[0][3] == None:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(2,0)),self.chessboard.whiteKingPos,(2,0),True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[0][2] or board[0][2].pieceType.color != piece.pieceType.color:
                        piece.currentPossibilities.add((2,0))
                        if draw:
                            self.graphics.drawPossibilityCircle(0,2)
            if self.chessboard.blackKingCastling and self.chessboard.board[0][5] == self.chessboard.board[0][6]  == None:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(6,0)),self.chessboard.whiteKingPos,(6,0),True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[0][6] or board[0][6].pieceType.color != piece.pieceType.color:
                        piece.currentPossibilities.add((6,0))
                        if draw:
                            self.graphics.drawPossibilityCircle(0,6)
    
    def knightPossibilities(self,currentPosX,currentPosY,draw,piece,board,renderAllPossibilities):
        for x,y in [(2,-1),(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2)]:
            dx = currentPosX + x
            dy = currentPosY + y
            if 0 <= dy < len(board) and 0 <= dx < len(board[0]):
                if not board[dy][dx] or board[dy][dx].pieceType.color != piece.pieceType.color:
                    if not renderAllPossibilities:
                        validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(dx,dy)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                    if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                        if not board[dy][dx] or  board[dy][dx].pieceType.color != piece.pieceType.color:
                            piece.currentPossibilities.add((dx,dy))
                            if draw:
                                self.graphics.drawPossibilityCircle(dy,dx)
                        
    
    def pawnPossibilities(self,currentPosX,currentPosY,draw,piece,board,renderAllPossibilities):
        if piece.pieceType.color == "white":
            #One and two squares forward
            if currentPosY > 0 and board[currentPosY-1][currentPosX] == None:
                if not renderAllPossibilities:
                        validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX,currentPosY-1)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[currentPosY-1][currentPosX]:
                        piece.currentPossibilities.add((currentPosX,currentPosY-1))
                        if draw:
                            self.graphics.drawPossibilityCircle(currentPosY-1,currentPosX)
            if currentPosY == 6  and board[currentPosY-2][currentPosX] == None == board[currentPosY-1][currentPosX] :
                
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX,currentPosY-2)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[currentPosY-2][currentPosX]:
                        piece.currentPossibilities.add((currentPosX,currentPosY-2))
                        if draw:
                            self.graphics.drawPossibilityCircle(currentPosY-2,currentPosX)
                
            #diagonals
            if currentPosX > 0 and currentPosY > 0 and board[currentPosY-1][currentPosX-1] != None:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX-1,currentPosY-1)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if piece.pieceType.color != board[currentPosY-1][currentPosX-1].pieceType.color:
                        piece.currentPossibilities.add((currentPosX-1,currentPosY-1))
                        if draw:
                            self.graphics.drawPossibilityCircle(currentPosY-1,currentPosX-1)
            if currentPosX < len(board[0])-1 and currentPosY > 0 and board[currentPosY-1][currentPosX+1] != None:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX+1,currentPosY-1)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if piece.pieceType.color != board[currentPosY-1][currentPosX+1].pieceType.color:
                        piece.currentPossibilities.add((currentPosX+1,currentPosY-1))
                        if draw:
                            self.graphics.drawPossibilityCircle(currentPosY-1,currentPosX+1)
                    
            #look for en passant 
            if currentPosX > 0 and currentPosY > 0 and (currentPosX-1,currentPosY-1) == self.chessboard.enPassantSquare:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX-1,currentPosY-1),True),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    piece.currentPossibilities.add((currentPosX-1,currentPosY-1))
                    if draw:
                        self.graphics.drawPossibilityCircle(currentPosY-1,currentPosX-1)
            if currentPosX < len(board[0])-1 and currentPosY > 0 and (currentPosX+1,currentPosY-1) == self.chessboard.enPassantSquare:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX+1,currentPosY-1),True),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                        piece.currentPossibilities.add((currentPosX+1,currentPosY-1))
                        if draw:
                            self.graphics.drawPossibilityCircle(currentPosY-1,currentPosX+1)
                
        else:
            #One and two squares forward
            if currentPosY < len(board)-1 and board[currentPosY+1][currentPosX] == None:
                if not renderAllPossibilities:
                        validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX,currentPosY+1)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[currentPosY+1][currentPosX]:
                        piece.currentPossibilities.add((currentPosX,currentPosY+1))
                        if draw:
                            self.graphics.drawPossibilityCircle(currentPosY+1,currentPosX)
            if currentPosY == 1  and board[currentPosY+2][currentPosX] == None == board[currentPosY+1][currentPosX]:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX,currentPosY+2)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[currentPosY+2][currentPosX]:
                        piece.currentPossibilities.add((currentPosX,currentPosY+2))
                        if draw:
                            self.graphics.drawPossibilityCircle(currentPosY+2,currentPosX)
                
            #diagonals
            if currentPosX > 0 and currentPosY < len(board)-1 and board[currentPosY+1][currentPosX-1] != None:
                #check for oposite color
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX-1,currentPosY+1)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if piece.pieceType.color != board[currentPosY+1][currentPosX-1].pieceType.color:
                        piece.currentPossibilities.add((currentPosX-1,currentPosY+1))
                        if draw:
                            self.graphics.drawPossibilityCircle(currentPosY+1,currentPosX-1)
            if currentPosX < len(board[0])-1 and currentPosY < len(board)-1 and board[currentPosY+1][currentPosX+1] != None:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX+1,currentPosY+1)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if piece.pieceType.color != board[currentPosY+1][currentPosX+1].pieceType.color:
                        piece.currentPossibilities.add((currentPosX+1,currentPosY+1))
                        if draw:
                            self.graphics.drawPossibilityCircle(currentPosY+1,currentPosX+1)
            
            #EN PASSANT
            if currentPosX > 0 and currentPosY < len(board)-1 and (currentPosX-1,currentPosY+1) == self.chessboard.enPassantSquare:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX-1,currentPosY+1),True),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    piece.currentPossibilities.add((currentPosX-1,currentPosY+1))
                    if draw:
                        self.graphics.drawPossibilityCircle(currentPosY+1,currentPosX-1)
            if currentPosX < len(board[0])-1 and currentPosY < len(board)-1 and (currentPosX+1,currentPosY+1) == self.chessboard.enPassantSquare:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX+1,currentPosY+1),True),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                        piece.currentPossibilities.add((currentPosX+1,currentPosY+1))
                        if draw:
                            self.graphics.drawPossibilityCircle(currentPosY+1,currentPosX+1)

        
    def getBoard(self):
        return self.chessboard

    def getGraphics(self):
        return self.graphics
    
    #Return 0 if no checks, returns 1 if white is in check, returns 2 if black is in check
    def isValidBoard(self,board,whiteKingPos, blackKingPos,renderAllPossibilities):
        
        #Iterate through the entire board
        for i in range(len(board)):
            for j in range(len(board[0])):
                #If the square isnt empty, look at what its targeting and check if the opposite king position is there
                if board[i][j] != None:
                    temporarySelectedPiece = board[i][j]
                    temporarySelectedPiece.currentPossibilities.clear()
                    self.renderSelectedPiece(False,temporarySelectedPiece,board,renderAllPossibilities)
                    if temporarySelectedPiece.pieceType.color == "black" and whiteKingPos in temporarySelectedPiece.currentPossibilities:
                        return 1
                    if temporarySelectedPiece.pieceType.color == "white" and blackKingPos in temporarySelectedPiece.currentPossibilities:
                        return 2
        return 0
    
    def move(self,x,y):
        #validate move
        temporaryBoard = self.chessboard.getTempBoard()
            
        #simulate the move in the simulated board
        tempPiece = Piece(self.selectedPiece.row,self.selectedPiece.column, self.selectedPiece.pieceType)
        tempWhiteKingPos = self.chessboard.whiteKingPos
        tempBlackKingPos = self.chessboard.blackKingPos
        if type(tempPiece.pieceType) == King:
            if tempPiece.pieceType.color == "white":
                tempWhiteKingPos = (x,y)
                
            else:
                tempBlackKingPos = (x,y)

        temporaryBoard[tempPiece.row][tempPiece.column] = None
        tempPiece.row = y
        tempPiece.column = x
        temporaryBoard[y][x] = tempPiece

        #Check if board would be valid after simulated move
        validBoardStatus = self.isValidBoard(temporaryBoard,tempWhiteKingPos,tempBlackKingPos,True)
        if validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
            
            if self.chessboard.board[y][x] == None:
                self.graphics.playDefaultSound()
            else:
                self.graphics.playCaptureSound()
                
                
                pieceTypeLetter = str(type(self.chessboard.board[y][x].pieceType))[15]
                if self.chessboard.board[y][x].pieceType.color == "white":
                    self.chessboard.whiteMaterial[pieceTypeLetter] -= 1
                else:
                    self.chessboard.blackMaterial[pieceTypeLetter.lower()] -= 1
            
            #delete pawn when in en passant
            if self.selectedPiece.pieceType.color == "white":
                if type(self.selectedPiece.pieceType) == Pawn and (x,y) == self.chessboard.enPassantSquare:
                    self.graphics.playCaptureSound()
                    self.chessboard.blackMaterial["p"]-=1
                    self.chessboard.board[y+1][x] = None
            else:
                if type(self.selectedPiece.pieceType) == Pawn and (x,y) == self.chessboard.enPassantSquare:
                    self.graphics.playCaptureSound()
                    self.chessboard.whiteMaterial["P"]-=1
                    self.chessboard.board[y-1][x] = None
            
            
            #check either to disable or keep en passant square
            if type(self.selectedPiece.pieceType) == Pawn and abs(y-self.selectedPiece.row) == 2:
                print("KEEP EN PASSANT SQUARE")
                if self.selectedPiece.pieceType.color == "white":
                    self.chessboard.enPassantSquare = (self.selectedPiece.column,self.selectedPiece.row-1)
                else:
                    self.chessboard.enPassantSquare = (self.selectedPiece.column,self.selectedPiece.row+1)
            else:
                self.chessboard.enPassantSquare = None
           
           
           
                        
            
            if self.chessboard.toMove == "white":
                if type(self.selectedPiece.pieceType) == King:
                    self.chessboard.whiteKingPos = (x,y)
                    self.chessboard.whiteKingCastling = False
                    self.chessboard.whiteQueenCastling = False
                #Disable castling in case rook is moved
                if type(self.selectedPiece.pieceType) == Rook:
                    if (self.selectedPiece.column, self.selectedPiece.row) == (0,7):
                        self.chessboard.whiteQueenCastling = False
                    elif (self.selectedPiece.column, self.selectedPiece.row) == (7,7):
                        self.chessboard.whiteKingCastling = False
                    
                self.chessboard.toMove = "black"
            else:
                if type(self.selectedPiece.pieceType) == King:
                    self.chessboard.blackKingPos = (x,y)
                    self.chessboard.blackKingCastling = False
                    self.chessboard.blackQueenCastling = False
                #Disable castling in case rook is moved
                if type(self.selectedPiece.pieceType) == Rook:
                    if (self.selectedPiece.column, self.selectedPiece.row) == (0,0):
                        self.chessboard.blackQueenCastling = False
                    elif (self.selectedPiece.column, self.selectedPiece.row) == (7,0):
                        self.chessboard.blackKingCastling = False
                self.chessboard.toMove = "white"
            self.chessboard.board[self.selectedPiece.row][self.selectedPiece.column] = None
            self.selectedPiece.row = y
            self.selectedPiece.column = x
            self.chessboard.board[y][x] = self.selectedPiece
            
             #check for promotions
            if type(self.selectedPiece.pieceType) == Pawn:
                if self.selectedPiece.pieceType.color == "white" and y == 0:
                    print("PROMOTION!")
                    newType = None
                    while newType != "n" and newType != "b" and newType != "q" and newType != "r":
                        newType = input("Type n for knight, b for bishop, q for queen and r for rook: ")   
                        if newType == "n":
                            self.chessboard.board[y][x] = Piece(self.selectedPiece.row,self.selectedPiece.column,Night("white"))
                        elif newType == "b":
                            self.chessboard.board[y][x] = Piece(self.selectedPiece.row,self.selectedPiece.column,Bishop("white"))
                        elif newType == "r":
                            
                            self.chessboard.board[y][x] = Piece(self.selectedPiece.row,self.selectedPiece.column,Rook("white"))
                        elif newType == "q":
                            self.chessboard.board[y][x] = Piece(self.selectedPiece.row,self.selectedPiece.column,Queen("white"))
                        else:
                            print("INCORRECT INPUT")
                         
                    self.chessboard.printBoardInfo()  
                
                
            self.selectedPiece = None
            print(self.chessboard.whiteMaterial,self.chessboard.blackMaterial)
        else:
            print("Invalid Move",self.selectedPiece.currentPossibilities)

    
    def moveChecker(self):
        if 0 < pygame.mouse.get_pos()[0] < self.graphics.screenHeight and 0 < pygame.mouse.get_pos()[1] < self.graphics.screenWidth:
            gridx,gridy = (pygame.mouse.get_pos()[0]//(self.graphics.pixelsPerSquare),pygame.mouse.get_pos()[1]//(self.graphics.pixelsPerSquare))
            if (self.chessboard.board[gridy][gridx] and  self.chessboard.board[gridy][gridx].pieceType.color == self.chessboard.toMove) or (self.selectedPiece and (gridx,gridy) in self.selectedPiece.currentPossibilities):
                if self.selectedPiece:
                    self.selectedPiece.currentPossibilities.clear()
                    self.renderSelectedPiece(False,None,None,False)
                
                if not self.selectedPiece or (gridx,gridy) not in self.selectedPiece.currentPossibilities :
                    self.selectedPiece = self.chessboard.board[gridy][gridx]
                    if self.selectedPiece:
                        self.selectedPiece.currentPossibilities.clear()
                else:
                    
                    #Check for castling
                    doNormalMove = True
                    if type(self.selectedPiece.pieceType) == King:
                        if self.selectedPiece.pieceType.color == "white":
                            if self.selectedPiece.position == (4,7):
                                if  (gridx,gridy) == (2,7):
                                    #castle queen side
                                    
                                    self.move(2,7)
                                    if not self.selectedPiece:
                                        self.selectedPiece = self.chessboard.board[7][0]
                                        self.move(3,7)
                                        self.chessboard.toMove ="black"
                                        doNormalMove = False
                                    else:
                                        print("INVALID CASTLE")
                                    
                                elif (gridx,gridy) == (6,7):
                                    #castle king side
                                    doNormalMove = False
                                    self.move(6,7)
                                    if not self.selectedPiece:
                                        self.selectedPiece = self.chessboard.board[7][7]
                                        self.move(5,7)
                                        self.chessboard.toMove ="black"
                                    else:
                                        print("INVALID CASTLE")
                        else:
                            if self.selectedPiece.position == (4,0):
                                if  (gridx,gridy) == (2,0):
                                    #castle queen side
                                    self.move(2,0)
                                    if not self.selectedPiece:
                                        self.selectedPiece = self.chessboard.board[0][0]
                                        self.move(3,0)
                                        self.chessboard.toMove ="white"
                                        doNormalMove = False
                                    else:
                                        print("INVALID CASTLE")
                                    
                                elif (gridx,gridy) == (6,0):
                                    #castle king side
                                    self.move(6,0)
                                    if not self.selectedPiece:
                                        self.selectedPiece = self.chessboard.board[0][7]
                                        self.move(5,0)
                                        self.chessboard.toMove ="white"
                                        doNormalMove = False
                                    else:
                                        print("INVALID CASTLING")
                                    
                    if doNormalMove:
                        
                        self.move(gridx,gridy)
                    
            else:
                self.selectedPiece = None
        else:
            print(self.chessboard.boardToFEN())
        
    def renderSelectedPiece(self,draw = True,piece = None,board = None,renderAllPossibilities = True):
        if not piece:
            piece = self.selectedPiece
        if not board:
            board = self.chessboard.board
        currentPosX,currentPosY = piece.column,piece.row
        if type(piece.pieceType) == Rook:
            self.rookPossiblities(currentPosX,currentPosY,draw,piece,board,renderAllPossibilities)
        elif type(piece.pieceType) == Bishop:
            self.bishopPossiblities(currentPosX,currentPosY,draw,piece,board,renderAllPossibilities)
        elif type(piece.pieceType) == Queen:
            self.bishopPossiblities(currentPosX,currentPosY,draw,piece,board,renderAllPossibilities)
            self.rookPossiblities(currentPosX,currentPosY,draw,piece,board,renderAllPossibilities)
        elif type(piece.pieceType) == King:
            self.kingPossibilities(currentPosX,currentPosY,draw,piece,board,renderAllPossibilities)
        elif type(piece.pieceType) == Night:
            self.knightPossibilities(currentPosX,currentPosY,draw,piece,board,renderAllPossibilities)
        elif type(piece.pieceType) == Pawn:
            self.pawnPossibilities(currentPosX,currentPosY,draw,piece,board,renderAllPossibilities)
        else:
            raise TypeError("Piece has no correct type")
    
    def isCheckmate(self,color):
        #check if it is possible to solve the current check
        for i in range(len(self.chessboard.board)):
            for j in range(len(self.chessboard.board[0])):
                temporaryBoard = self.chessboard.getTempBoard()
                currentPiece = temporaryBoard[i][j]
                if currentPiece and currentPiece.pieceType.color == color:
                    self.renderSelectedPiece(False,currentPiece,temporaryBoard)
                    whiteKingPos = self.chessboard.whiteKingPos
                    blackKingPos = self.chessboard.blackKingPos
                    
                    movesToCheck = copy.copy(currentPiece.currentPossibilities)
                    for moves in movesToCheck:
                        if type(currentPiece.pieceType) == King:
                            if color == "white":
                                whiteKingPos = moves
                            else:
                                blackKingPos = moves
                        temporaryBoard = self.chessboard.getTempBoard()
                        temporaryBoard[i][j] = None
                        temporaryBoard[moves[1]][moves[0]] = currentPiece
                        currentPiece.position = moves
                        
                        if self.isValidBoard(temporaryBoard,whiteKingPos,blackKingPos,True) == 0:

                            return False
        return True
    
    def main(self):
        
        self.graphics.checkForQuit()
        self.graphics.fillScreen("gray")
        
        
        self.graphics.drawBoard(self.chessboard)
        
        if pygame.mouse.get_pressed()[0]:
            self.moveChecker()
            
        self.graphics.drawBoard(self.chessboard)
        
        if self.selectedPiece:
            self.graphics.drawSquare("red",(self.selectedPiece.column * self.graphics.pixelsPerSquare, self.selectedPiece.row * self.graphics.pixelsPerSquare, self.graphics.pixelsPerSquare, self.graphics.pixelsPerSquare))
        
        self.graphics.drawPieces(self.chessboard)
        
        if self.selectedPiece:
            self.selectedPiece.currentPossibilities.clear()
            self.renderSelectedPiece(True,None,None,False)
        
        if self.isValidBoard(self.chessboard.board,self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True) == 1:
            print("black checks white")
            if self.isCheckmate("white"):
                self.graphics.displayCheckmate("black")
        elif self.isValidBoard(self.chessboard.board,self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True) == 2:
            print("white checks black")
            if self.isCheckmate("black"):
                self.graphics.displayCheckmate("white")
            
        
        self.graphics.renderToMove()
        
        self.graphics.updateDisplay()