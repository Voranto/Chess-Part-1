import pygame
from chessboard import Chessboard
from pieces import Piece,King,Bishop,Queen,Rook,Pawn
from location import Square

class Graphics:
    def __init__(self, width, height,board):

        self.screenHeight = height
        self.screenWidth = width
        self.board = board
        self.screen = pygame.display.set_mode(
            (self.screenWidth, self.screenHeight))
        
        self.pixelsPerSquare = min(self.screenHeight,self.screenWidth) // 8
        
        
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.bigFont = pygame.font.SysFont("Comic Sans MS", 100)
        self.defaultMove =  pygame.mixer.Sound('assets/defaultMove.mp3')
        self.capture =  pygame.mixer.Sound('assets/capture.mp3')
        pygame.display.set_caption("Chess Board")

    def getScreenHeight(self):
        return self.screenHeight
    def getScreenWidth(self):
        return self.screenWidth
    def getScreen(self):
        return self.screen

    def playDefaultSound(self):
        self.defaultMove.play()
    
    def playCaptureSound(self):
        self.capture.play()
    
    def drawPossibilityCircle(self,x,y):
        pygame.draw.circle(self.screen, pygame.Color(80,80,80,2),(y*self.pixelsPerSquare + self.pixelsPerSquare // 2, x * self.pixelsPerSquare + self.pixelsPerSquare // 2),15)
    

    
    
    def fillScreen(self,color):
        self.screen.fill(color)
    
    def checkForQuit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT()
                exit()
    
    def drawSquare(self,color,rect):
        pygame.draw.rect(self.screen,color,rect)
    
    def renderToMove(self):
        text1 = self.my_font.render("To move: ", False, (0, 0, 0))
        text2 = self.my_font.render(str(self.board.toMove).upper(), False, (0, 0, 0))
        self.screen.blit(text1, (820,10))
        self.screen.blit(text2, (830,50))
        
        
    def updateDisplay(self):
        pygame.display.update()
            
        
        
        
        
    def displayCheckmate(self,color):
        text1 = self.bigFont.render("CHECKMATE",False,(0,0,0))
        text2 = self.bigFont.render(str(color).upper() + " WINS",False,(0,0,0))
        pygame.draw.rect(self.screen, "lightgray",(80,230,700,350))
        self.screen.blit(text1,(100,250))
        self.screen.blit(text2,(80,400))
    
    def drawBoard(self,chessboard):
        boardHeight = chessboard.getHeight()
        boardWidth = chessboard.getWidth()
        
        pixelsPerSquare = min(self.screenHeight,self.screenWidth) // boardHeight 
        
        
        #draw squares
        for i in range(boardHeight):
            for j in range(boardWidth):
                rectValues = (j*pixelsPerSquare,i*pixelsPerSquare,pixelsPerSquare,pixelsPerSquare)
                color = pygame.Color("chartreuse4") if (i+j)%2 == 1 else pygame.Color("cornsilk2")
                pygame.draw.rect(self.screen,color,rectValues)
    
    
    def printBoard(self):
        for row in self.board.board:
            for obj in row:
                if obj is None:
                    print("None", end=" ")
                else:
                    print(type(obj.pieceType), end=" ")
    
    def drawPieces(self,chessboard):
        pieces = self.board.board
        boardHeight = chessboard.getHeight()
        boardWidth = chessboard.getWidth()
        
        pixelsPerSquare = min(self.screenHeight,self.screenWidth) // boardHeight 
        offset = 5
        n = len(pieces)
        m = len(pieces[0])
        
        for i in range(n):
            for j in range(m):
                currentPiece = pieces[i][j]
                if currentPiece == None:
                    continue
                
                self.screen.blit(currentPiece.getTexture(), (j*pixelsPerSquare + offset,i*pixelsPerSquare + offset))