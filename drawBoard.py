# Draw Board
# Date - 16/09/2020

import pygame
pygame.init()

class DrawChessBoard():
    def __init__(self, gamePosition):    
        import pygame
        import collections
        import os
        pygame.init()

        boardSize=(640, 640)
        mainBoard = pygame.display.set_mode(size=boardSize)
        boardImg = pygame.image.load(os.path.join('sprites', 'myboard.png')).convert_alpha()
        boardImg = pygame.transform.scale(boardImg, (640, 640))
        peiceImg = pygame.image.load(os.path.join('sprites', 'peicesImg.png')).convert_alpha()
        peiceImg = pygame.transform.scale(peiceImg, (480, 160))

        mainBoard.blit(boardImg, (0,0))
        mainBoard.blit(peiceImg, (0, 0), (0,0,480,480))   # top, left, height, width
        pygame.display.update() 



run = True
while(run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    DrawChessBoard(0)

    

      