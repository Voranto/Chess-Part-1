from pieces import Piece,King,Night,Bishop,Queen,Rook,Pawn
from location import Square

class Chessboard:
    
    def __init__(self, height, width):
        if (height != width):
            raise ValueError("The chess grid must be square")
        self.height = height
        self.width = width
        self.board = [[None]*width for _ in range(height)]
        
        
        self.toMove = "white"
        self.fullMoves = 1
        self.halfMoves = 0
        
        self.whiteMaterial = {"R":0 , "B": 0, "N":0,"Q":0,"K":0,"P":0}
        self.blackMaterial = {"r":0 , "b": 0, "n":0,"q":0,"k":0,"p":0}
        
        self.enPassantSquare = None
        
        self.whiteKingPos = None
        self.blackKingPos = None
        
        #Castling booleans
        self.whiteKingCastling = True
        self.whiteQueenCastling = True
        self.blackKingCastling = True
        self.blackQueenCastling = True
    
    
    
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def getFEN(self):
        return self.FEN

    def setFEN(self, value):
        self.FEN = value

    def getBoard(self):
        return self.board[:]
    
    def setBoard(self, board):
        self.board = board[:]

    def FENToBoard(self,FEN):
        n = len(FEN)
        i = 0
        j = 0
        
        #board part of FEN
        for p in range(n):
            if FEN[p] == " ":
                p+= 1
                break
            
            elif FEN[p]  == "/":
                j += 1
                i = 0 
            else:
                if FEN[p].isdigit():
                    i += int(FEN[p])
                else:
                    if FEN[p].lower() == "p":
                        self.board[j][i] = Piece(j,i,Pawn("white" if FEN[p] == "P" else "black"))
                    elif FEN[p].lower() == "r":
                        self.board[j][i] = Piece(j,i,Rook("white" if FEN[p] == "R" else "black"))
                    elif FEN[p].lower() == "n":
                        self.board[j][i] = Piece(j,i,Night("white" if FEN[p] == "N" else "black"))
                    elif FEN[p].lower() == "b":
                        self.board[j][i] = Piece(j,i,Bishop("white" if FEN[p] == "B" else "black"))
                    elif FEN[p].lower() == "q":
                        self.board[j][i] = Piece(j,i,Queen("white" if FEN[p] == "Q" else "black")) 
                    elif FEN[p].lower() == "k":
                        self.board[j][i] = Piece(j,i,King("white" if FEN[p] == "K" else "black"))
                        
                        if FEN[p] == "K":
                            self.whiteKingPos  = (i,j)
                        else:
                            self.blackKingPos  = (i,j)
                    else:
                        raise Exception("Invalid piece type when reading FEN", str(FEN[p]))

                    if FEN[p] in self.whiteMaterial:
                        self.whiteMaterial[FEN[p]] += 1
                    else:
                        self.blackMaterial[FEN[p]] += 1
                    i+= 1
        
        currentCheck = 0
        while p < n:
            if FEN[p] == " ":
                currentCheck += 1
            else:
                #Checking who is to move
                if currentCheck == 0:
                    if FEN[p] == "w":
                        self.toMove = "white"
                    elif FEN[p] == "b":
                        self.toMove = "black"
                    else:
                        raise Exception("Error when reading FEN and assigning color")
                    
                    
                elif currentCheck == 1:
                    self.whiteKingCastling = FEN[p] != "-"
                    self.whiteQueenCastling = FEN[p+1] != "-"
                    self.blackKingCastling = FEN[p+2] != "-"
                    self.blackQueenCastling = FEN[p+3] != "-"
                    p+= 3 
                elif currentCheck == 2:
                    if FEN[p] == "-":
                        pass
                    else:
                        self.enPassantSquare = (ord(FEN[p])-97, int(FEN[p+1]))
                        p+= 1
                
                elif currentCheck == 3:
                    self.halfMoves = int(FEN[p])
                
                elif currentCheck == 4:
                    self.fullMoves = int(FEN[p])
                
                else:
                    raise ValueError("currentCheck has too high a value. Too many spaces in the FEN")
            p+= 1
                            
    def boardToFEN(self,board = None):
        if board == None: board = self.board
        
        FEN = ""
        
        for i in range(len(board)):
            c = 0
            for j in range(len(board[0])):
                if board[i][j] == None:
                    c += 1
                else:
                    if c != 0:
                        FEN += str(c)
                    pieceTypeLetter = str(type(board[i][j].pieceType))[15]
                    if board[i][j].pieceType.color == "white":
                        FEN +=   pieceTypeLetter.upper()
                    else:
                        FEN += pieceTypeLetter.lower()
                    c = 0
            if c != 0:
                FEN += str(c)
            if i != len(board)-1:
                FEN += "/"
        FEN += " " + str(self.toMove)[0] + " "
        
        
        FEN += "K"if self.whiteKingCastling else "-"
        FEN += "Q"if self.whiteQueenCastling else "-"
        FEN += "k"if self.blackKingCastling else "-"
        FEN += "q"if self.blackQueenCastling else "-"
        
        FEN += " "
        
        if self.enPassantSquare:
            FEN += chr(self.enPassantSquare[0]+97)
            FEN += str(self.enPassantSquare[1])
        else:
            FEN += "- "
            
        FEN += " " + str(self.halfMoves)
        FEN += " " + str(self.fullMoves)
        return FEN
                                     
                                
    def getTempBoard(self):
        temporaryBoard = []
        #create clone of board to not affect the main one
        for i in range(self.height):
            temp = []
            for j in range(self.width):
                if self.board[i][j] == None:
                    temp.append(None)
                else:
                    curr = self.board[i][j]
                    temp.append(Piece(curr.row,curr.column, curr.pieceType))
            temporaryBoard.append(temp)
        return temporaryBoard         
                        
        
    def printBoardInfo(self):
        for row in self.board:
            temp = [type(item.pieceType) if item else "None" for item in row]
            print(temp)
            
        print("Person to move is: ", self.toMove)
        print("White King Side Castling: ", self.whiteKingCastling)
        print("White Queen Side Castling: ", self.whiteQueenCastling)
        print("Black King Side Castling: ", self.blackKingCastling)
        print("Black Queen Side Castling: ", self.blackQueenCastling)
        print("White king pos: ", self.whiteKingPos)
        print("Black king pos: ", self.blackKingPos)
        if (self.enPassantSquare):
            print("En passant target square is: " ,self.enPassantSquare)
        else:
            print("No target en passant Square")
        
        print("Full moves: " ,self.fullMoves)
        print("Half moves: " ,self.halfMoves)
            
    