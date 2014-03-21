import socket
import os
import threading

connections_list = []
nick_name = ""

def main():
	os.system('cls')

	nick_name = raw_input("Nickname: ")
	
	sock_server = Server()
	sock_server.start()

	print("My ip: " + get_local_address() + "\n")
	print("Online list: ")
	
	for i in IP('10.77.70.0/24'):
                if str(i) != str(get_local_address()):
                        result = try_connect(str(i))
                        if (result != None):
                                connections_list.append(result)
                                Listner_o = Listner(result)
                                Listner_o.start()
                                print(i)

	while True:
                message = raw_input()
                if message == "getlist":
                        print(str(connections_list) + " " + str(len(connections_list)))

                for i in connections_list:
                        i.send((nick_name + ": " + message).encode())
                        


def try_connect(ip):
    try:
        sock_connect = socket.socket()
        sock_connect.settimeout(0.01)
        sock_connect.connect((ip, 6666))
        sock_connect.settimeout(None)
        data = sock_connect.recv(1024).decode()
    	return sock_connect
    except BaseException:
        return None

def get_local_address():
    return socket.gethostbyname_ex(socket.gethostname())[2][0]

class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket()
        self.sock.bind(('', 6666))
        self.sock.listen(1)

    def run(self):
    	while True:
            self.conn, self.addr = self.sock.accept()
            self.conn.send("1".encode())
            Listner_o = Listner(self.conn)
            Listner_o.start()
            connections_list.append(self.conn)

class Listner (threading.Thread):
    def __init__(self, connect):
            threading.Thread.__init__(self)
            self.connect = connect
            self.nick_name = nick_name

    def run(self):
            while True:
                try:
                    data = self.connect.recv(1024).decode()
                    if data != "":
                            print(data)
                except BaseException:
                    connections_list.remove(self.connect)
                    break

if __name__ == "__main__":
	main()
