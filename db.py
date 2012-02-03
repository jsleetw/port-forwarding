import sqlite3
import sys


class db():
    """db"""
    def __init__(self, argv):
        if len(argv) < 2:
            print 'No action specified.'
            sys.exit()

        action = argv[1]
        con = sqlite3.connect("./test.db")
        con.isolation_level = None  # for autocommit mode
        self.cur = con.cursor()
        try:
            getattr(self, action)()
        except sqlite3.OperationalError, e:
            print "E:" + str(e)
            self.create()
            getattr(self, action)()

    def drop(self):
        self.cur.execute("drop table test")

    def insert(self):
        #insert ip port listen-port
        if len(sys.argv) < 5:
            print 'Not enough argument.'
            sys.exit()

        ip = sys.argv[2]
        port = sys.argv[3]
        listen_port = sys.argv[4]
        self.cur.execute("insert into test(ip, port, listen_port) values (:ip,\
                          :port, :listen_port)",
                          {"ip": ip, "port": port, "listen_port": listen_port})
        self.select()

    def select(self):
        self.cur.execute("select ip, port, listen_port from test")
        data = self.cur.fetchall()
        print len(data)
        for i in data:
            print i[0]

    def create(self):
        self.cur.execute("create table test(ip, port, listen_port)")

if __name__ == '__main__':
    init = db(sys.argv)
