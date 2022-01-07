class Product:
    def __init__(self, productID, name, price, category, amount):
        self.productID = productID
        self.name = name
        self.price = price
        self.category = category
        self.amount = amount

    def getProductID(self):
        return self.productID

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price

    def getCategory(self):
        return self.category

    def getAmount(self):
        return self.amount

    def toString(self):
        return f"{self.productID}, {self.name}, {self.price}, {self.category}, {self.amount}"
