class User:
    def __init__(self, controller, userID, name, surname, email, phoneNumber, address, login, password, userType):
        self.dbController = controller
        self.userType = userType
        self.id = userID
        self.name = name
        self.surname = surname
        self.email = email
        self.phoneNumber = phoneNumber
        self.address = address
        self.login = login
        self.password = password

    def getController(self):
        return self.dbController

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
    def __init__(self, clientController, userID, name, surname, email, phoneNumber, address, login, password):
        super().__init__(clientController, userID, name, surname, email, phoneNumber, address, login, password, "klient")


class Employee(User):
    def __init__(self, employeeController, userID, name, surname, email, phoneNumber, address, login, password):
        super().__init__(employeeController, userID, name, surname, email, phoneNumber, address, login, password, "pracownik")
