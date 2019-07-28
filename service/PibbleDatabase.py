import MySQLdb

class PibbleDatabase:
    def __init__(self, paramMysql=None):
        if not paramMysql == None:
            self.params = paramMysql
        else:
            self.params = {
                'host'   : 'localhost',
                'user'   : 'root',
                'passwd' : 'test',
                'db'     : 'pibble_catalog'
            }

        try:
            self.conn = MySQLdb.connect(**self.params)
            self.cursor = conn.cursor()
        except(Exception):
            print("An error occured during connection to DB.")
    
    def getNames(self):
        self.cursor.execute("SELECT * FROM objects")
        names = self.cursor.fetchall()
        return names

    def getAllCollumns(self):
        collNames = []
        self.cursor.execute("SHOW COLUMNS FROM objects")
        coll = self.cursor.fetchall()
        for collumn in coll:
            collNames.append(collumn[0])
        return collNames

    def getObjectByName(self, name):
        self.cursor.execute("SELECT * FROM objects WHERE NAME = {}".format(name))
        row = self.cursor.fetchall()
        return row

"""paramMysql = {
    'host'   : 'localhost',
    'user'   : 'root',
    'passwd' : 'test',
    'db'     : 'pibble_catalog'
}

sql = "SELECT * FROM objects"
sql2 = "SHOW TABLES"
sql3 = "SHOW COLUMNS FROM objects"

conn = MySQLdb.connect(**paramMysql)

cur = conn.cursor()
cur.execute(sql3)

rows = cur.fetchall()
print(rows)

conn.close()
"""
