from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import state
import pickle
import threading
import random

ENCODING = "utf8"
BUFSIZ = 1024
FPS = 100
gameState = state.State()
gameState.dx = 2
gameState.dy = 2

def ballMove():
    gameState.ballX += gameState.dx
    gameState.ballY += gameState.dy

    if gameState.ballY > 290 or gameState.ballY < -290:
        gameState.dy *= -1

    if gameState.ballX > 890:
        gameState.scoreLeft += 1

    if gameState.ballX < -890:
        gameState.scoreRight += 1

    if gameState.ballX > 890 or gameState.ballX < -890:
        gameState.ballX = 0
        gameState.ballY = 0
        gameState.dy *= -1
        gameState.dx *= -1

# винятки при зіткненні ракетки з м'ячем
    if (gameState.ballX > 880 and gameState.ballX < 890) and (gameState.ballY < gameState.rightPlayerY + 30 and gameState.ballY > gameState.rightPlayerY - 30):
        gameState.dx *= -1

    if (gameState.ballX < -880 and gameState.ballX > -890) and (gameState.ballY < gameState.leftPlayerY + 30 and gameState.ballY > gameState.leftPlayerY - 30):
        gameState.dx *= -1

    broadcastObject(gameState)
    threading.Timer(1/FPS, ballMove).start()

def accept_incoming_connections():
    clientNumber = 0
    while clientNumber < 3:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()
        clientNumber += 1

    threading.Timer(2, ballMove).start()


def handle_client(client):
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    clientNames[client] = name

    while True:
        msg = client.recv(BUFSIZ).decode("utf8")
        if msg == "UP" and clientNames[client] == "LEFT":
            gameState.leftPlayerY += 30
        if msg == "DOWN" and clientNames[client] == "LEFT":
            gameState.leftPlayerY -= 30
        if msg == "UP" and clientNames[client] == "RIGHT":
            gameState.rightPlayerY += 30
        if msg == "DOWN" and clientNames[client] == "RIGHT":
            gameState.rightPlayerY -= 30

        broadcastObject(gameState)

def broadcastObject(msg):
    """Broadcasts a message to all the clientNames."""
    for key in clientNames.keys():
        key.send(pickle.dumps(msg))

clientNames = {}
addresses = {}
print("SERVER")
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(('', PORT))

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

