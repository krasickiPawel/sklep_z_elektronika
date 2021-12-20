import mysql.connector
from datetime import datetime


class Database:
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

    def showProducts(self):
        self.show('produkty')

    def showProductsUnavailable(self):
        self.show('produkty_niedostepne')

    def showOrdersCanceled(self):
        self.show('zamowienia_anulowane')

    def showOrdersInRealization(self):
        self.show('zamowienia_w_trakcie_realizacji')

    def showOrdersCompleted(self):
        self.show('zamowienia_zrealizowane')

    def showBasket(self, userID):
        self.callStoredProcedureWithReturn('pokaz_koszyk', [userID])

    def addToBasket(self, userID, productID):
        self.callStoredProcedureWithoutReturn('dodaj_do_koszyka', [userID, productID, datetime.now()])

    def addNewProduct(self, name, price, category, amount):
        self.callStoredProcedureWithoutReturn('wprowadz_nowy_produkt', [name, price, category, amount])

    def checkProductAmount(self, productID):
        self.callStoredProcedureWithReturn('sprawdz_ilosc_produktu', [productID])

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

    def buyProduct(self, orderID):
        self.callStoredProcedureWithoutReturn('kup_produkt', [orderID])

    def showShopHist(self, userID):
        self.callStoredProcedureWithReturn('pokaz_historie_zamowien_klienta', [userID])

    def confirmOrder(self, orderID):
        self.callStoredProcedureWithoutReturn('potwierdz_zamowienie', [orderID])

    def deleteProduct(self, productID):
        self.callStoredProcedureWithoutReturn('usun_produkt', [productID])

    def searchProductUsingID(self, productID):
        self.callStoredProcedureWithReturn('wyszukaj_produkt_po_id', [productID])

    def searchProductUsingName(self, productName):
        self.callStoredProcedureWithReturn('wyszukaj_produkt_po_nazwie', [productName])

    def searchOrderUsingID(self, orderID):
        self.callStoredProcedureWithReturn('wyszukaj_zamowienie_po_id', [orderID])

    def login(self, username, password):
        self.callStoredProcedureWithReturn('zaloguj_uzytkownika', [username, password])