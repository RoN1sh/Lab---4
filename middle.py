from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pickle
# поле + ракетки + м'яч + механіка(для клави) + рахунок
import turtle  # для графіки
import winsound  # для музики
import initialize
import threading

BUFSIZ = 1024
score_for1 = 0
score_for2 = 0

window = initialize.window(600, 600)
ball = initialize.ball()
score = initialize.score()

def receive():
    global score_for1
    global score_for2
    while True:
        msg = client_socket.recv(BUFSIZ)
        state = pickle.loads(msg)
        ball.setx(state.ballX)
        ball.sety(state.ballY)
        score_for1 = state.scoreLeft
        score_for2 =  state.scoreRight
        window.update()

def drawScore():
    score.clear()
    score.write("Player A: {}  Player B: {}".format(score_for1, score_for2), align="center", font=("Arial", 30))
    threading.Timer(1, drawScore).start()

window.update()
window.listen()

print("MIDDLE field")
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)
if not HOST:
    HOST = "127.0.0.1"

drawScore()
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket.send(bytes("MIDDLE", "utf8"))
receive_thread = Thread(target=receive)
receive_thread.start()
window.mainloop()