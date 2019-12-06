from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pickle
# поле + ракетки + м'яч + механіка(для клави) + рахунок
import turtle  # для графіки
import winsound  # для музики
import initialize

BUFSIZ = 1024

window = initialize.window(600, 600)
raketka = initialize.player(1)
ball = initialize.ball()
ball.setx(600)

def receive():
    while True:
        msg = client_socket.recv(BUFSIZ)
        state = pickle.loads(msg)
        raketka.sety(state.leftPlayerY)
        ball.setx(state.ballX+600)
        ball.sety(state.ballY)
        window.update()

# Функції для руху ракеток
def racket_up():
    client_socket.send(bytes("UP", "utf8"))

def racket_down():
    client_socket.send(bytes("DOWN", "utf8"))

# Клавіші для управління ракетками
window.onkey(racket_up, "w")
window.onkey(racket_down, "s")
window.update()
window.listen()

print("LEFT player")
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)
if not HOST:
    HOST = "127.0.0.1"

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket.send(bytes("LEFT", "utf8"))

receive_thread = Thread(target=receive)
receive_thread.start()
window.mainloop()