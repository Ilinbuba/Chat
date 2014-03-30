from IPy import IP
import socket
import os
import threading
from Tkinter import *

connections_list = []
nick_name = ""
tk=Tk()
log = Text(tk)
nick_name = ""

def main():
    os.system('cls')
    init_gui() 

def search():
    sock_server = Server()
    sock_server.start()
    
    log.insert(END, "My ip: " + get_local_address() + "\n")
    log.insert(END, "Online list: \n")

    for i in IP('10.77.70.0/24'):
                if str(i) != str(get_local_address()):
                        result = try_connect(str(i))
                        if (result != None):
                                connections_list.append(result)
                                Listner_o = Listner(result)
                                Listner_o.start()
                                log.insert(END, str(i) + "\n")
                        

def init_gui():
    global log
    global nick_name
    text=StringVar()
    name=StringVar()
    name.set('UserName')
    text.set('')
    tk.title('HummerHeadIEagleIntercepterChat')
    tk.geometry('400x300')
    
    log = Text(tk)
    nick = Entry(tk, textvariable=name)
    msg = Entry(tk, textvariable=text)
    msg.pack(side='bottom', fill='x', expand='true')
    nick.pack(side='bottom', fill='x', expand='true')
    log.pack(side='top', fill='both',expand='true')
    nick_name = name.get()
    
    def sendproc(event):
        log.insert(END,name.get()+':'+text.get()+'\n')
        
        if text.get() == "getlist":
            log.insert(END, str(connections_list) + " " + str(len(connections_list))+"\n")
        for i in connections_list:
            i.send((nick_name + ": " + text.get()).encode('UTF8'))

        text.set('')
    
    msg.bind('<Return>',sendproc)
    search()
    tk.mainloop()

def try_connect(ip):
    try:
        sock_connect = socket.socket()
        sock_connect.settimeout(0.01)
        sock_connect.connect((ip, 6666))
        sock_connect.settimeout(None)
        sock_connect.send(nick_name.encode("UTF8"))
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
            self.conn.send("1".encode("UTF8"))
            log.insert(END, self.conn.recv(1024).decode("UTF8") + "\n")
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
                    data = self.connect.recv(1024).decode('UTF8')
                    if data != "":
                            log.insert(END, data + "\n")
                except BaseException:
                    connections_list.remove(self.connect)
                    break

if __name__ == "__main__":
main()
