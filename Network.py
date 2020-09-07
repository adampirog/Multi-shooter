import socket
import pickle

PACKAGE_SIZE = 2048


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(7)
        
        self.server = "192.168.1.25"
        self.port = 5555
        self.addr = (self.server, self.port)
    
    def connect(self):
        try:
            self.client.connect(self.addr)
            return_message = self.client.recv(PACKAGE_SIZE)
            if(return_message):
                return pickle.loads(return_message)
            else:
                return None
        except Exception:
            pass
        
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL))
            return_message = self.client.recv(PACKAGE_SIZE)
            if(return_message):
                return pickle.loads(return_message)
            else:
                return None
        except socket.error as e:
            print(str(e))

         
def main():
    pass


if __name__ == "__main__":
    main()
