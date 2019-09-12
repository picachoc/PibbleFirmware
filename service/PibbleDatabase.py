import MySQLdb

from functools import partial


print = partial(print, flush=True)


class PibbleDatabase:
    def __init__(self, brain, paramMysql=None):
        self.brain = brain
        self.inited = False

        
        if paramMysql:
            self.params = paramMysql
        else:
            self.params = {
                'db_host' : 'localhost',
                'db_user' : 'root',
                'db_password' : 'test',
                'db_name' : 'pibble_catalog',
                'db_max_items_retrieved' : 500
            }

        self.conn = None
        self.cursor = None


    def init(self):
        if not self.brain.inited:
            self.inited = False
            return False
        else:   
            try:
                self.conn = MySQLdb.connect(host=self.params["db_host"], user=self.params["db_user"], passwd=self.params["db_password"], db=self.params["db_name"])
                self.cursor = self.conn.cursor()
                self.inited = True
                return True
            except(Exception) as err:
                print(err)
                self.inited = False
                return {"error" : str(err)}
                

    def getTypes(self):
        if self.inited:
            try:
                self.cursor.execute("SELECT DISTINCT type FROM objects")
                types = self.cursor.fetchall()
                return types
            except(Exception) as err:
                print(err)
                return {"error" : str(err)}
        else:
            return {"inited" : False}
        
    def getConstellations(self, table):
        if self.inited:
            try:
                self.cursor.execute("SELECT DISTINCT constellation FROM {}".format(table))
                constellations = self.cursor.fetchall()
                return constellations
            except(Exception) as err:
                print(err)
                return {"error" : str(err)}
        else:
            return {"inited" : False}

    def getAllFromTable(self, table=None, args=None):
        if self.inited:
            try:
                visibility = args.pop("visible")
                liste = []
                
                ##self.cursor.execute("SELECT * FROM {}".format(table))
                sql_request = "SELECT * FROM {}".format(table)
                first = True
                for key in args:
                    if not (args[key] == None or args[key] == ""):
                            if first == False:
                                sql_request += " AND "
                            else:
                                sql_request += " WHERE "

                            if not args[key].isdigit():
                                if key == "name" and args[key] == "NOT NULL":               ## a
                                    sql_request +=  "{} IS {}".format(key, args[key])       ## enlever
                                elif key == "name":
                                    sql_request +=  "{} LIKE '{}%'".format(key, args[key])
                                else:
                                    sql_request +=  "{} = '{}'".format(key, args[key])
                            elif key == "magnitude":
                                sql_request +=  "{} < {}".format(key, args[key])
                            else:
                                sql_request +=  "{} = {}".format(key, args[key])
                                
                            first = False
                sql_request += " LIMIT {}".format(self.params["db_max_items_retrieved"])
                print("SQL request : " + sql_request)

                self.cursor.execute(sql_request)
                        
                row = self.cursor.fetchall()
                colNames = self.getAllcolumns(table)
                index = 0
                for obj in row:
                    liste.append({})
                    for x in range(0,len(colNames)):
                        liste[index].update({colNames[x] : obj[x]})
                    index += 1

                if visibility == "true":
                    liste = self.brain.getVisibles(liste)
                return liste
            except(Exception) as err:
                print(err)
                return {"error" : str(err)}
        else:
            return {"inited" : False}

    def getAllcolumns(self, table):
        if self.inited:
            try:
                colNames = []
                self.cursor.execute("SHOW COLUMNS FROM {}".format(table))
                col = self.cursor.fetchall()
                for column in col:
                    colNames.append(column[0].lower())
                return colNames
            except(Exception) as err:
                print(err)
                return {"error" : str(err)}
        else:
            return {"inited" : False}

    def getObjectByName(self, table=None, name=None):
        if self.inited:
            try:
                objs_dict = {}
                self.cursor.execute("SELECT * FROM objects WHERE NAME = '{}'".format(name))
                row = self.cursor.fetchall()
                colNames = self.getAllcolumns(table)
                for obj in row:
                    for x in range(0,len(colNames)):
                        objs_dict.update({colNames[x] : obj[x]})
                return objs_dict
            except(Exception) as err:
                print(err)
                return {"error" : str(err)}
        else:
            return {"inited" : False}


    def getAlignInit(self):
        if self.inited:
            try:
                objs_dict = self.getAllFromTable("stars", {"visible" : True, "name" : "NOT NULL"})
                return objs_dict
            except(Exception) as err:
                print(err)
                return {"error" : str(err)}
        else:
            return {"inited" : False}

    def addUserObject(self, args):
        if self.inited:
            try:
                sql_request = "INSERT INTO user_objects "
                column_str = "("
                values_str = "("
                first = True

                id_request = "SELECT count(id) FROM user_objects"
                id = int(self.cursor.execute(id_request)) + 1
                column_str += "id, "
                values_str += str(id) + ", "
                
                for key in args:
                    if first == False:
                        column_str += ", "
                        values_str += ", "
                    

                    column_str += str(key)
                    if str(args[key]).isdigit():
                        values_str += str(args[key])
                    else:
                        values_str += "'" + str(args[key]) + "'"
                
                column_str += ")"
                values_str += ")"

                first = False

                sql_request += column_str + " VALUES " + values_str
                print(sql_request)

                self.cursor.execute(sql_request)
                return {"success" : True}
            except(Exception) as err:
                print(err)
                return {"error" : str(err)}
        else:
            return {"inited" : False}
