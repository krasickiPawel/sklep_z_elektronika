class User:
    def __init__(self, userType, name, surname, email, phoneNumber, address, login, password):
        self.dbConnector = None
        self.userType = userType
        self.id = None
        self.name = name
        self.surname = surname
        self.email = email
        self.phoneNumber = phoneNumber
        self.address = address
        self.login = login
        self.password = password

    def setID(self, _id):
        self.id = _id

    def getID(self):
        return self.id

    def setDbConnector(self, dbConnector):
        self.dbConnector = dbConnector

    def getDBConnector(self):
        return self.dbConnector

    def getName(self):
        return self.name

    def getSurname(self):
        return self.surname

    def getEmail(self):
        return self.email

    def getPhoneNumber(self):
        return self.phoneNumber

    def getAddress(self):
        return self.address


class Client(User):
    def __init__(self, clientCommunicationWithDatabase, name, surname, email, phoneNumber, address, login, password):
        super().__init__("klient", name, surname, email, phoneNumber, address, login, password)
        self.clientCommunicationWithDatabase = clientCommunicationWithDatabase


class Employee(User):
    def __init__(self, employeeCommunicationWithDatabase, name, surname, email, phoneNumber, address, login, password):
        super().__init__("pracownik", name, surname, email, phoneNumber, address, login, password)
        self.employeeCommunicationWithDatabase = employeeCommunicationWithDatabase
