from sklep_z_elektronika.controller.databaseController import DatabaseController
from datetime import datetime


class UserController(DatabaseController):
    def __init__(self, dataBase):
        super().__init__(dataBase)

    def checkProductAmount(self, productID):
        return self.callStoredProcedureWithReturn('sprawdz_ilosc_produktu', [productID])

    def getUserData(self, userID):
        return self.callStoredProcedureWithReturn('zwroc_dane_uzytkownika', [userID])

    def showProducts(self):
        return self.show('produkty')

    def searchProductUsingName(self, productName):
        return self.callStoredProcedureWithReturn('wyszukaj_produkt_po_nazwie', [productName])

    def loginUser(self, username, password, userType):
        success = -1
        userID = 0
        return self.callLoginProcedure('zaloguj_uzytkownika', [success, userID, username, password, userType])


class ClientController(UserController):
    def __init__(self, dataBase):
        super().__init__(dataBase)

    def showBasket(self, userID):
        return self.callStoredProcedureWithReturn('pokaz_koszyk', [userID])

    def addToBasket(self, userID, productID):
        self.callStoredProcedureWithoutReturn('dodaj_do_koszyka', [userID, productID, datetime.now()])

    def buyProduct(self, orderID):
        self.callStoredProcedureWithoutReturn('kup_produkt', [orderID])

    def showShopHist(self, userID):
        return self.callStoredProcedureWithReturn('pokaz_historie_zamowien_klienta', [userID])

    def login(self, username, password):
        return self.loginUser(username, password, "klient")

    def register(self, username, password, name, surname, email, phoneNumber, address):
        success = -1
        return self.callRegisterProcedure('zarejestruj_uzytkownika', [success, username, password, name, surname, email,
                                                                      phoneNumber, address, "klient"])


class EmployeeController(UserController):
    def __init__(self, dataBase):
        super().__init__(dataBase)

    def showProductsUnavailable(self):
        return self.show('produkty_niedostepne')

    def showOrdersCanceled(self):
        return self.show('zamowienia_anulowane')

    def showOrdersInRealization(self):
        return self.show('zamowienia_w_trakcie_realizacji')

    def showOrdersCompleted(self):
        return self.show('zamowienia_zrealizowane')

    def login(self, username, password):
        return self.loginUser(username, password, "pracownik")

    def searchOrderUsingID(self, orderID):
        return self.callStoredProcedureWithReturn('wyszukaj_zamowienie_po_id', [orderID])

    def searchProductUsingID(self, productID):
        return self.callStoredProcedureWithReturn('wyszukaj_produkt_po_id', [productID])

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
