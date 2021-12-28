from sklep_z_elektronika.model.database import Database
from sklep_z_elektronika.model.user import Client, Employee
from sklep_z_elektronika.model.loggedUsers import LoggedUsers
from sklep_z_elektronika.controller.userController import ClientController, EmployeeController


class MainController:
    def __init__(self):
        self.db = Database('localhost', 'root', 'mysql123', 'test_elektronika')
        self.loggedUsers = LoggedUsers()

    def loginClient(self, request):
        username = 0
        password = 0

        cc = ClientController(self.db)
        cc.connect()

        success, _id = cc.login(username, password)

        print(success, _id, cc.getUserData(_id)[0])
        if success == 1:
            name, surname, email, phoneNumber, address, username, password, userType = cc.getUserData(_id)[0]
            user = Client(cc, _id, name, surname, email, phoneNumber, address, username, password)
            self.loggedUsers.addLoggedUser(_id, user)

        cc.disconnect()
        return _id  # w www jeśli _id != 0 to dodać do ciasteczek czy tam gdzieś i później używać do getLoggedUser

    def loginEmployee(self, request):
        username = 0
        password = 0

        ec = EmployeeController(self.db)
        ec.connect()

        success, _id = ec.login(username, password)

        print(success, _id, ec.getUserData(_id)[0])
        if success == 1:
            name, surname, email, phoneNumber, address, username, password, userType = ec.getUserData(_id)[0]
            user = Employee(ec, _id, name, surname, email, phoneNumber, address, username, password)
            self.loggedUsers.addLoggedUser(_id, user)

        ec.disconnect()
        return _id  # w www jeśli _id != 0 to dodać do ciasteczek czy tam gdzieś i później używać do getLoggedUser

    def registerClient(self, request):
        username = "login1"
        password = "123"
        name = "test rejestracji1"
        surname = "xd1"
        email = "test1@email.test"
        phoneNumber = "545 324 212"
        address = "add"

        cc = ClientController(self.db)
        cc.connect()

        success = cc.register(username, password, name, surname, email, phoneNumber, address)
        print(success)

        cc.disconnect()

        return True if success == 1 else False

    def getLoggedUser(self, _id):
        return self.loggedUsers.getLoggedUser(_id)

    def showProducts(self, _id):
        user = self.getLoggedUser(_id)
        userController = user.getController()
        productList = userController.showProducts()
        return productList

if __name__ == '__main__':
    pass
    # print(cc.searchProductUsingName('i'))
    # success, _id = cc.login("pawcio", "123")
    # print(success, _id)
    # db.connect()
    # db.login('papaj', 'dupa')
    # db.addToBasket(6, 33)
    # db.addNewProduct("xiaomi mi 11", 150.5, 'tel', 14)
    # db.disconnect()
