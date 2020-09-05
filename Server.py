import socket
from _thread import start_new_thread
from Classes import Player
import pickle
import threading
import random

players = []
players_lock = threading.Lock()


def add_new_player():
    global players
    
    with players_lock:
        new_id = len(players)
        players.append(Player(new_id, (random.randint(100, 400), random.randint(100, 400))))
        
    return new_id


def client_thread(conn, player):
    global players
    
    new_id = add_new_player()
    conn.send(pickle.dumps([new_id, players], protocol=pickle.HIGHEST_PROTOCOL))
    reply = ""
    
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            new_id = data[0]
            with players_lock:
                players[new_id] = data[1]
            
            if not data:
                print("Disconnected")
                break
            else:
                with players_lock:
                    reply = players
                
            conn.sendall(pickle.dumps(reply, protocol=pickle.HIGHEST_PROTOCOL))
        
        except Exception:
            break
        
    print("Lost connection")
    conn.close()


def main():
    server = "192.168.1.25"
    port = 5555
    maxPlayers = 2
    currentPlayers = 0

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((server, port))
    except socket.error as e:
        print(str(e))

    s.listen(maxPlayers)
    print("Server started, waiting for connection")

    while True:
        conn, addr = s.accept()
        print("Connected to: ", addr)

        start_new_thread(client_thread, (conn, currentPlayers))
        currentPlayers += 1


if __name__ == "__main__":
    main()
