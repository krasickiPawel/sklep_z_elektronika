import mysql.connector
from datetime import datetime


class DatabaseCommunication:
    def __init__(self, host, user, password, database):
        self.db = None
        self.cursor = None
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        self.db = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        self.cursor = self.db.cursor()

    def disconnect(self):
        self.cursor.close()
        self.db.close()

    def show(self, view):
        try:
            self.cursor.execute(f'SELECT * FROM {view}')
            resultList = self.cursor.fetchall()
            for result in resultList:
                print(result)
        except Exception as e:
            print(e)

    def callStoredProcedureWithoutReturn(self, name, args):
        try:
            self.cursor.callproc(f'{name}', args)
            self.db.commit()
        except mysql.connector.Error as e:
            print(e)

    def callStoredProcedureWithReturn(self, name, args):
        try:
            self.cursor.callproc(name, args)
            for result in self.cursor.stored_results():
                print(result.fetchall())
        except mysql.connector.Error as e:
            print(e)

    def checkProductAmount(self, productID):
        self.callStoredProcedureWithReturn('sprawdz_ilosc_produktu', [productID])


class ClientCommunicationWithDatabase:
    def __init__(self, databaseCommunication):
        self.databaseCommunication = databaseCommunication

    def showProducts(self):
        self.databaseCommunication.show('produkty')

    def showBasket(self, userID):
        self.databaseCommunication.callStoredProcedureWithReturn('pokaz_koszyk', [userID])

    def addToBasket(self, userID, productID):
        self.databaseCommunication.callStoredProcedureWithoutReturn('dodaj_do_koszyka', [userID, productID, datetime.now()])

    def buyProduct(self, orderID):
        self.databaseCommunication.callStoredProcedureWithoutReturn('kup_produkt', [orderID])

    def showShopHist(self, userID):
        self.databaseCommunication.callStoredProcedureWithReturn('pokaz_historie_zamowien_klienta', [userID])

    def searchProductUsingName(self, productName):
        self.databaseCommunication.callStoredProcedureWithReturn('wyszukaj_produkt_po_nazwie', [productName])

    def login(self, username, password):
        self.databaseCommunication.callStoredProcedureWithReturn('zaloguj_uzytkownika', [username, password])

    def register(self, username, password, name, surname, email, phoneNumber, address):
        self.databaseCommunication.callStoredProcedureWithoutReturn('zarejestruj_uzytkownika', [username, password, name, surname, email, phoneNumber, address])


class EmployeeCommunicationWithDatabase:
    def __init__(self, databaseCommunication):
        self.databaseCommunication = databaseCommunication

    def showProductsUnavailable(self):
        self.databaseCommunication.show('produkty_niedostepne')

    def showOrdersCanceled(self):
        self.databaseCommunication.show('zamowienia_anulowane')

    def showOrdersInRealization(self):
        self.databaseCommunication.show('zamowienia_w_trakcie_realizacji')

    def showOrdersCompleted(self):
        self.databaseCommunication.show('zamowienia_zrealizowane')

    def login(self, username, password):
        self.databaseCommunication.callStoredProcedureWithReturn('zaloguj_uzytkownika', [username, password])

    def searchOrderUsingID(self, orderID):
        self.databaseCommunication.callStoredProcedureWithReturn('wyszukaj_zamowienie_po_id', [orderID])

    def searchProductUsingID(self, productID):
        self.databaseCommunication.callStoredProcedureWithReturn('wyszukaj_produkt_po_id', [productID])

    def searchProductUsingName(self, productName):
        self.databaseCommunication.callStoredProcedureWithReturn('wyszukaj_produkt_po_nazwie', [productName])

    def confirmOrder(self, orderID):
        self.databaseCommunication.callStoredProcedureWithoutReturn('potwierdz_zamowienie', [orderID])

    def deleteProduct(self, productID):
        self.databaseCommunication.callStoredProcedureWithoutReturn('usun_produkt', [productID])

    def cancelOrder(self, orderID):
        self.databaseCommunication.callStoredProcedureWithoutReturn('anuluj_zamowienie', [orderID])

    def editProductPrice(self, price, productID):
        self.databaseCommunication.callStoredProcedureWithoutReturn('edytuj_cene_produktu', [price, productID])

    def editProductAmount(self, amount, productID):
        self.databaseCommunication.callStoredProcedureWithoutReturn('edytuj_ilosc_produktu', [amount, productID])

    def editProductCategory(self, category, productID):
        self.databaseCommunication.callStoredProcedureWithoutReturn('edytuj_kategorie_produktu', [category, productID])

    def editProductName(self, name, productID):
        self.databaseCommunication.callStoredProcedureWithoutReturn('edytuj_nazwe_produktu', [name, productID])

    def addNewProduct(self, name, price, category, amount):
        self.databaseCommunication.callStoredProcedureWithoutReturn('wprowadz_nowy_produkt', [name, price, category, amount])

    def checkProductAmount(self, productID):
        self.databaseCommunication.checkProductAmount(productID)
