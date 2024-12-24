import pygame
import copy
from pieces import Piece,King,Night,Bishop,Queen,Rook,Pawn
from location import Square
class Interface:
    def __init__(self,board,graphics):
        self.chessboard = board
        self.graphics = graphics
        self.selectedPiece = None

    def rookPossiblities(self,currentPosX,currentPosY,draw,piece,board):
        #Horizontal axis
        for i in range(currentPosX+1,len(board)):
            if not board[currentPosY][i]:
                piece.currentPossibilities.add((i,currentPosY))
                if draw:
                    self.graphics.drawPossibilityCircle(currentPosY,i)
            elif board[currentPosY][i].pieceType.color != piece.pieceType.color:
                piece.currentPossibilities.add((i,currentPosY))
                if draw:
                    self.graphics.drawPossibilityCircle(currentPosY,i)
            
            
            if board[currentPosY][i] != None:
                break
            
            
        for i in range(currentPosX-1,-1,-1):
            if not board[currentPosY][i]:
                if draw:
                    self.graphics.drawPossibilityCircle(currentPosY,i)
                piece.currentPossibilities.add((i,currentPosY))
            elif board[currentPosY][i].pieceType.color != piece.pieceType.color:
                if draw:
                    self.graphics.drawPossibilityCircle(currentPosY,i)
                piece.currentPossibilities.add((i,currentPosY))
            
            if board[currentPosY][i] != None:
                break
            
        
        #Vertical axis
        for i in range(currentPosY+1,len(board[0])):
            if not board[i][currentPosX]:
                if draw:
                    self.graphics.drawPossibilityCircle(i,currentPosX)
                piece.currentPossibilities.add((currentPosX,i))
            elif board[i][currentPosX].pieceType.color != piece.pieceType.color:
                if draw:
                    self.graphics.drawPossibilityCircle(i,currentPosX)
                piece.currentPossibilities.add((currentPosX,i))
            
            if board[i][currentPosX] != None:
                break
            
        for i in range(currentPosY-1,-1,-1):
            if not board[i][currentPosX]:
                if draw:
                    self.graphics.drawPossibilityCircle(i,currentPosX)
                piece.currentPossibilities.add((currentPosX,i))
            elif board[i][currentPosX].pieceType.color != piece.pieceType.color:
                if draw:
                    self.graphics.drawPossibilityCircle(i,currentPosX)
                piece.currentPossibilities.add((currentPosX,i))
            if board[i][currentPosX] != None:
                break
                  
    def bishopPossiblities(self,currentPosX,currentPosY,draw,piece,board):
        #Top left
        p = 1
        while currentPosX  + p < len(board) and currentPosY  + p < len(board[0]):
            if not board[currentPosY+p][currentPosX+p]:
                piece.currentPossibilities.add((currentPosX+p,currentPosY+p))
                if draw:
                    self.graphics.drawPossibilityCircle(currentPosY+p,currentPosX+p)
            elif board[currentPosY+p][currentPosX+p].pieceType.color != piece.pieceType.color:
                piece.currentPossibilities.add((currentPosX+p,currentPosY+p))
                if draw:
                    self.graphics.drawPossibilityCircle(currentPosY+p,currentPosX+p)
            
            if board[currentPosY+p][currentPosX+p] != None:
                break
            
            p+= 1
        
        #top right
        p = 1
        while currentPosX  - p >= 0 and currentPosY  + p < len(board[0]):
            if not board[currentPosY+p][currentPosX-p]:
                piece.currentPossibilities.add((currentPosX-p,currentPosY+p))
                if draw:
                    self.graphics.drawPossibilityCircle(currentPosY+p,currentPosX-p)
            elif board[currentPosY+p][currentPosX-p].pieceType.color != piece.pieceType.color:
                piece.currentPossibilities.add((currentPosX-p,currentPosY+p))
                if draw:
                    self.graphics.drawPossibilityCircle(currentPosY+p,currentPosX-p)
            if board[currentPosY+p][currentPosX-p] != None:
                break
            
            p+= 1
        
         #Bottom left
        p = 1
        while currentPosX  - p >= 0 and currentPosY  -p >= 0:
            if not board[currentPosY-p][currentPosX-p]:
                piece.currentPossibilities.add((currentPosX-p,currentPosY-p))
                if draw:
                    self.graphics.drawPossibilityCircle(currentPosY-p,currentPosX-p)
            elif board[currentPosY-p][currentPosX-p].pieceType.color != piece.pieceType.color:
                piece.currentPossibilities.add((currentPosX-p,currentPosY-p))
                if draw:
                    self.graphics.drawPossibilityCircle(currentPosY-p,currentPosX-p)
            if board[currentPosY-p][currentPosX-p] != None:
                break
            
            p+= 1
        
        #top right
        p = 1
        while currentPosX  + p < len(board) and currentPosY  - p >= 0:
            if not board[currentPosY-p][currentPosX+p]:
                if draw:
                    self.graphics.drawPossibilityCircle(currentPosY-p,currentPosX+p)
                piece.currentPossibilities.add((currentPosX+p,currentPosY-p))
            elif board[currentPosY-p][currentPosX+p].pieceType.color != piece.pieceType.color:
                if draw:
                    self.graphics.drawPossibilityCircle(currentPosY-p,currentPosX+p)
                piece.currentPossibilities.add((currentPosX+p,currentPosY-p))
            if board[currentPosY-p][currentPosX+p] != None:
                break
            
            p+= 1
        
    def kingPossibilities(self,currentPosX,currentPosY,draw,piece,board):
        for x,y in [(-1,0),(-1,1),(1,-1),(0,-1),(1,0),(0,1),(1,1),(-1,-1)]:
            dx = currentPosX + x
            dy = currentPosY + y
            if 0 <= dy < len(board) and 0 <= dx < len(board[0]):
                if not board[dy][dx] or board[dy][dx].pieceType.color != piece.pieceType.color:
                    if draw:
                        self.graphics.drawPossibilityCircle(dy,dx)
                    piece.currentPossibilities.add((dx,dy))
        
        #Check for castling
        if piece.pieceType.color == "white":
            if self.chessboard.whiteQueenCastling and self.chessboard.board[7][1] == self.chessboard.board[7][2]  == self.chessboard.board[7][3] == None:
                if draw:
                    self.graphics.drawPossibilityCircle(7,2)
                piece.currentPossibilities.add((2,7))
            if self.chessboard.whiteKingCastling and self.chessboard.board[7][5] == self.chessboard.board[7][6]  == None:
                if draw:
                    self.graphics.drawPossibilityCircle(7,6)
                piece.currentPossibilities.add((6,7))
        else:
            if self.chessboard.blackQueenCastling and self.chessboard.board[0][1] == self.chessboard.board[0][2]  == self.chessboard.board[0][3] == None:
                if draw:
                    self.graphics.drawPossibilityCircle(0,2)
                piece.currentPossibilities.add((2,0))
            if self.chessboard.blackKingCastling and self.chessboard.board[0][5] == self.chessboard.board[0][6]  == None:
                if draw:
                    self.graphics.drawPossibilityCircle(0,6)
                piece.currentPossibilities.add((6,0))
    
    def knightPossibilities(self,currentPosX,currentPosY,draw,piece,board):
        for x,y in [(2,-1),(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2)]:
            dx = currentPosX + x
            dy = currentPosY + y
            if 0 <= dy < len(board) and 0 <= dx < len(board[0]):
                if not board[dy][dx] or board[dy][dx].pieceType.color != piece.pieceType.color:
                    if draw:    
                        self.graphics.drawPossibilityCircle(dy,dx)
                    piece.currentPossibilities.add((dx,dy))
    
    def pawnPossibilities(self,currentPosX,currentPosY,draw,piece,board):
        if piece.pieceType.color == "white":
            #One and two squares forward
            if currentPosY > 0 and board[currentPosY-1][currentPosX] == None:
                if draw:    
                    self.graphics.drawPossibilityCircle(currentPosY-1,currentPosX)
                piece.currentPossibilities.add((currentPosX,currentPosY-1))
            if currentPosY == 6  and board[currentPosY-2][currentPosX] == None == board[currentPosY-1][currentPosX] :
                if draw:
                    self.graphics.drawPossibilityCircle(currentPosY-2,currentPosX)
                piece.currentPossibilities.add((currentPosX,currentPosY-2))
                
            #diagonals
            if currentPosX > 0 and currentPosY > 0 and board[currentPosY-1][currentPosX-1] != None:
                if piece.pieceType.color != board[currentPosY-1][currentPosX-1].pieceType.color:
                    if draw:
                        self.graphics.drawPossibilityCircle(currentPosY-1,currentPosX-1)
                    piece.currentPossibilities.add((currentPosX-1,currentPosY-1))
            if currentPosX < len(board[0])-1 and currentPosY > 0 and board[currentPosY-1][currentPosX+1] != None:
                if piece.pieceType.color != board[currentPosY-1][currentPosX+1].pieceType.color:
                    if draw:    
                        self.graphics.drawPossibilityCircle(currentPosY-1,currentPosX+1)
                    piece.currentPossibilities.add((currentPosX+1,currentPosY-1))
                    
            #look for en passant 
            if currentPosX > 0 and currentPosY > 0 and (currentPosX-1,currentPosY-1) == self.chessboard.enPassantSquare:
                if draw:    
                    self.graphics.drawPossibilityCircle(currentPosY-1,currentPosX-1)
                piece.currentPossibilities.add((currentPosX-1,currentPosY-1))
            if currentPosX < len(board[0])-1 and currentPosY > 0 and (currentPosX+1,currentPosY-1) == self.chessboard.enPassantSquare:
                if draw:    
                    self.graphics.drawPossibilityCircle(currentPosY-1,currentPosX+1)
                piece.currentPossibilities.add((currentPosX+1,currentPosY-1))
                
        else:
            #One and two squares forward
            if currentPosY < len(board)-1 and board[currentPosY+1][currentPosX] == None:
                if draw:    
                    self.graphics.drawPossibilityCircle(currentPosY+1,currentPosX)
                piece.currentPossibilities.add((currentPosX,currentPosY+1))
            if currentPosY == 1  and board[currentPosY+2][currentPosX] == None == board[currentPosY+1][currentPosX]:
                if draw:    
                    self.graphics.drawPossibilityCircle(currentPosY+2,currentPosX)
                piece.currentPossibilities.add((currentPosX,currentPosY+2))
                
            #diagonals
            if currentPosX > 0 and currentPosY < len(board)-1 and board[currentPosY+1][currentPosX-1] != None:
                #check for oposite color
                if piece.pieceType.color != board[currentPosY+1][currentPosX-1].pieceType.color:
                    if draw:    
                        self.graphics.drawPossibilityCircle(currentPosY+1,currentPosX-1)
                    piece.currentPossibilities.add((currentPosX-1,currentPosY+1))
            if currentPosX < len(board[0])-1 and currentPosY < len(board)-1 and board[currentPosY+1][currentPosX+1] != None:
                if piece.pieceType.color != board[currentPosY+1][currentPosX+1].pieceType.color:
                    if draw:    
                        self.graphics.drawPossibilityCircle(currentPosY+1,currentPosX+1)
                    piece.currentPossibilities.add((currentPosX+1,currentPosY+1))
            
            #EN PASSANT
            if currentPosX > 0 and currentPosY < len(board)-1 and (currentPosX-1,currentPosY+1) == self.chessboard.enPassantSquare:
                if draw:    
                    self.graphics.drawPossibilityCircle(currentPosY+1,currentPosX-1)
                piece.currentPossibilities.add((currentPosX-1,currentPosY+1))
            if currentPosX < len(board[0])-1 and currentPosY < len(board)-1 and (currentPosX+1,currentPosY+1) == self.chessboard.enPassantSquare:
                if draw:    
                    self.graphics.drawPossibilityCircle(currentPosY+1,currentPosX+1)
                piece.currentPossibilities.add((currentPosX+1,currentPosY+1))

        
    def getBoard(self):
        return self.chessboard

    def getGraphics(self):
        return self.graphics
    
    #Return 0 if no checks, returns 1 if white is in check, returns 2 if black is in check
    def isValidMove(self,board,whiteKingPos, blackKingPos,color = None):
        if color == None:
            color = self.chessboard.toMove
        
        #Iterate through the entire board
        for i in range(len(board)):
            for j in range(len(board[0])):
                #If the square isnt empty, look at what its targeting and check if the opposite king position is there
                if board[i][j] != None:
                    temporarySelectedPiece = board[i][j]
                    temporarySelectedPiece.currentPossibilities.clear()
                    self.renderSelectedPiece(False,temporarySelectedPiece,board)
                    if color == "white" and temporarySelectedPiece.pieceType.color == "black" and whiteKingPos in temporarySelectedPiece.currentPossibilities:
                        return 1
                    if color == "black" and temporarySelectedPiece.pieceType.color == "white" and blackKingPos in temporarySelectedPiece.currentPossibilities:
                        return 2
        return 0
    
    def move(self,x,y):
        #validate move
        temporaryBoard = []
        
        for i in range(self.chessboard.height):
            temp = []
            for j in range(self.chessboard.width):
                if self.chessboard.board[i][j] == None:
                    temp.append(None)
                else:
                    curr = self.chessboard.board[i][j]
                    temp.append(Piece(curr.row,curr.column, curr.pieceType))
            temporaryBoard.append(temp)
            
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
        if self.isValidMove(temporaryBoard,tempWhiteKingPos,tempBlackKingPos) == 0:
            
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
            print(self.chessboard.enPassantSquare)
            
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
            
            
                
                
            self.selectedPiece = None
            print(self.chessboard.whiteMaterial,self.chessboard.blackMaterial)
        else:
            print("Invalid Move")

    
    def moveChecker(self):
        if 0 < pygame.mouse.get_pos()[0] < self.graphics.screenHeight and 0 < pygame.mouse.get_pos()[1] < self.graphics.screenWidth:
            gridx,gridy = (pygame.mouse.get_pos()[0]//(self.graphics.pixelsPerSquare),pygame.mouse.get_pos()[1]//(self.graphics.pixelsPerSquare))
            if (self.chessboard.board[gridy][gridx] and  self.chessboard.board[gridy][gridx].pieceType.color == self.chessboard.toMove) or (self.selectedPiece and (gridx,gridy) in self.selectedPiece.currentPossibilities):
                if not self.selectedPiece or (gridx,gridy) not in self.selectedPiece.currentPossibilities :
                    self.selectedPiece = self.chessboard.board[gridy][gridx]
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
        
    def renderSelectedPiece(self,draw = True,piece = None,board = None):
        if not piece:
            piece = self.selectedPiece
        if not board:
            board = self.chessboard.board
        currentPosX,currentPosY = piece.column,piece.row
        if type(piece.pieceType) == Rook:
            self.rookPossiblities(currentPosX,currentPosY,draw,piece,board)
        elif type(piece.pieceType) == Bishop:
            self.bishopPossiblities(currentPosX,currentPosY,draw,piece,board)
        elif type(piece.pieceType) == Queen:
            self.bishopPossiblities(currentPosX,currentPosY,draw,piece,board)
            self.rookPossiblities(currentPosX,currentPosY,draw,piece,board)
        elif type(piece.pieceType) == King:
            self.kingPossibilities(currentPosX,currentPosY,draw,piece,board)
        elif type(piece.pieceType) == Night:
            self.knightPossibilities(currentPosX,currentPosY,draw,piece,board)
        elif type(piece.pieceType) == Pawn:
            self.pawnPossibilities(currentPosX,currentPosY,draw,piece,board)
        else:
            raise TypeError("Piece has no correct type")
    
    def isCheckmate(self,color):
        #color represents the color that is being checked (black in test case)
        
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
                        
                        if self.isValidMove(temporaryBoard,whiteKingPos,blackKingPos,color) == 0:
                            print(currentPiece.pieceType,moves)
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
            self.renderSelectedPiece()
        
        if self.isValidMove(self.chessboard.board,self.chessboard.whiteKingPos,self.chessboard.blackKingPos) == 1:
            print("black checks white")
            if self.isCheckmate("white"):
                self.graphics.displayCheckmate("black")
        elif self.isValidMove(self.chessboard.board,self.chessboard.whiteKingPos,self.chessboard.blackKingPos) == 2:
            print("white checks black")
            if self.isCheckmate("black"):
                self.graphics.displayCheckmate("white")
            
        
        self.graphics.renderToMove()
        
        self.graphics.updateDisplay()