# Draw Board
# Date - 02/12/2020
# objected oriented implementation of Board
# Server Client Application

import socket
import pickle
import pygame
from pygame import mixer
import copy
import os
import pickle
import sys
from myClasses import GamePosition

pygame.init()
mixer.init()

boardSize=(640, 640)
mainBoard = pygame.display.set_mode(size=boardSize)
boardImg  = pygame.image.load(os.path.join('sprites', 'myboard.png')).convert_alpha()
boardImg  = pygame.transform.scale(boardImg, (640, 640))
peiceImg  = pygame.image.load(os.path.join('sprites', 'peicesImg.png')).convert_alpha()
peiceImg  = pygame.transform.scale(peiceImg, (480, 160))
redCircle = pygame.image.load(os.path.join('sprites', 'red_circle.png'))
redCircle = pygame.transform.scale(redCircle, (20, 20))
peiceDict = {'b':80, 'w':0, 'K':0, 'Q':80, 'B':160, 'N':240, 'R':320, 'P':400}


board = [['bR', 'bP', 0, 0, 0, 0, 'wP', 'wR'],
        ['bN', 'bP', 0, 0, 0, 0, 'wP', 'wN'],
        ['bB', 'bP', 0, 0, 0, 0, 'wP', 'wB'],
        ['bQ', 'bP', 0, 0, 0, 0, 'wP', 'wQ'],
        ['bK', 'bP', 0, 0, 0, 0, 'wP', 'wK'],
        ['bB', 'bP', 0, 0, 0, 0, 'wP', 'wB'],
        ['bN', 'bP', 0, 0, 0, 0, 'wP', 'wN'],
        ['bR', 'bP', 0, 0, 0, 0, 'wP', 'wR'] ]




def drawBoard(curGamePos, legalPath=[], drag=False, dragPeice=None):
    global boardImg; global peiceImg; global redCircle; global mainBoard; global peiceDict; global boardSize;
    mainBoard.blit(boardImg, (0,0))  # draws the main board
    board = curGamePos.board
    for i in range(0, 8):  # draws chess peices on board
        for j in range(0, 8):
            if(board[i][j]!=0):
                peiceColor = peiceDict[board[i][j][0]]
                peiceType  = peiceDict[board[i][j][1]]
                mainBoard.blit(peiceImg, (i*80, j*80), (peiceType,peiceColor,80,80))

    if(drag):
        dragPeiceColor = peiceDict[dragPeice[0]]
        dragPeiceType  = peiceDict[dragPeice[1]]
        x, y = pygame.mouse.get_pos()
        mainBoard.blit(peiceImg, (x-40, y-40), (dragPeiceType,dragPeiceColor,80,80))

    for cord in legalPath:
        mainBoard.blit(redCircle, (cord[0]*80+30, cord[1]*80+30))
    pygame.display.update()


def rawBoard(curGamePos):
    board = curGamePos.board
    for i in board:
        print(i)
    print('\n\n')

def opp(col):
    if(col=='w'):
        return 'b'
    return 'w' 

def cordToPos(pos):
    a, b = pos
    if(a<0 or b<0 or a>640 or b>640):
        return None, None
    return int(a/80), int(b/80)

def lookFor(curGamePos, peice):
    listOfPos = []
    board = curGamePos.board
    for i in range(0, 8):
        for j in range(0, 8):
            if(board[i][j]==peice):
                listOfPos.append((i, j))
    return listOfPos

def attackedSquares(curGamePos, col):
    board = curGamePos.board
    listOfAttackedSquares = []
    for i in range(0, 8):
        for j in range(0, 8):
            if(board[i][j]!=0 and board[i][j][0]==col):
                listOfAttackedSquares.extend(findLegalPath(curGamePos, i, j, board[i][j], True))
    # print(listOfAttackedSquares)
    return listOfAttackedSquares

def isCheck(curGamePos, col):
    peice = col+'K'
    x, y = lookFor(curGamePos, peice)[0]
    if((x, y) in attackedSquares(curGamePos, opp(col))):
        return True
    return False


def findLegalPath(curGamePos, x, y, peice, attackSearch=False):
    # Finds the legal path of the peice being draged 
    # print(peice)
    board = curGamePos.board
    listOfPath = set()
    col = peice[0]
    # Pawn Movement
    if(peice[1]=='P'):   
        if(peice[0]=='w'):
            if(y==6 and board[x][y-1]==0 and board[x][y-2]==0):
                listOfPath.add((x, y-1))
                listOfPath.add((x, y-2))
            if(y-1>=0 and board[x][y-1]==0):
                listOfPath.add((x, y-1))
            if(y-1>=0 and x-1>=0 and board[x-1][y-1]!=0 and board[x-1][y-1][0]=='b'):
                listOfPath.add((x-1, y-1))
            if(y-1>=0 and x+1<=7 and board[x+1][y-1]!=0 and board[x+1][y-1][0]=='b'):
                listOfPath.add((x+1, y-1))

        if(peice[0]=='b'):
            if(y==1 and board[x][y+1]==0 and board[x][y+2]==0):
                listOfPath.add((x, y+1))
                listOfPath.add((x, y+2))
            if(y+1<=7 and board[x][y+1]==0):
                listOfPath.add((x, y+1))
            if(y+1<=7 and x-1>=0 and board[x-1][y+1]!=0 and board[x-1][y+1][0]=='w'):
                listOfPath.add((x-1, y+1))
            if(y+1<=7 and x+1<=7 and board[x+1][y+1]!=0 and board[x+1][y+1][0]=='w'):
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
                if(board[kx][y]==0):
                    listOfPath.add((kx, y))
                elif(board[kx][y][0]!=peice[0]):
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
                if(board[x][ky]==0):
                    listOfPath.add((x, ky))
                elif(board[x][ky][0]!=peice[0]):
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
                    if(board[kx][ky]==0):
                        listOfPath.add((kx, ky))
                    elif(board[kx][ky][0]!=peice[0]):
                        listOfPath.add((kx, ky))
                        break
                    else:
                        break

    # Queen Movement
    if(peice[1]=='Q'):
        a = findLegalPath(curGamePos, x, y, peice[0]+'B', True)
        b = findLegalPath(curGamePos, x, y, peice[0]+'R', True)
        listOfPath.update(a)
        listOfPath.update(b)

    # Knight Movement
    if(peice[1]=='N'):
        for i in [-1, 1, -2, 2]:
            for j in [-1, 1, -2, 2]:
                kx = x+i
                ky = y+j
                if(abs(i)!=abs(j) and kx>=0 and kx<=7 and ky>=0 and ky<=7):
                    if(board[kx][ky]==0 or (board[kx][ky]!=0 and peice[0]!=board[kx][ky][0])):
                        listOfPath.add((kx, ky))

    # King Movement
    if(peice[1]=='K'):
        for i in [0, 1, -1]:
            for j in [0, 1, -1]:
                kx = x+i
                ky = y+j
                if(abs(i)+abs(j)!=0 and kx>=0 and kx<=7 and ky>=0 and ky<=7):
                    if(board[kx][ky]==0 or (peice[0]!=board[kx][ky][0])):
                        listOfPath.add((kx, ky))

        # Check for Castling of white King
        white = curGamePos.whiteCastling
        black = curGamePos.blackCastling
        if(white[1] and white[0]+white[2] and peice[0]=='w'):
            if(white[0] and board[1][7]==0 and board[2][7]==0 and board[3][7]==0):
                listOfPath.add((2, 7))
            if(white[2] and board[5][7]==0 and board[6][7]==0):
                listOfPath.add((6, 7))

        # Check for Castling of Black King
        if(black[1] and black[0]+black[2] and peice[0]=='b'):
            if(black[0] and board[1][0]==0 and board[2][0]==0 and board[3][0]==0):
                listOfPath.add((2, 0))
            if(black[2] and board[5][0]==0 and board[6][0]==0):
                listOfPath.add((6, 0))

    # remove if the peice movement leading to check
    if(attackSearch==False):
        # print(peice, " ", (ix, iy), " --> ", listOfPath, "\n\n")
        newList=[]
        for tup in listOfPath:
            fx, fy = tup
            dupGamePos = curGamePos.clone()
            makeMove(dupGamePos, x, y, fx, fy)
            # rawBoard(dupGamePos)
            if not isCheck(dupGamePos, col):
                newList.append(tup)
        listOfPath=newList

    return listOfPath


def makeMove(curGamePos, ix, iy, fx, fy):
    board = curGamePos.board
    peice = curGamePos.getPeice(ix, iy)
    castling = curGamePos.castlingRights
    white = curGamePos.whiteCastling
    black = curGamePos.blackCastling
    player = curGamePos.player
    # King movement
    if(peice[1]=='K'):
        # wK   {(5, 7), (6, 7)}
        # print("run", fx-ix)
        curGamePos.castlingRights[player%2][1]=0
        if(abs(fx-ix)==2):
            if(fx==2):   # long catling
                board[fx][fy] = peice
                board[fx+1][fy] = curGamePos.getPeice(0, fy)
                board[0][fy] = 0
            if(fx==6):   # short catling
                
                board[fx][fy] = peice
                board[fx-1][fy] = curGamePos.getPeice(7, fy)
                board[7][fy] = 0
            board[ix][iy]=0
        else:
            board[fx][fy] = peice
            board[ix][iy] = 0    
        
    else:
        if((ix==0 and iy==7) or (fx==0 and fy==7)):
            white[0]=0
        elif((ix==7 and iy==7) or (fx==7 and fy==7)):
            white[2]=0
        if((ix==0 and iy==0) or (fx==0 and fy==0)):
            black[0]=0
        elif((ix==7 and iy==0) or (fx==7 and fy==0)):
            black[2]=0
        board[fx][fy] = peice
        board[ix][iy] = 0


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1243))

recPos = s.recv(2048)
currentGame = pickle.loads(recPos)
run = True
drag = False
ix = None
iy = None
dragPeice = 0
downClick = False
upClick = False
legalPath = None
peiceChance = ['w', 'b']
AiGamePos = None

##################### MAIN LOOP ##############################################################################

while(run):

    if(downClick==False):
        iX = -1
        iY = -1
    if(upClick==False):
        fX = -1
        fY = -1
    dragPeice = 0
    legalPath = None

    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            run = False
        if(event.type == pygame.MOUSEBUTTONDOWN):
            # clicke down
            upClick = False
            ix, iy = cordToPos(pygame.mouse.get_pos())
            if(ix!=None):
                downClick = True
        
        if(event.type == pygame.MOUSEBUTTONUP):
            # click released
            downClick = False
            fx, fy = cordToPos(pygame.mouse.get_pos())
            if(fx!=None):
                upClick = True
   
    sendPos = pickle.dumps(currentGame)
    s.send(sendPos)
    recPos = s.recv(2048)
    currentGame = pickle.loads(recPos)
    
    if(downClick): 
        board = currentGame.board
        peice = currentGame.getPeice(ix, iy)
        if(peice!=0 and peice[0]==peiceChance[currentGame.player%2]):   # curGamePos, legalPath, drag=False, dragPeice=None
            # player clicked on a valid peice
            legalPath = findLegalPath(currentGame, ix, iy, board[ix][iy])
            varPeice = board[ix][iy]
            board[ix][iy] = 0
            drawBoard(currentGame, legalPath, True, peice)
            board[ix][iy] = varPeice
        else:
            downClick=False
            ix=-1; iy=-1
    elif(upClick):
        board = currentGame.board
        peice = currentGame.getPeice(ix, iy)
        if(peice!=0 and peice[0]==peiceChance[currentGame.player%2]):
            legalPath = findLegalPath(currentGame, ix, iy, board[ix][iy])
            if((fx, fy) in legalPath):
                makeMove(currentGame, ix, iy, fx, fy)
                currentGame.player+=1
        legalPath=[]
        drawBoard(currentGame)
        upClick=False
        downClick=False
    else:
        drawBoard(currentGame)





   