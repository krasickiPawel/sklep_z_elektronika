from src.model.database import Database
from src.model.user import Client, Employee
from src.model.loggedUsers import LoggedUsers
from src.controller.userController import ClientController, EmployeeController, UserController
from src.model.order import Order, HistOrder, EmployeeViewOrder
from src.model.product import Product
from threading import Timer
import time


class MainController:
    def __init__(self, host, user, password, database):
        self.db = Database(host, user, password, database)
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
            print("no jestem tu")
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

    def clientRegister(self, name, surname, email, phoneNumber, address, password):
        cc = ClientController(self.db)
        cc.connect()

        success = cc.register(name, surname, email, phoneNumber, address, password)

        cc.disconnect()

        return True if success == 1 else False

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
            return self.searchProductUsingID(productID)[0].getName()
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

    def clientBuyProductsInBasket(self, _id):   # zamów (bez płacenia)  #sory za ten syf xD
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

            success = cc.buyProduct(oRD)

            time.sleep(0.05)
            print(success, oRD.getOrderID())
            if success:
                successfullyBoughtProducts.append(oRD)
                ordersToRemoveFromRAM.append(oRD)
                # client.removeOrderBasket(oRD)

        # ratowanie shopHist w RAM, ale i tak sie z tego wycofalem i przeszedłem na pobieranie bezpośrednio z bazy
        basket = cc.showFormattedBasket(_id)
        for order in basket:
            productID, productName, productCategory, productPrice, orderID, clientID, date, status = order
            histOrder = HistOrder(orderID, productName, productCategory, productPrice, date, status)
            if status != "w koszyku":               # xD
                client.addOrderShopHist(histOrder)  # to nie ma prawa dzialac -> naprawione w clientShowShopHist(_id)
        # ########################################################

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
        cc = ClientController(self.db)
        cc.connect()

        shopHistTupleList = cc.showShopHist(_id)
        shopHist = []

        for shopHistOrder in shopHistTupleList:
            orderID, productName, productCategory, productPrice, date, status = shopHistOrder
            histOrder = HistOrder(orderID, productName, productCategory, productPrice, date, status)
            shopHist.append(histOrder)

        cc.disconnect()

        # client = self.loggedUsers.getLoggedClient(_id)
        # shopHist = client.getShopHist()
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
        client = self.getLoggedClient(_id)
        client.stopTimer()
        self.loggedUsers.removeLoggedClient(_id)

    def employeeLogout(self, _id):
        employee = self.getLoggedEmployee(_id)
        employee.stopTimer()
        self.loggedUsers.removeLoggedEmployee(_id)  # TODO w www wypisac "zostales wylogowany"

    def searchProductUsingID(self, productID):      # TODO wrzucać do view pracownika jak w searchByName
        uc = UserController(self.db)
        uc.connect()
        productInfo = uc.searchProductUsingID(productID)[0]
        uc.disconnect()
        productID, name, price, category, amount = productInfo
        product = Product(productID, name, price, category, amount)
        return [product]

    def clientCheckIfLogged(self, _id):
        return self.loggedUsers.checkIfLogged(_id)

    def employeeCheckIfLogged(self, _id):
        return self.loggedUsers.checkIfEmpLogged(_id)

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

    def employeeShowProductsUnavailable(self):
        productList = []
        ec = EmployeeController(self.db)
        ec.connect()                                                # dotąd powtarzalne

        productListFromDB = ec.showProductsUnavailable()

        ec.disconnect()                                             # odtąd powtarzalne
        for productFromDB in productListFromDB:
            productID, name, price, category, amount = productFromDB
            product = Product(productID, name, price, category, amount)
            productList.append(product)

        return productList                                          # trzeba skorzystac z prepareProductsToShow

    def employeeShowViewOrder(self, view):
        orderList = []
        ec = EmployeeController(self.db)
        ec.connect()                                                # dotąd powtarzalne

        orderListFromDB = []
        if view == "completed":
            orderListFromDB = ec.showOrdersCompleted()
        elif view == "canceled":
            orderListFromDB = ec.showOrdersCanceled()
        else:
            orderListFromDB = ec.showOrdersInRealization()

        ec.disconnect()                                             # odtąd powtarzalne

        for orderFromDB in orderListFromDB:
            orderID, clientID, productID, clientName, clientSurname, clientEmail, clientPhone, clientAddress, productName, productCategory, productPrice, orderDate, orderStatus = orderFromDB

            order = EmployeeViewOrder(orderID, clientID, productID, clientName, clientSurname, clientEmail, clientPhone, clientAddress, productName, productCategory, productPrice, orderDate, orderStatus)     # dla indywidualnego pracownika przypisac widok
            orderList.append(order)

        return orderList

    def employeeShowViewOrderInProgress(self):
        return self.employeeShowViewOrder("inProgress")

    def employeeShowViewOrderCanceled(self):
        return self.employeeShowViewOrder("canceled")

    def employeeShowViewOrderCompleted(self):
        return self.employeeShowViewOrder("completed")

    def employeePrepareEmployeeViewOrder(self, employeeID, orderList):
        employee = self.getLoggedEmployee(employeeID)
        employee.setCurrentlyViewedOrders(orderList)            # trzeba z tego skorzystac i dodac jako argument 1 z 3 funkcji powyzej

    def employeeShowPreparedViewOrder(self, employeeID):
        employee = self.getLoggedEmployee(employeeID)
        return employee.getCurrentlyViewedOrders()

    def employeeCancelOrder(self, orderID):
        orderID = int(orderID)

        ec = EmployeeController(self.db)
        ec.connect()
        ec.cancelOrder(orderID)
        ec.disconnect()

    def employeeConfirmOrder(self, orderID):
        orderID = int(orderID)

        ec = EmployeeController(self.db)
        ec.connect()
        ec.confirmOrder(orderID)
        ec.disconnect()

    def employeeAddProduct(self, name, price, category, amount):
        ec = EmployeeController(self.db)
        ec.connect()
        ec.addNewProduct(name, price, category, amount)
        ec.disconnect()

    def employeeEditProduct(self, productID, name, price, category, amount):
        productID = int(productID)

        ec = EmployeeController(self.db)
        ec.connect()

        ec.editProductName(name, productID)
        time.sleep(0.02)

        ec.editProductPrice(price, productID)
        time.sleep(0.02)

        ec.editProductCategory(category, productID)
        time.sleep(0.02)

        ec.editProductAmount(amount, productID)
        time.sleep(0.02)

        ec.disconnect()

    def employeeDeleteProduct(self, productID):
        productID = int(productID)
        ec = EmployeeController(self.db)
        ec.connect()

        ec.deleteProduct(productID)

        ec.disconnect()

    def employeeSearchOrderUsingID(self, orderID):
        ec = EmployeeController(self.db)
        ec.connect()
        orderFromDB = ec.searchOrderUsingID(orderID)[0]
        ec.disconnect()

        orderID, clientID, productID, clientName, clientSurname, clientEmail, clientPhone, clientAddress, productName, productCategory, productPrice, orderDate, orderStatus = orderFromDB

        order = EmployeeViewOrder(orderID, clientID, productID, clientName, clientSurname, clientEmail, clientPhone,
                                  clientAddress, productName, productCategory, productPrice, orderDate,
                                  orderStatus)

        return [order]
