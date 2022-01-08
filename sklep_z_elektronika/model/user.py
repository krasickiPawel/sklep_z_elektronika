class User:
    def __init__(self, userID, name, surname, email, phoneNumber, address, password):
        self.id = userID
        self.name = name
        self.surname = surname
        self.email = email
        self.phoneNumber = phoneNumber
        self.address = address
        self.password = password
        self.timer = None
        self.currentlyViewedProducts = None     # indywidualna lista wyświetlanych produktów

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

    def setTimer(self, timer):
        self.timer = timer

    def startTimer(self):
        self.timer.start()

    def setCurrentlyViewedProducts(self, productList):
        self.currentlyViewedProducts = productList

    def getCurrentlyViewedProducts(self):
        return self.currentlyViewedProducts


class Client(User):
    def __init__(self, userID, name, surname, email, phoneNumber, address, password):
        super().__init__(userID, name, surname, email, phoneNumber, address, password)
        self.shopHist = []                      # reszta orders klienta
        self.basket = []                        # orders "w koszyku"

    def addOrderShopHist(self, order):
        self.shopHist.append(order)

    def removeOrderShopHist(self, order):
        self.shopHist.remove(order)

    def addOrderBasket(self, order):
        self.basket.append(order)

    def removeOrderBasket(self, order):
        self.basket.remove(order)

    def getBasket(self):
        return self.basket

    def getShopHist(self):
        return self.shopHist


class Employee(User):
    def __init__(self, userID, name, surname, email, phoneNumber, address, password, position, salary):
        super().__init__(userID, name, surname, email, phoneNumber, address, password)
        self.position = position
        self.salary = salary

