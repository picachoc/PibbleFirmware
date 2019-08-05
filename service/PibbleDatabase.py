import MySQLdb

class PibbleDatabase:
    def __init__(self, paramMysql=None):
        if not paramMysql == None:
            self.params = paramMysql
        else:
            self.params = {
                'db_host'   : 'localhost',
                'db_user'   : 'root',
                'db_password' : 'test',
                'db_name'     : 'pibble_catalog'
            }

        try:
            self.conn = MySQLdb.connect(host=self.params["db_host"], user=self.params["db_user"], passwd=self.params["db_password"], db=self.params["db_name"])
            self.cursor = self.conn.cursor()
        except(Exception) as err:
            print(err)

    def getNames(self):
        self.cursor.execute("SELECT * FROM objects")
        names = self.cursor.fetchall()
        return names

    def getTypes(self):
        self.cursor.execute("SELECT DISTINCT type FROM objects")
        types = self.cursor.fetchall()
        return types
        
    def getConstellations(self, table):
        self.cursor.execute("SELECT DISTINCT constellation FROM {}".format(table))
        constellations = self.cursor.fetchall()
        return constellations

    def getAllFromTable(self, table=None):
        liste = []
        self.cursor.execute("SELECT * FROM {}".format(table))
        row = self.cursor.fetchall()
        collNames = self.getAllCollumns(table)
        index = 0
        for obj in row:
            liste.append({})
            for x in range(0,len(collNames)):
                liste[index].update({collNames[x] : obj[x]})
            index += 1
        return liste

    def getAllCollumns(self, table):
        collNames = []
        self.cursor.execute("SHOW COLUMNS FROM {}".format(table))
        coll = self.cursor.fetchall()
        for collumn in coll:
            collNames.append(collumn[0])
        return collNames

    def getObjectByName(self, table=None, name=None):
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
