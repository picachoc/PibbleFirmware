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
                'db'     : 'test'
            }

        try:
            self.conn = MySQLdb.connect(**self.params)
            self.cursor = self.conn.cursor()
        except(Exception) as err:
            print(err)

    def getNames(self):
        self.cursor.execute("SELECT * FROM objects")
        names = self.cursor.fetchall()
        return names

    def getAllCollumns(self, table):
        collNames = []
        self.cursor.execute("SHOW COLUMNS FROM {}".format(table))
        coll = self.cursor.fetchall()
        for collumn in coll:
            collNames.append(collumn[0])
        return collNames

    def getObjectByName(self, table, name):
        objs_dict = {}
        self.cursor.execute("SELECT * FROM objects WHERE NAME = '{}'".format(name))
        row = self.cursor.fetchall()
        collNames = self.getAllCollumns(table)
        for obj in row:
            for x in range(0,len(collNames)):
                objs_dict.update({collNames[x] : obj[x]})
        return objs_dict

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
