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
        return self.productName.capitalize()

    def getProductPrice(self):
        return self.productPrice

    def getOrderStatus(self):
        return self.status.capitalize()

    def getProductCategory(self):
        return self.productCategory.capitalize()

    def getOrderDate(self):
        return self.date

    def toString(self):
        return f"{self.orderID}, {self.productCategory}, {self.productName}, {self.productPrice}, {self.date}, {self.status}"


class EmployeeViewOrder:
    def __init__(self, orderID, clientID, productID, clientName, clientSurname, clientEmail, clientPhone, clientAddress,
                 productName, productCategory, productPrice, orderDate, orderStatus):
        self.orderID = orderID
        self.clientID = clientID
        self.productID = productID
        self.clientName = clientName
        self.clientSurname = clientSurname
        self.clientEmail = clientEmail
        self.clientPhone = clientPhone
        self.clientAddress = clientAddress
        self.productName = productName
        self.productCategory = productCategory
        self.productPrice = productPrice
        self.orderDate = orderDate
        self.orderStatus = orderStatus

    def getOrderID(self):
        return self.orderID

    def getClientID(self):
        return self.clientID

    def getProductID(self):
        return self.productID

    def getClientName(self):
        return self.clientName.capitalize()

    def getClientSurname(self):
        return self.clientSurname.capitalize()

    def getClientEmail(self):
        return self.clientEmail

    def getClientPhone(self):
        return self.clientPhone

    def getClientAddress(self):
        return self.clientAddress

    def getProductName(self):
        return self.productName.capitalize()

    def getProductCategory(self):
        return self.productCategory.capitalize()

    def getProductPrice(self):
        return self.productPrice

    def getOrderDate(self):
        return self.orderDate

    def getOrderStatus(self):
        return self.orderStatus.capitalize()
