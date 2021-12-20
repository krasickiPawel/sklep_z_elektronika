class User:
    def __init__(self, userType, userID, name, surname, email, phoneNumber, address, login, password):
        self.userType = userType
        self.id = userID
        self.name = name
        self.surname = surname
        self.email = email
        self.phoneNumber = phoneNumber
        self.address = address
        self.login = login
        self.password = password

    def getID(self):
        return self.id

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
    def __init__(self, clientCommunicationWithDatabase, userID, name, surname, email, phoneNumber, address, login, password):
        super().__init__("client", userID, name, surname, email, phoneNumber, address, login, password)
        self.clientCommunicationWithDatabase = clientCommunicationWithDatabase


class Employee(User):
    def __init__(self, employeeCommunicationWithDatabase, userID, name, surname, email, phoneNumber, address, login, password):
        super().__init__("employee", userID, name, surname, email, phoneNumber, address, login, password)
        self.employeeCommunicationWithDatabase = employeeCommunicationWithDatabase
