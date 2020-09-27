# Date Started --> 22/08/2020

import pygame
import collections

pygame.init()

boardColor = [(153,76,0), (255,153,51)]
boardSize = (400,500)
whitePawn = pygame.image.load("whitePawn.png")
whitePawn = pygame.transform.scale(whitePawn, (40, 40))
whiteRook = pygame.image.load("whiteRook.png")
whiteRook = pygame.transform.scale(whiteRook, (40, 40))
whiteBishop = pygame.image.load("whiteBishop.png")
whiteBishop = pygame.transform.scale(whiteBishop, (40, 40))
whiteKing = pygame.image.load("whiteKing.png")
whiteKing = pygame.transform.scale(whiteKing, (40, 40))
whiteQueen = pygame.image.load("whiteQueen.png")
whiteQueen = pygame.transform.scale(whiteQueen, (40, 40))
whiteKnight = pygame.image.load("whiteKnight.png")
whiteKnight = pygame.transform.scale(whiteKnight, (40, 40))

blackPawn = pygame.image.load("blackPawn.png")
blackPawn = pygame.transform.scale(blackPawn, (40, 40))
blackRook = pygame.image.load("blackRook.png")
blackRook = pygame.transform.scale(blackRook, (40, 40))
blackBishop = pygame.image.load("blackBishop.png")
blackBishop = pygame.transform.scale(blackBishop, (40, 40))
blackKing = pygame.image.load("blackKing.png")
blackKing = pygame.transform.scale(blackKing, (40, 40))
blackQueen = pygame.image.load("blackQueen.png")
blackQueen = pygame.transform.scale(blackQueen, (40, 40))
blackKnight = pygame.image.load("blackKnight.png")
blackKnight = pygame.transform.scale(blackKnight, (40, 40))


peicePos = [[blackRook, blackKnight, blackBishop, blackQueen, blackKing, blackBishop, blackKnight, blackRook],
            [blackPawn,blackPawn,blackPawn,blackPawn,blackPawn,blackPawn,blackPawn,blackPawn],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [whitePawn,whitePawn,whitePawn,whitePawn,whitePawn,whitePawn,whitePawn,whitePawn],
            [whiteRook, whiteKnight, whiteBishop, whiteQueen, whiteKing, whiteBishop, whiteKnight, whiteRook] ]




def drawBoard(showPeicePath, pathList):
    mainBoard = pygame.display.set_mode(size=boardSize)
    for i in range(0, 8):
        for j in range(0, 8):
            # coloring Board
            pygame.draw.rect(mainBoard, boardColor[(i+j+1)%2], (j*50,i*50,50,50))
            if(peicePos[i][j]==0):
                continue
            # adding Peices
            mainBoard.blit(peicePos[i][j], (j*50+5,i*50+5))        
    
    if(showPeicePath):
        for cord in pathList:
            pygame.draw.circle(mainBoard, (0,255,0), [cord[0]*50+25, cord[1]*50+25], 5)


    pygame.display.update()         

def legalPath(givenPeice, x, y):
    cord = []
    # print(x, y)
    # print(x, y-1)
    # print(peicePos[y-1][x])
    if(givenPeice == whitePawn): # White Pawn
        if(peicePos[y-1][x]==0):
            cord.append([x, y-1])
        if(y==6 and peicePos[y-2][x]==0):
            cord.append([x, y-2])

    elif(givenPeice == blackPawn): # Black Pawn
        if(peicePos[y+1][x]==0):
            cord.append([x, y+1])
        if(y==1 and peicePos[y+2][x]==0):
            cord.append([x, y+2])

    if(givenPeice == whiteKnight): # White Knight
        for i in range(-2, 3):
            if(i==0):
                continue
            for j in range(-2, 3):
                if(abs(i)==abs(j) or j==0):
                    continue
                x1 = x+i
                y1 = y+j
                if(x+i>=0 and x+i<8 and y+j>=0 and y+j<8 and peicePos[y1][x1]!=whiteKnight and peicePos[y1][x1]!=whiteRook and peicePos[y1][x1]!=whitePawn and peicePos[y1][x1]!=whiteBishop and peicePos[y1][x1]!=whiteQueen and peicePos[y1][x1]!=whiteKing):
                    cord.append([x1, y1])   

    if(givenPeice == blackKnight):  # Black Knigh
        for i in range(-2, 3):
            if(i==0):
                continue
            for j in range(-2, 3):
                if(abs(i)==abs(j) or j==0):
                    continue
                x1 = x+i
                y1 = y+j
                if(x+i>=0 and x+i<8 and y+j>=0 and y+j<8 and peicePos[y1][x1]!=blackKnight and peicePos[y1][x1]!=blackRook and peicePos[y1][x1]!=blackPawn and peicePos[y1][x1]!=blackBishop and peicePos[y1][x1]!=blackQueen and peicePos[y1][x1]!=blackKing):
                    cord.append([x1, y1])

    if(givenPeice == whiteRook): # WHite ROOK
        a = 1
        while(x-a>=0):
            if(peicePos[y][x-a]==0):
                cord.append([x-a,y])
            elif(peicePos[y][x-a]==blackPawn or peicePos[y][x-a]==blackQueen or peicePos[y][x-a]==blackRook or peicePos[y][x-a]==blackBishop or peicePos[y][x-a]==blackKnight or peicePos[y][x-a]==blackKing):
                cord.append([x-a,y])
                break
            else:
                break
            print(peicePos[y][x-a])
            a+=1

        a=1
        while(x+a<8):
            if(peicePos[y][x+a]==0):
                cord.append([x+a,y])
            elif(peicePos[y][x+a]==blackPawn or peicePos[y][x+a]==blackQueen or peicePos[y][x+a]==blackRook or peicePos[y][x+a]==blackBishop or peicePos[y][x+a]==blackKnight or peicePos[y][x+a]==blackKing):
                cord.append([x+a,y])
                break
            else:
                break
            print(peicePos[y][x+a])
            a+=1

        a=1
        while(y+a<8):
            if(peicePos[y+a][x]==0):
                cord.append([x,y+a])
            elif(peicePos[y+a][x]==blackPawn or peicePos[y+a][x]==blackQueen or peicePos[y+a][x]==blackRook or peicePos[y+a][x]==blackBishop or peicePos[y+a][x]==blackKnight or peicePos[y+a][x]==blackKing):
                cord.append([x,y+a])
                break
            else:
                break
            print(peicePos[y+a][x])
            a+=1

        a=1
        while(y-a>=0):
            if(peicePos[y-a][x]==0):
                cord.append([x,y-a])
            elif(peicePos[y-a][x]==blackPawn or peicePos[y-a][x]==blackQueen or peicePos[y-a][x]==blackRook or peicePos[y-a][x]==blackBishop or peicePos[y-a][x]==blackKnight or peicePos[y-a][x]==blackKing):
                cord.append([x,y-a])
                break
            else:
                break
            print(peicePos[y-a][x])
            a+=1

    if(givenPeice == blackRook): # Black ROOK
        a = 1
        while(x-a>=0):
            if(peicePos[y][x-a]==0):
                cord.append([x-a,y])
            elif(peicePos[y][x-a]==whitePawn or peicePos[y][x-a]==whiteQueen or peicePos[y][x-a]==whiteRook or peicePos[y][x-a]==whiteBishop or peicePos[y][x-a]==whiteKnight or peicePos[y][x-a]==whiteKing):
                cord.append([x-a,y])
                break
            else:
                break
            print(peicePos[y][x-a])
            a+=1

        a=1
        while(x+a<8):
            if(peicePos[y][x+a]==0):
                cord.append([x+a,y])
            elif(peicePos[y][x+a]==whitePawn or peicePos[y][x+a]==whiteQueen or peicePos[y][x+a]==whiteRook or peicePos[y][x+a]==whiteBishop or peicePos[y][x+a]==whiteKnight or peicePos[y][x+a]==whiteKing):
                cord.append([x+a,y])
                break
            else:
                break
            print(peicePos[y][x+a])
            a+=1

        a=1
        while(y+a<8):
            if(peicePos[y+a][x]==0):
                cord.append([x,y+a])
            elif(peicePos[y+a][x]==whitePawn or peicePos[y+a][x]==whiteQueen or peicePos[y+a][x]==whiteRook or peicePos[y+a][x]==whiteBishop or peicePos[y+a][x]==whiteKnight or peicePos[y+a][x]==whiteKing):
                cord.append([x,y+a])
                break
            else:
                break
            print(peicePos[y+a][x])
            a+=1

        a=1
        while(y-a>=0):
            if(peicePos[y-a][x]==0):
                cord.append([x,y-a])
            elif(peicePos[y-a][x]==whitePawn or peicePos[y-a][x]==whiteQueen or peicePos[y-a][x]==whiteRook or peicePos[y-a][x]==whiteBishop or peicePos[y-a][x]==whiteKnight or peicePos[y-a][x]==whiteKing):
                cord.append([x,y-a])
                break
            else:
                break
            print(peicePos[y-a][x])
            a+=1


    if(givenPeice == whiteBishop): # WHite BISHOP
        a = 1
        while(x-a>=0 and y-a>=0):
            if(peicePos[y-a][x-a]==0):
                cord.append([x-a,y-a])
            elif(peicePos[y-a][x-a]==blackPawn or peicePos[y-a][x-a]==blackQueen or peicePos[y-a][x-a]==blackRook or peicePos[y-a][x-a]==blackBishop or peicePos[y-a][x-a]==blackKnight or peicePos[y-a][x-a]==blackKing):
                cord.append([x-a,y-a])
                break
            else:
                break
            print(peicePos[y-a][x-a])
            a+=1

        a=1
        while(x+a<8 and y+a<8):
            if(peicePos[y+a][x+a]==0):
                cord.append([x+a,y+a])
            elif(peicePos[y+a][x+a]==blackPawn or peicePos[y+a][x+a]==blackQueen or peicePos[y+a][x+a]==blackRook or peicePos[y+a][x+a]==blackBishop or peicePos[y+a][x+a]==blackKnight or peicePos[y+a][x+a]==blackKing):
                cord.append([x+a,y+a])
                break
            else:
                break
            print(peicePos[y+a][x+a])
            a+=1

        a=1
        while(y+a<8 and x-a>=0):
            if(peicePos[y+a][x-a]==0):
                cord.append([x-a,y+a])
            elif(peicePos[y+a][x-a]==blackPawn or peicePos[y+a][x-a]==blackQueen or peicePos[y+a][x-a]==blackRook or peicePos[y+a][x-a]==blackBishop or peicePos[y+a][x-a]==blackKnight or peicePos[y+a][x-a]==blackKing):
                cord.append([x-a,y+a])
                break
            else:
                break
            print(peicePos[y+a][x-a])
            a+=1

        a=1
        while(y-a>=0 and x+a<8):
            if(peicePos[y-a][x+a]==0):
                cord.append([x+a,y-a])
            elif(peicePos[y-a][x+a]==blackPawn or peicePos[y-a][x+a]==blackQueen or peicePos[y-a][x+a]==blackRook or peicePos[y-a][x+a]==blackBishop or peicePos[y-a][x+a]==blackKnight or peicePos[y-a][x+a]==blackKing):
                cord.append([x+a,y-a])
                break
            else:
                break
            print(peicePos[y-a][x+a])
            a+=1





    print(cord)
    return cord

def movePeice(peiceMovCord):
    if(len(peiceMovCord)<2):
        return 0
    x1, y1 = peiceMovCord[-2][0], peiceMovCord[-2][1]
    x2, y2 = peiceMovCord[-1][0], peiceMovCord[-1][1]
    checkList = legalPath(peicePos[peiceMovCord[-2][1]][peiceMovCord[-2][0]], x1, y1)
    m = [x2, y2]
    for cord in checkList:
        if cord==m:
            peicePos[y2][x2] = peicePos[y1][x1]
            peicePos[y1][x1] = 0 
            showPeicePath = False 
            break;      
    


run = True
showPeicePath = False
pathList = []
peiceMovCord = []
while(run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        if pygame.mouse.get_pressed()[0]:  
            if(int(pygame.mouse.get_pos()[1]/50)<=7 and int(pygame.mouse.get_pos()[0]/50)<=7):
                # print(peicePos[int(pygame.mouse.get_pos()[1]/50)][int(pygame.mouse.get_pos()[0]/50)])  
                # print("cord --> ", int(pygame.mouse.get_pos()[1]/50), int(pygame.mouse.get_pos()[0]/50))
                pathList = legalPath(peicePos[int(pygame.mouse.get_pos()[1]/50)][int(pygame.mouse.get_pos()[0]/50)], int(pygame.mouse.get_pos()[0]/50), int(pygame.mouse.get_pos()[1]/50))
                peiceMovCord.append([int(pygame.mouse.get_pos()[0]/50), int(pygame.mouse.get_pos()[1]/50)])
                showPeicePath = True
                movePeice(peiceMovCord)

    drawBoard(showPeicePath, pathList)