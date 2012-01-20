import sqlite3
import sys

class db():
    """db"""
    def __init__(self, argv):
        if len(argv) < 2:
            print 'No action specified.'
            sys.exit()

        print argv[1]
        con = sqlite3.connect("./test.db")
        self.cur = con.cursor()

    def create(self):
        self.cur.execute("create table test(i)")

if __name__ == '__main__':
    init = db(sys.argv)
