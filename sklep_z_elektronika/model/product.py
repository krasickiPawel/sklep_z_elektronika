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
        return self.name.capitalize()

    def getPrice(self):
        return self.price

    def getCategory(self):
        return self.category.capitalize()

    def getAmount(self):
        if self.amount > 0:
            return f"{self.amount} dostępnych sztuk"
        else:
            return 'Produkt niedostępny'

    def isAvailable(self):
        if self.amount > 0:
            return "white"
        else:
            return "LightCoral"

    def toString(self):
        return f"{self.productID}, {self.name}, {self.price}, {self.category}, {self.amount}"
