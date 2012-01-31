import sqlite3
import sys


class db():
    """db"""
    def __init__(self, argv):
        if len(argv) < 2:
            print 'No action specified.'
            sys.exit()

        print argv[1]
        action = argv[1]
        con = sqlite3.connect("./test.db")
        con.isolation_level = None  # for autocommit mode
        self.cur = con.cursor()
        getattr(self, action)()

    def insert(self):
        self.cur.execute("insert into test(i) values (1)")
        self.cur.execute("select * from test")
        print self.cur.fetchall()

    def select(self):
        try:
            self.cur.execute("select * from test")
            print self.cur.fetchall()
        except sqlite3.OperationalError, e:
            print "E:" + str(e)
            self.create()
            self.select()

    def create(self):
        self.cur.execute("create table test(i)")

if __name__ == '__main__':
    init = db(sys.argv)
