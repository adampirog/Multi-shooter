import socket
import pickle
import random
import threading
from Player import Player
from Network import PACKAGE_SIZE


players = {}
players_lock = threading.Lock()


def add_new_player():
    global players
    
    with players_lock:
        new_id = len(players)
        players[new_id] = (Player(new_id, random.randint(100, 400), random.randint(100, 400)))
        players_copy = players
        
    return new_id, players_copy
            

def client_thread_function(connection):
    global players
    
    my_id, reply = add_new_player()
    connection.send(pickle.dumps((my_id, reply), protocol=pickle.HIGHEST_PROTOCOL))
    
    while True:
        try:
            raw_data = connection.recv(PACKAGE_SIZE)
            if(not raw_data):
                break
            
            data = pickle.loads(raw_data)
            
            with players_lock:
                players[my_id] = data[1]
                reply = players
                
            connection.sendall(pickle.dumps(reply, protocol=pickle.HIGHEST_PROTOCOL))
        
        except Exception:
            break
        
    print("Player disconnected")
    with players_lock:
        players.pop(my_id)

    connection.close()


def main():
    server = "192.168.1.25"
    port = 5555
    running = True
    maxPlayers = 3

    open_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        open_socket.bind((server, port))
    except socket.error as e:
        print(str(e))

    open_socket.listen()
    print("Server started, waiting for connection")

    while running:
        if(len(players) < maxPlayers):
            connection, address = open_socket.accept()
            print("Connected to: ", address)

            client_thread = threading.Thread(target=client_thread_function, args=[connection])
            client_thread.start()


if __name__ == "__main__":
    main()
