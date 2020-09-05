import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(10)
        
        self.server = "192.168.1.25"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.object = self.connect()
        
    def get_object(self):
        return self.object
    
    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except Exception:
            pass
        
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(str(e))

         
def main():
    pass


if __name__ == "__main__":
    main()
