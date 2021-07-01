import socket
import pickle
import random
import time
import threading
from Player import Player, SPAWN_AREAS, detect_players_collision
from Network import PACKAGE_SIZE


players = {}
players_lock = threading.Lock()

item_spawn_zones = [[0, 300, 300], [1, 700, 700], [2, 100, 900], [3, 900, 100]]
spawn_timer = time.time()
SPAWN_INTERVAL = 10


def spawn_item():
    global spawn_timer, item_spawn_zones
    
    if (time.time() - spawn_timer >= SPAWN_INTERVAL):
        spawn_timer = time.time()
                
        free_slots = [index for index, zone in enumerate(item_spawn_zones) if zone[0] is None]
        if(len(free_slots) == 0):
            return 
            
        item_spawn_zones[random.choice(free_slots)][0] = random.randint(0, 3)
        

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
        items_copy = item_spawn_zones
        
    return new_id, players_copy, items_copy
            

def client_thread_function(connection):
    global players, item_spawn_zones
    
    my_id, reply1, reply2 = add_new_player()
    connection.send(pickle.dumps((my_id, reply1, reply2), protocol=pickle.HIGHEST_PROTOCOL))
    
    while True:
        try:
            raw_data = connection.recv(PACKAGE_SIZE)
            if(not raw_data):
                break
            
            data = pickle.loads(raw_data)
            
            with players_lock:
                players[my_id] = data[1]
                item_spawn_zones = data[2]
                spawn_item()
                reply = (players, item_spawn_zones)
                
            connection.sendall(pickle.dumps(reply, protocol=pickle.HIGHEST_PROTOCOL))
        
        except Exception:
            break
        
    print("Player disconnected")
    with players_lock:
        players.pop(my_id)

    connection.close()


def main():
    server = "192.168.1.16"
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
