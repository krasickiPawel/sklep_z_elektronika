from src.controller.databaseController import DatabaseController


class UserController(DatabaseController):
    def __init__(self, dataBase):
        super().__init__(dataBase)

    def checkProductAmount(self, productID):
        returnList = self.callStoredProcedureWithReturn('sprawdz_ilosc_produktu', [productID])
        if returnList is not None:
            return returnList[0][0]
        else:
            return None

    def showProducts(self):
        return self.showView('produkty')

    def searchProductUsingName(self, productName):
        return self.callStoredProcedureWithReturn('wyszukaj_produkt_po_nazwie', [productName])

    def loginUser(self, email, password, loginType):
        success = -1
        userID = 0
        return self.callLoginProcedure(loginType, [success, userID, email, password])

    def searchProductUsingID(self, productID):
        return self.callStoredProcedureWithReturn('wyszukaj_produkt_po_id', [productID])


class ClientController(UserController):
    def __init__(self, dataBase):
        super().__init__(dataBase)

    def getClientData(self, clientID):
        return self.callStoredProcedureWithReturn('zwroc_dane_klienta', [clientID])[0]

    def showFormattedBasket(self, clientID):
        return self.callStoredProcedureWithReturn('pokaz_koszyk', [clientID])

    def showBasketOrders(self, clientID):
        return self.callStoredProcedureWithReturn('zwroc_zamowienia_w_koszyku', [clientID])

    def addToBasket(self, clientID, productID):
        self.callStoredProcedureWithoutReturn('dodaj_do_koszyka', [clientID, productID])

    def removeFromBasket(self, orderID):
        self.callStoredProcedureWithoutReturn('usun_z_koszyka', [orderID])

    def buyProduct(self, order):
        productID = order.getProductID()
        productAmount = self.checkProductAmount(productID)
        if productAmount is not None and productAmount > 0:
            self.callStoredProcedureWithoutReturn('kup_produkt', [order.getOrderID()])
            return True
        else:
            return False

    def showShopHist(self, clientID):
        return self.callStoredProcedureWithReturn('pokaz_historie_zamowien_klienta', [clientID])

    def login(self, email, password):
        return self.loginUser(email, password, "zaloguj_klienta")

    def register(self, name, surname, email, phoneNumber, address, password):
        success = -1
        return self.callRegisterProcedure('zarejestruj_klienta', [success, name, surname, email, phoneNumber, address,
                                                                  password])

    def getBasketTotalPrice(self, clientID):
        totalPrice = 0
        return self.callRegisterProcedure('cena_koszyka', [totalPrice, clientID])


class EmployeeController(UserController):
    def __init__(self, dataBase):
        super().__init__(dataBase)

    def getEmployeeData(self, employeeID):
        return self.callStoredProcedureWithReturn('zwroc_dane_pracownika', [employeeID])[0]

    def showProductsUnavailable(self):
        return self.showView('produkty_niedostepne')

    def showOrdersCanceled(self):
        return self.showView('zamowienia_anulowane')

    def showOrdersInRealization(self):
        return self.showView('zamowienia_w_trakcie_realizacji')

    def showOrdersCompleted(self):
        return self.showView('zamowienia_zrealizowane')

    def login(self, email, password):
        return self.loginUser(email, password, "zaloguj_pracownika")

    def searchOrderUsingID(self, orderID):
        return self.callStoredProcedureWithReturn('wyszukaj_zamowienie_po_id', [orderID])

    def confirmOrder(self, orderID):
        self.callStoredProcedureWithoutReturn('potwierdz_zamowienie', [orderID])

    def deleteProduct(self, productID):
        self.callStoredProcedureWithoutReturn('usun_produkt', [productID])

    def cancelOrder(self, orderID):
        self.callStoredProcedureWithoutReturn('anuluj_zamowienie', [orderID])

    def editProductPrice(self, price, productID):
        self.callStoredProcedureWithoutReturn('edytuj_cene_produktu', [price, productID])

    def editProductAmount(self, amount, productID):
        self.callStoredProcedureWithoutReturn('edytuj_ilosc_produktu', [amount, productID])

    def editProductCategory(self, category, productID):
        self.callStoredProcedureWithoutReturn('edytuj_kategorie_produktu', [category, productID])

    def editProductName(self, name, productID):
        self.callStoredProcedureWithoutReturn('edytuj_nazwe_produktu', [name, productID])

    def addNewProduct(self, name, price, category, amount):
        self.callStoredProcedureWithoutReturn('wprowadz_nowy_produkt', [name, price, category, amount])
