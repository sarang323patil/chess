# Draw Board
# Date - 16/09/2020

import pygame
from pygame import mixer  # Load the popular external library

mixer.init()
pygame.init()

gamePosition = [['bR', 'bP', 0, 0, 0, 0, 'wP', 'wR'],
                ['bN', 'bP', 0, 0, 0, 0, 'wP', 'wN'],
                ['bB', 'bP', 0, 0, 0, 0, 'wP', 'wB'],
                ['bQ', 'bP', 0, 0, 0, 0, 'wP', 'wQ'],
                ['bK', 'bP', 0, 0, 0, 0, 'wP', 'wK'],
                ['bB', 'bP', 0, 0, 0, 0, 'wP', 'wB'],
                ['bN', 'bP', 0, 0, 0, 0, 'wP', 'wN'],
                ['bR', 'bP', 0, 0, 0, 0, 'wP', 'wR'] ]



class DrawChessBoard():
    # DRAWING CHESS BOARD
    # DRAWING 
    def __init__(self, gamePosition, drag=False, dragX=None, dragY=None, dragPeice=None, legalPath=[]):    
        import pygame
        import collections
        import os
        pygame.init()

        self.peiceDict = {'b':80, 'w':0, 'K':0, 'Q':80, 'B':160, 'N':240, 'R':320, 'P':400}
        self.drag=drag   # boolean (T/F) if the peice is being draged or not
        self.dragX = dragX   # run time cordinate of peice being draged
        self.dragY = dragY
        self.dragPeice = dragPeice   # The peice which is being draged right now
        self.legalPath = legalPath   # Legal path of the peice being draged
        self.boardSize=(640, 640)    # size of board
        self.gamePosition = gamePosition   # 2D array, Position of all the peices on Board
        self.mainBoard = pygame.display.set_mode(size=self.boardSize)  # Main board window

        # Loading sprites which needs to be displayed
        self.boardImg = pygame.image.load(os.path.join('sprites', 'myboard.png')).convert_alpha()
        self.boardImg = pygame.transform.scale(self.boardImg, (640, 640))
        self.peiceImg = pygame.image.load(os.path.join('sprites', 'peicesImg.png')).convert_alpha()
        self.peiceImg = pygame.transform.scale(self.peiceImg, (480, 160))
        self.redCircle = pygame.image.load(os.path.join('sprites', 'red_circle.png'))
        self.redCircle = pygame.transform.scale(self.redCircle, (20, 20))

        # Print Board and Peices
        self.mainBoard.blit(self.boardImg, (0,0))
        for i in range(0, 8):
            for j in range(0, 8):
                if(self.gamePosition[i][j]!=0):
                    peiceColor = self.peiceDict[gamePosition[i][j][0]]
                    peiceType  = self.peiceDict[gamePosition[i][j][1]]
                    self.mainBoard.blit(self.peiceImg, (i*80, j*80), (peiceType,peiceColor,80,80))
                    

        # PRINT draging PEICE
        if(self.drag==True):
            dragPeiceColor = self.peiceDict[self.dragPeice[0]]
            dragPeiceType  = self.peiceDict[self.dragPeice[1]]
            self.mainBoard.blit(self.peiceImg, (self.dragX, self.dragY), (dragPeiceType,dragPeiceColor,80,80))
            
        # Highlight the Path of Peice being Draged
        if(len(self.legalPath)>0):
            for cord in self.legalPath:
                # print(cord)
                if(cord[1]!='w' and cord[1]!='b'):
                    self.mainBoard.blit(self.redCircle, (cord[0]*80+30, cord[1]*80+30))
                else:
                    if(cord[1]=='w'):
                        if(cord[0]=='L'):
                            self.mainBoard.blit(self.redCircle, (2*80+30, 7*80+30))
                        if(cord[0]=='R'):
                            self.mainBoard.blit(self.redCircle, (6*80+30, 7*80+30))
                    if(cord[1]=='b'):
                        if(cord[0]=='L'):
                            self.mainBoard.blit(self.redCircle, (2*80+30, 0*80+30))
                        if(cord[0]=='R'):
                            self.mainBoard.blit(self.redCircle, (6*80+30, 0*80+30))
        

        pygame.display.update() 




def findLegalPath(gamePosition, x, y, peice):
    # Finds the legal path of the peice being draged 
    # print(peice)
    listOfPath = set()

    # Pawn Movement
    if(peice[1]=='P'):   
        if(peice[0]=='w'):
            if(y==6 and gamePosition[x][y-1]==0 and gamePosition[x][y-2]==0):
                listOfPath.add((x, y-1))
                listOfPath.add((x, y-2))
            if(y-1>=0 and gamePosition[x][y-1]==0):
                listOfPath.add((x, y-1))
            if(y-1>=0 and x-1>=0 and gamePosition[x-1][y-1]!=0 and gamePosition[x-1][y-1][0]=='b'):
                listOfPath.add((x-1, y-1))
            if(y-1>=0 and x+1<=7 and gamePosition[x+1][y-1]!=0 and gamePosition[x+1][y-1][0]=='b'):
                listOfPath.add((x+1, y-1))

        if(peice[0]=='b'):
            if(y==1 and gamePosition[x][y+1]==0 and gamePosition[x][y+2]==0):
                listOfPath.add((x, y+1))
                listOfPath.add((x, y+2))
            if(y+1<=7 and gamePosition[x][y+1]==0):
                listOfPath.add((x, y+1))
            if(y+1<=7 and x-1>=0 and gamePosition[x-1][y+1]!=0 and gamePosition[x-1][y+1][0]=='w'):
                listOfPath.add((x-1, y+1))
            if(y+1<=7 and x+1<=7 and gamePosition[x+1][y+1]!=0 and gamePosition[x+1][y+1][0]=='w'):
                listOfPath.add((x+1, y+1))

    # Rook Movement
    if(peice[1]=='R'):  #Rook Movement
        for i in [-1, 1]:  # horizontal movement
            kx = x
            while True:
                # print(kx)
                kx = kx + i
                if(kx<0 or kx>7):
                    break
                if(gamePosition[kx][y]==0):
                    listOfPath.add((kx, y))
                elif(gamePosition[kx][y][0]!=peice[0]):
                    listOfPath.add((kx, y))
                    break
                else:
                    break

        for i in [-1, 1]:  # Vertical movement
            ky = y
            while True:
                ky = ky + i
                if(ky<0 or ky>7):
                    break
                if(gamePosition[x][ky]==0):
                    listOfPath.add((x, ky))
                elif(gamePosition[x][ky][0]!=peice[0]):
                    listOfPath.add((x, ky))
                    break
                else:
                    break

    # Bishop Movement
    if(peice[1]=='B'):  #Bishop Movement
        for i in [-1, 1]:  # horizontal movement
            for j in [-1, 1]:
                ky = y
                kx = x
                while True:
                    kx = kx + i
                    ky = ky + j
                    if(ky<0 or kx<0 or ky>7 or kx>7):
                        break
                    if(gamePosition[kx][ky]==0):
                        listOfPath.add((kx, ky))
                    elif(gamePosition[kx][ky][0]!=peice[0]):
                        listOfPath.add((kx, ky))
                        break
                    else:
                        break

    # Queen Movement
    if(peice[1]=='Q'):
        a = findLegalPath(gamePosition, x, y, peice[0]+'B')
        b = findLegalPath(gamePosition, x, y, peice[0]+'R')
        listOfPath.update(a)
        listOfPath.update(b)

    # Knight Movement
    if(peice[1]=='N'):
        for i in [-1, 1, -2, 2]:
            for j in [-1, 1, -2, 2]:
                kx = x+i
                ky = y+j
                if(abs(i)!=abs(j) and kx>=0 and kx<=7 and ky>=0 and ky<=7):
                    if(gamePosition[kx][ky]==0 or (gamePosition[kx][ky]!=0 and peice[0]!=gamePosition[kx][ky][0])):
                        listOfPath.add((kx, ky))

    # King Movement
    if(peice[1]=='K'):
        for i in [0, 1, -1]:
            for j in [0, 1, -1]:
                kx = x+i
                ky = y+j
                if(abs(i)+abs(j)!=0 and kx>=0 and kx<=7 and ky>=0 and ky<=7):
                    if(gamePosition[kx][ky]==0 or (peice[0]!=gamePosition[kx][ky][0])):
                        listOfPath.add((kx, ky))

        # Check for Castling of white King
        if(whiteKingCastling[1] and whiteKingCastling[0]+whiteKingCastling[2] and peice[0]=='w'):
            if(whiteKingCastling[0] and gamePosition[1][7]==0 and gamePosition[2][7]==0 and gamePosition[3][7]==0):
                listOfPath.add(('L', 'w'))
            if(whiteKingCastling[0] and gamePosition[5][7]==0 and gamePosition[6][7]==0):
                listOfPath.add(('R', 'w'))

        # Check for Castling of Black King
        if(blackKingCastling[1] and blackKingCastling[0]+blackKingCastling[2] and peice[0]=='b'):
            if(blackKingCastling[0] and gamePosition[1][0]==0 and gamePosition[2][0]==0 and gamePosition[3][0]==0):
                listOfPath.add(('L', 'b'))
            if(blackKingCastling[0] and gamePosition[5][0]==0 and gamePosition[6][0]==0):
                listOfPath.add(('R', 'b'))


    return listOfPath

def Cloning(li1): 
    li_copy = [] 
    li_copy.extend(li1) 
    return li_copy 

def getBoardScore(gamePosition):
    peiceScoreDict = {'wP':10, 'wN':20, 'wB':20, 'wR':30, 'wQ':50, 'wK':60, 'bP':-10, 'bN':-20, 'bB':-20, 'bR':-30, 'bQ':-50, 'bK':-60}
    score = 0
    # print(gamePosition)
    for i in range(0, 8):
        for j in range(0, 8):
            # print(i, j)
            if(gamePosition[i][j]!=0):
                score += peiceScoreDict[gamePosition[i][j]]
    return int(score)



run = True
drag = False
orignalX = None
orignalY = None
dragPeice = 0
click = None
legalPath = None
turnCount=0
peiceChance = ['w', 'b']
whiteKingCastling = [1,1,1]  # left rook, king, right Rook  ((0,7), (4,7), (7,7))
blackKingCastling = [1,1,1]
while(run):

    orignalX = -1
    orignalY = -1
    dragPeice = 0
    legalPath = None

    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            run = False
        if(event.type == pygame.MOUSEBUTTONUP):
            # print("CLICK")
            click=True
            orignalX, orignalY = pygame.mouse.get_pos()
            
   
    
   
    if(orignalX>=0 and orignalY>=0 and click==True):
        orignalX/=80; orignalY/=80;
        orignalX=int(orignalX); orignalY=int(orignalY); 
        # print(orignalX, orignalY)
        dragPeice = gamePosition[orignalX][orignalY]

    # print("SCORE --> ", getBoardScore(gamePosition))
    if(dragPeice!=0 and dragPeice[0]==peiceChance[turnCount%2]):
        # MOUSE is being clicked drag the peice which is being used
        drag = True
        # FIND all Legal Path for the Peice
        legalPath = findLegalPath(gamePosition, orignalX, orignalY, dragPeice)
        
        while(drag):
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    run = False
                    drag = False
                if(event.type == pygame.MOUSEBUTTONUP):
                    finalX, finalY = pygame.mouse.get_pos()
                    finalX = int(finalX/80)
                    finalY = int(finalY/80)
                    drag = False
            
            gamePosition[orignalX][orignalY] = 0
            x, y = pygame.mouse.get_pos()
            DrawChessBoard(gamePosition, True, x-40, y-40, dragPeice, legalPath)
       

        # print(dragPeice)

        if (finalX, finalY) in legalPath:
            # A Legal move is made
            # Place the peice on Legal Path
            mixer.music.load('F:\\softwareDev\\game_dev\\chess\\sprites\\woodSound.mp3')
            mixer.music.play()
            gamePosition[finalX][finalY] = dragPeice
            turnCount += 1
            # check Catling Rights of white King
            if(whiteKingCastling[0] and dragPeice=='wR' and orignalX==0 and orignalY==7):
                whiteKingCastling[0]=0
            if(whiteKingCastling[1] and dragPeice=='wK' and orignalX==4 and orignalY==7):
                whiteKingCastling[1]=0
            if(whiteKingCastling[2] and dragPeice=='wR' and orignalX==7 and orignalY==7):
                whiteKingCastling[2]=0

            # Check For black King Castling Rights
            if(whiteKingCastling[0] and dragPeice=='bR' and orignalX==0 and orignalY==0):
                whiteKingCastling[0]=0
            if(whiteKingCastling[1] and dragPeice=='bK' and orignalX==4 and orignalY==0):
                whiteKingCastling[0]=0
            if(whiteKingCastling[2] and dragPeice=='bR' and orignalX==7 and orignalY==0):
                whiteKingCastling[0]=0


        elif(dragPeice[1]=='K' and abs(finalX-orignalX)==2):
            # A LEGAL MOVE IS MADE
            # print('whiteKingCastling', whiteKingCastling)
            if(dragPeice[0]=='w' ):
                turnCount+=1
                whiteKingCastling[1]=0
                if(finalX==6):
                    gamePosition[6][7]='wK'
                    gamePosition[5][7]='wR'
                    gamePosition[4][7]=0
                    gamePosition[7][7]=0
                if(finalX==2):
                    gamePosition[2][7]='wK'
                    gamePosition[3][7]='wR'
                    gamePosition[0][7]=0
                    gamePosition[4][7]=0

            if(dragPeice[0]=='b'):
                turnCount+=1
                blackKingCastling[1]=0
                if(finalX==6):
                    gamePosition[6][0]='bK'
                    gamePosition[5][0]='bR'
                    gamePosition[4][0]=0
                    gamePosition[7][0]=0
                if(finalX==2):
                    gamePosition[2][0]='bK'
                    gamePosition[3][0]='bR'
                    gamePosition[0][0]=0
                    gamePosition[4][0]=0



        else:
            # Place the peice back to its  orignal position
            gamePosition[orignalX][orignalY] = dragPeice

    DrawChessBoard(gamePosition, False)

