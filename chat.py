from IPy import IP
import socket
import os
import threading
from Tkinter import *

connections_list = []
nick_name = ""
log = ""

def main():
    os.system('cls')
    init_save_name()


def init_save_name():
    global nick_name
    
    def save_name(event):
        global nick_name
        if (nick.get() != ""):
            nick_name = nick.get()
            name_input.destroy()
            init_gui()
            
    name_input = Tk()
    nick = Entry(name_input)
    nick.pack(side='top', fill='x', expand='true')
    ok_button = Button(name_input, text="OK", command=lambda: save_name(""))
    ok_button.pack(fill=BOTH, expand=1)
    nick.bind('<Return>',save_name)      
    name_input.mainloop()
    
def search():
    global nick_name
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
    tk=Tk()
    log = Text(tk)
    text=StringVar()
    text.set('')    
    tk.title('HummerHeadIEagleIntercepterChat')
    tk.geometry('400x300')
    nick = Label(tk, text=nick_name)
    nick.pack(side='bottom', fill='x', expand='true')
    
    msg = Entry(tk, textvariable=text)
    msg.pack(side='bottom', fill='x', expand='true')
    log.pack(side='top', fill='both',expand='true')

    def sendproc(event):
        log.insert(END,nick_name +': ' + text.get()+'\n')
        
        for i in connections_list:
                i.send((nick_name + ": " + text.get()).encode("UTF8"))
        text.set('')
    def handler(): 
        for i in connections_list:
            i.send((nick_name + ": left the chat.").encode("UTF8"))
        tk.destroy()
        
    tk.protocol("WM_DELETE_WINDOW", handler)
    msg.bind('<Return>',sendproc)
    tk.bind('<Escape>', lambda: tk.destroy())
    search()
    tk.mainloop()

def try_connect(ip):
    try:
        sock_connect = socket.socket()
        sock_connect.settimeout(0.01)
        sock_connect.connect((ip, 6666))
        sock_connect.settimeout(None)
        sock_connect.send((nick_name + " entered chat.").encode("UTF8"))
        data = sock_connect.recv(1024).decode()
        return sock_connect
    except BaseException:
        return None

def get_local_address():
    return socket.gethostbyname_ex(socket.gethostname())[2][0]

class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.nick_name = nick_name
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
