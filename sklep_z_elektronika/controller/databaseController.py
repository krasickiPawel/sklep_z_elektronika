import mysql.connector


class DatabaseController:
    def __init__(self, dataBase):
        self.dataBase = dataBase
        self.cursor = None

    def connect(self):
        self.dataBase.db = mysql.connector.connect(host=self.dataBase.host, user=self.dataBase.user, password=self.dataBase.password, database=self.dataBase.database)
        self.cursor = self.dataBase.db.cursor()

    def disconnect(self):
        self.cursor.close()
        self.dataBase.db.close()

    def showView(self, view):
        try:
            self.cursor.execute(f'SELECT * FROM {view}')
            resultList = self.cursor.fetchall()
            returnList = []
            for result in resultList:
                returnList.append(result)
            return returnList                           # lista krotek
        except Exception as e:
            print(e)

    def callStoredProcedureWithoutReturn(self, name, args):
        try:
            self.cursor.callproc(f'{name}', args)
            self.dataBase.db.commit()                   # zatwierdzenie zmian
        except mysql.connector.Error as e:
            print(e)

    def callStoredProcedureWithReturn(self, name, args):
        try:
            self.cursor.callproc(name, args)
            resultList = None
            for result in self.cursor.stored_results():
                resultList = result.fetchall()
            return resultList                           # lista krotek
        except mysql.connector.Error as e:
            print(e)

    def callLoginProcedure(self, name, args):
        try:
            resultArgs = self.cursor.callproc(name, args)
            return resultArgs[0], resultArgs[1]         # success, userID
        except mysql.connector.Error as e:
            print(e)

    def callRegisterProcedure(self, name, args):
        try:
            resultArgs = self.cursor.callproc(name, args)
            self.dataBase.db.commit()
            return resultArgs[0]                        # success
        except mysql.connector.Error as e:
            print(e)
