from databaseController import Database


if __name__ == '__main__':
    db = Database('localhost', 'root', 'mysql123', 'test_elektronika')
    db.connect()
    db.login('papaj', 'dupa')
    # db.addToBasket(6, 33)
    # db.addNewProduct("xiaomi mi 11", 150.5, 'tel', 14)
    db.disconnect()
