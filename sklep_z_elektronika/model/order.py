class Order:
    def __init__(self, orderID, clientID, productID, date, status):
        self.orderID = orderID
        self.clientID = clientID
        self.productID = productID
        self.date = date
        self.status = status

    def getOrderID(self):
        return self.orderID

    def getProductID(self):
        return self.productID

    def getStatus(self):
        return self.status


class HistOrder:
    def __init__(self, orderID, productName, productCategory, productPrice, date, status):
        self.orderID = orderID
        self.productName = productName
        self.productCategory = productCategory
        self.productPrice = productPrice
        self.date = date
        self.status = status

    def getOrderID(self):
        return self.orderID

    def getProductName(self):
        return self.productName

    def getProductPrice(self):
        return self.productPrice

    def getOrderStatus(self):
        return self.status

    def getProductCategory(self):
        return self.productCategory

    def toString(self):
        return f"{self.orderID}, {self.productCategory}, {self.productName}, {self.productPrice}, {self.date}, {self.status}"
