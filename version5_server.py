import socket
import time
import pickle
from _thread import *
from myClasses import GamePosition

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1243))
s.listen(5)

board = [['bR', 'bP', 0, 0, 0, 0, 'wP', 'wR'],
        ['bN', 'bP', 0, 0, 0, 0, 'wP', 'wN'],
        ['bB', 'bP', 0, 0, 0, 0, 'wP', 'wB'],
        ['bQ', 'bP', 0, 0, 0, 0, 'wP', 'wQ'],
        ['bK', 'bP', 0, 0, 0, 0, 'wP', 'wK'],
        ['bB', 'bP', 0, 0, 0, 0, 'wP', 'wB'],
        ['bN', 'bP', 0, 0, 0, 0, 'wP', 'wN'],
        ['bR', 'bP', 0, 0, 0, 0, 'wP', 'wR'] ]

currentGame = GamePosition(board, 0, [1,1,1], [1,1,1])

def threaded_client(clientsocket, player):
    global currentGame
    sendPos = pickle.dumps(currentGame)
    clientsocket.send(sendPos)
    while True:
        recPos = clientsocket.recv(2048)
        recPos = pickle.loads(recPos)
        if(recPos.player>currentGame.player and player==currentGame.player%2):
            currentGame = recPos
        sendPos = pickle.dumps(currentGame)
        clientsocket.send(sendPos)

currentPlayer = 0
while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    start_new_thread(threaded_client, (clientsocket, currentPlayer))
    currentPlayer+=1