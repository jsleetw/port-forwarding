import socket
import sys
import thread


class port_forwarding:
    """a class using in port_forwarding"""
    def __init__(self, setup, error):
        #sys.stderr = file(error, 'a')
        for settings in self.parse(setup):
            thread.start_new_thread(self.server, settings)
        lock = thread.allocate_lock()
        lock.acquire()
        lock.acquire()

    def parse(self, setup):
        settings = list()
        for line in file(setup):
            parts = line.split()
            settings.append((parts[0], int(parts[1]), int(parts[2])))
        return settings

    def server(self, *settings):
        try:
            dock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dock_socket.bind(('', settings[2]))
            dock_socket.listen(5)
            while True:
                client_socket, address = dock_socket.accept()
                print "clinet %s -> from port:%s -> to:%s:%s" % (str(address).strip(), settings[2], settings[0], settings[1])
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.connect((settings[0], settings[1]))
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
                source.shutdown(socket.SHUT_RDWR)
                destination.shutdown(socket.SHUT_RDWR)

if __name__ == '__main__':
    demon = port_forwarding('proxy.ini', 'error.log')
