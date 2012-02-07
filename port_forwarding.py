import socket
import sqlite3
import thread


class port_forwarding:
    """using in port_forwarding"""
    def __init__(self, setup, error):
        for settings in self.fetch_db():
            thread.start_new_thread(self.server, settings)
        lock = thread.allocate_lock()
        lock.acquire()
        lock.acquire()

    def fetch_db(self):
        con = sqlite3.connect("./test.db")
        cur = con.cursor()
        cur.execute("select ip, port, listen_port from test")
        data = cur.fetchall()
        return data

    def parse(self, setup):
        settings = list()
        for line in file(setup):
            parts = line.split()
            settings.append((parts[0], int(parts[1]), int(parts[2])))
        return settings

    def server(self, *settings):
        try:
            ip = str(settings[0])
            port = int(settings[1])
            listen_port = int(settings[2])
            dock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dock_socket.bind(('', listen_port))
            dock_socket.listen(5)
            while True:
                client_socket, address = dock_socket.accept()
                print "clinet %s -> from port:%s -> to:%s:%s" % \
                (str(address).strip(), listen_port, ip, port)
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.connect((ip, port))
                thread.start_new_thread(self.forward, (client_socket, server_socket))
                thread.start_new_thread(self.forward, (server_socket, client_socket))
        finally:
            thread.start_new_thread(self.server, settings)

    def forward(self, source, destination):
        string = ' '
        while string:
            string = source.recv(1024)
            if string:
                destination.sendall(string)
            else:
                try:
                    source.shutdown(socket.SHUT_RDWR)
                    destination.shutdown(socket.SHUT_RDWR)
                except socket.error, e:
                    print "E:" + str(e)


if __name__ == '__main__':
    demon = port_forwarding('proxy.ini', 'error.log')
