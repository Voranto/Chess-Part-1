import pygame
class Piece:
    def __init__(self,row,column,pieceType):
        self.row = row
        self.column = column
        self.position = (column,row)
        self.pieceType = pieceType
        self.currentPossibilities = set()
    
    def getTexture(self):
        return self.pieceType.texture
        

class Rook:
    def __init__(self,color):
        self.color = color
        if self.color == "white":
            self.texture = pygame.image.load("assets/whiteRook.png")
        elif self.color == "black":
            self.texture = pygame.image.load("assets/blackRook.png")
        else:
            raise Exception("Invalid Piece Color for Rook")
        self.texture = pygame.transform.scale_by(self.texture,1.5)
        
class Bishop:
    def __init__(self,color):
        self.color = color
        if self.color == "white":
            self.texture = pygame.image.load("assets/whiteBishop.png")
        elif self.color == "black":
            self.texture = pygame.image.load("assets/blackBishop.png")
        else:
            raise Exception("Invalid Piece Color for Bishop")
        self.texture = pygame.transform.scale_by(self.texture,1.5)
        
class Pawn:
    def __init__(self,color):
        self.color = color
        if self.color == "white":
            self.texture = pygame.image.load("assets/whitePawn.png")
        elif self.color == "black":
            self.texture = pygame.image.load("assets/blackPawn.png")
        else:
            raise Exception("Invalid Piece Color for Pawn")
        self.texture = pygame.transform.scale_by(self.texture,1.5)
        
class Queen:
    def __init__(self,color):
        self.color = color
        if self.color == "white":
            self.texture = pygame.image.load("assets/whiteQueen.png")
        elif self.color == "black":
            self.texture = pygame.image.load("assets/blackQueen.png")
        else:
            raise Exception("Invalid Piece Color for Queen")
        self.texture = pygame.transform.scale_by(self.texture,1.5)
    
class Night:
    def __init__(self,color):
        self.color = color
        if self.color == "white":
            self.texture = pygame.image.load("assets/whiteKnight.png")
        elif self.color == "black":
            self.texture = pygame.image.load("assets/blackKnight.png")
        else:
            raise Exception("Invalid Piece Color for Knight")
        self.texture = pygame.transform.scale_by(self.texture,1.5)
        
class King:
    def __init__(self,color):
        self.color = color
        if self.color == "white":
            self.texture = pygame.image.load("assets/whiteKing.png")
        elif self.color == "black":
            self.texture = pygame.image.load("assets/blackKing.png")
        else:
            raise Exception("Invalid Piece Color for King")       
        self.texture = pygame.transform.scale_by(self.texture,1.5)
        
