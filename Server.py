import socket
import pickle
import random
import threading
from Classes import Player, GROUND_LVL, WIDTH, HEIGHT, PLAYER_HEIGHT

players = []
players_lock = threading.Lock()


def add_new_player():
    global players
    
    with players_lock:
        new_id = len(players)
        players.append(Player(new_id, random.randint(50, WIDTH - 50), HEIGHT - GROUND_LVL - PLAYER_HEIGHT))
        
    return new_id


def create_packages():
    package_list = []
    with players_lock:
        for player in players:
            package_list.append(player.export_package())    
    
    return package_list


def client_thread_function(connection):
    # message contains (client_id, info_package)
    
    my_id = add_new_player()
    reply = create_packages()
    connection.send(pickle.dumps([my_id, reply], protocol=pickle.HIGHEST_PROTOCOL))
    
    while True:
        try:
            data = pickle.loads(connection.recv(2048))
            player_id = data[0]
            with players_lock:
                players[player_id].import_package(data[1])
            
            if not data:
                break
            else:
                reply = create_packages()
                
            connection.sendall(pickle.dumps(reply, protocol=pickle.HIGHEST_PROTOCOL))
        
        except Exception:
            break
        
    print("Client disconnected")
    players.pop(my_id)
    connection.close()


def main():
    server = "192.168.1.25"
    port = 5555
    maxPlayers = 2
    running = True

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
