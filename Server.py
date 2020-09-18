import socket
import pickle
import random
import threading
from Player import Player, SPAWN_AREAS, detect_players_collision
from Network import PACKAGE_SIZE


players = {}
players_lock = threading.Lock()

item_spawn_zones = []


def add_new_player():
    global players
    
    with players_lock:
        new_id = len(players)
        if new_id % 2 == 0:
            x, y = random.randint(SPAWN_AREAS[0][0], SPAWN_AREAS[0][1]), random.randint(SPAWN_AREAS[1][0], SPAWN_AREAS[1][1])
            if(detect_players_collision(x, y, new_id, players)):
                while(detect_players_collision(x, y, new_id, players)):
                    x, y = random.randint(SPAWN_AREAS[0][0], SPAWN_AREAS[0][1]), random.randint(SPAWN_AREAS[1][0], SPAWN_AREAS[1][1])
        else:
            x, y = random.randint(SPAWN_AREAS[1][0], SPAWN_AREAS[1][1]), random.randint(SPAWN_AREAS[0][0], SPAWN_AREAS[0][1])
            if(detect_players_collision(x, y, new_id, players)):
                while(detect_players_collision(x, y, new_id, players)):
                    x, y = random.randint(SPAWN_AREAS[0][0], SPAWN_AREAS[0][1]), random.randint(SPAWN_AREAS[1][0], SPAWN_AREAS[1][1])
            
        players[new_id] = Player(new_id, x, y)
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
                reply = (players, item_spawn_zones)
                
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
