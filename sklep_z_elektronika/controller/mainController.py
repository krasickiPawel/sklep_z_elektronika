from sklep_z_elektronika.model.database import Database
from sklep_z_elektronika.model.user import Client, Employee
from sklep_z_elektronika.model.loggedUsers import LoggedUsers
from sklep_z_elektronika.controller.userController import ClientController, EmployeeController, UserController
from sklep_z_elektronika.model.order import Order, HistOrder
from sklep_z_elektronika.model.product import Product
from threading import Timer
import time


class MainController:
    def __init__(self):
        self.db = Database('localhost', 'root', 'mysql123', 'test_elektronika')
        self.loggedUsers = LoggedUsers()

    def clientLogin(self, email, password):     # TODO jeśli coś jest w basket to rzucić jakąś przypominajkę z alertu
        cc = ClientController(self.db)
        cc.connect()

        success, _id = cc.login(email, password)

        if success == 1:
            name, surname, email, phoneNumber, address = cc.getClientData(_id)
            client = Client(_id, name, surname, email, phoneNumber, address, password)
            basketOrders = cc.showBasketOrders(_id)
            for basketOrder in basketOrders:
                orderID, clientID, productID, date, status = basketOrder
                order = Order(orderID, clientID, productID, date, status)
                client.addOrderBasket(order)
            shopHistOrders = cc.showShopHist(_id)
            for shopHistOrder in shopHistOrders:
                orderID, productName, productCategory, productPrice, date, status = shopHistOrder
                histOrder = HistOrder(orderID, productName, productCategory, productPrice, date, status)
                client.addOrderShopHist(histOrder)
            self.loggedUsers.addLoggedClient(_id, client)
            cc.disconnect()
            return _id      # TODO w www wyswietlic pozniej produkty
        else:
            cc.disconnect()
            return None
            # TODO w www jeśli _id != None to dodać do ciasteczek czy tam gdzieś i później używać do getLoggedUser

    def employeeLogin(self, username, password):
        ec = EmployeeController(self.db)
        ec.connect()

        success, _id = ec.login(username, password)

        if success == 1:
            name, surname, email, phoneNumber, address, position, salary = ec.getEmployeeData(_id)
            employee = Employee(_id, name, surname, email, phoneNumber, address, password, position, salary)
            self.loggedUsers.addLoggedEmployee(_id, employee)
            ec.disconnect()
            return _id

        else:
            ec.disconnect()
            return None
            # TODO w www jeśli _id != None to dodać do ciasteczek czy tam gdzieś i później używać do getLoggedUser

    def clientRegister(self, name, surname, email, phoneNumber, address, password):
        cc = ClientController(self.db)
        cc.connect()

        success = cc.register(name, surname, email, phoneNumber, address, password)

        cc.disconnect()

        return True if success == 1 else False  # TODO sprawdzic w www czy udalo sie zalogowac

    def getLoggedClient(self, _id):
        return self.loggedUsers.getLoggedClient(_id)

    def getLoggedEmployee(self, _id):
        return self.loggedUsers.getLoggedEmployee(_id)

    def getAllProductsFromDB(self):
        productList = []
        uc = UserController(self.db)
        uc.connect()
        productListFromDB = uc.showProducts()
        uc.disconnect()
        for productFromDB in productListFromDB:
            productID, name, price, category, amount = productFromDB
            product = Product(productID, name, price, category, amount)
            productList.append(product)

        return productList

    def prepareProductsToShow(self, _id, userType, productList):
        if userType == "client":
            client = self.getLoggedClient(_id)
            client.setCurrentlyViewedProducts(productList)
        elif userType == "employee":
            employee = self.getLoggedEmployee(_id)
            employee.setCurrentlyViewedProducts(productList)

    def showProducts(self, _id, userType):
        if userType == "client":
            client = self.getLoggedClient(_id)
            return client.getCurrentlyViewedProducts()
        elif userType == "employee":
            employee = self.getLoggedEmployee(_id)
            return employee.getCurrentlyViewedProducts()

    def clientShowBasketOrders(self, _id):
        client = self.loggedUsers.getLoggedClient(_id)
        basket = client.getBasket()
        return basket   # TODO sprawdzic czy nie jest pusty, jeśli jest to wypisać "twój koszyk jest pusty", pamiętać że po każdym dodaniu i usunięciu z koszyka należy wyświetlić (przeładować) koszyk

    def clientShowFormattedBasket(self, _id):
        cc = ClientController(self.db)
        cc.connect()
        basketFromDB = cc.showFormattedBasket(_id)
        totalPrice = cc.getBasketTotalPrice(_id)
        cc.disconnect()

        return [basketFromDB, totalPrice]

    def clientAddToBasket(self, _id, productID):    # dodanie do koszyka nie rezerwuje produktu (nie zmniejsza jego ilosci w bazie) - dopiero "zamów" to robi
        cc = ClientController(self.db)
        cc.connect()
        cc.addToBasket(_id, productID)

        clientBasket = self.clientShowBasketOrders(_id)
        basketSet = set()
        for clientBasketOrder in clientBasket:
            basketSet.add(clientBasketOrder.getOrderID())

        newOrder = None
        basketList = cc.showBasketOrders(_id)
        cc.disconnect()

        for basketOrder in basketList:
            if basketOrder[0] not in basketSet:
                newOrder = basketOrder

        if newOrder is not None:
            orderID, clientID, productID, date, status = newOrder
            orderToAddToClientBasket = Order(orderID, clientID, productID, date, status)
            client = self.loggedUsers.getLoggedClient(_id)
            client.addOrderBasket(orderToAddToClientBasket)
            return self.searchProductUsingID(productID).getName()
        else:
            return None

    def clientRemoveFromBasket(self, _id, orderID):
        cc = ClientController(self.db)
        cc.connect()
        cc.removeFromBasket(orderID)

        client = self.getLoggedClient(_id)
        clientBasket = self.clientShowBasketOrders(_id)
        orderToBeRemoved = None
        for order in clientBasket:
            if int(order.getOrderID()) == int(orderID):
                orderToBeRemoved = order
        client.removeOrderBasket(orderToBeRemoved)

        databaseCheck = False
        applicationCheck = False
        checkIDSetDatabase = set()
        checkIDSetApplication = set()

        checkOrderList = cc.showBasketOrders(_id)
        cc.disconnect()
        checkBasket = client.getBasket()

        for order in checkOrderList:
            checkIDSetDatabase.add(order[0])
        if orderID not in checkIDSetDatabase:
            databaseCheck = True
        for order in checkBasket:
            checkIDSetApplication.add(order.getOrderID())
        if orderID not in checkIDSetApplication:
            applicationCheck = True

        if applicationCheck and databaseCheck:
            return True
        else:
            return False

    def clientBuyProductsInBasket(self, _id):   # zamów (bez płacenia)  #TODO produkt - main będzie miał listę //lub nie
        """

        cc = ClientController(self.db)
        cc.connect()
        cc.addToBasket(_id, productID)

        clientBasket = self.clientShowBasketOrders(_id)
        basketSet = set()
        for clientBasketOrder in clientBasket:
            basketSet.add(clientBasketOrder.getOrderID())

        newOrder = None
        basketList = cc.showBasketOrders(_id)
        cc.disconnect()

        for basketOrder in basketList:
            if basketOrder[0] not in basketSet:
                newOrder = basketOrder

        if newOrder is not None:
            orderID, clientID, productID, date, status = newOrder
            orderToAddToClientBasket = Order(orderID, clientID, productID, date, status)
            client = self.loggedUsers.getLoggedClient(_id)
            client.addOrderBasket(orderToAddToClientBasket)
            return True
        else:
            return False

        :param _id:
        :return:
        """

        successfullyBoughtProducts = []
        client = self.getLoggedClient(_id)
        basketRAM = client.getBasket()

        cc = ClientController(self.db)
        cc.connect()

        basket = cc.showFormattedBasket(_id)
        basketLen = len(basket)

        ordersToRemoveFromRAM = []
        for order in basket:
            productID, productName, productCategory, productPrice, orderID, clientID, date, status = order
            oRD = Order(orderID, clientID, productID, date, status)
            histOrder = HistOrder(orderID, productName, productCategory, productPrice, date, status)
            success = cc.buyProduct(oRD)
            time.sleep(0.05)
            print(success, oRD.getOrderID())
            if success:
                successfullyBoughtProducts.append(oRD)
                client.addOrderShopHist(oRD)
                ordersToRemoveFromRAM.append(oRD)
                client.addOrderShopHist(histOrder)
                # client.removeOrderBasket(oRD)

        cc.disconnect()
        juzNieMamSil = []
        for oRD in ordersToRemoveFromRAM:
            for i in range(len(basketRAM)):
                if oRD.getOrderID() == basketRAM[i].getOrderID():
                    juzNieMamSil.append(basketRAM[i])

        for officialOrder in juzNieMamSil:
            client.removeOrderBasket(officialOrder)

        if len(successfullyBoughtProducts) == basketLen:
            return True
        else:
            return False                # coś się nie powiodło

    def clientShowShopHist(self, _id):
        client = self.loggedUsers.getLoggedClient(_id)
        shopHist = client.getShopHist()
        return shopHist

    def searchProductUsingName(self, productName):
        uc = UserController(self.db)
        uc.connect()
        productListFromDatabase = uc.searchProductUsingName(productName)
        uc.disconnect()

        productList = []
        for productFromDatabase in productListFromDatabase:
            productID, name, price, category, amount = productFromDatabase
            product = Product(productID, name, price, category, amount)
            productList.append(product)

        if len(productList) > 0:
            return productList
        else:
            return None

    def clientLogout(self, _id):
        self.loggedUsers.removeLoggedClient(_id)

    def employeeLogout(self, _id):
        self.loggedUsers.removeLoggedEmployee(_id)  # TODO w www wypisac "zostales wylogowany"

    def searchProductUsingID(self, productID):
        uc = UserController(self.db)
        uc.connect()
        productInfo = uc.searchProductUsingID(productID)[0]
        uc.disconnect()
        productID, name, price, category, amount = productInfo
        product = Product(productID, name, price, category, amount)
        return product

    def clientCheckIfLogged(self, _id):
        return self.loggedUsers.checkIfLogged(_id)

    def cleanMemory(self, _id, time, userType):
        if userType == "client":
            t = Timer(time, self.loggedUsers.removeLoggedClient, args=[_id])
            client = self.getLoggedClient(_id)
            client.setTimer(t)
            client.startTimer()
        elif userType == "employee":
            t = Timer(time, self.loggedUsers.removeLoggedEmployee, args=[_id])
            employee = self.getLoggedEmployee(_id)
            employee.setTimer(t)
            employee.startTimer()
