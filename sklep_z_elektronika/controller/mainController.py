from sklep_z_elektronika.model.databaseCommunication import DatabaseCommunication


if __name__ == '__main__':
    db = DatabaseCommunication('localhost', 'root', 'mysql123', 'test_elektronika')
    db.connect()
    # db.login('papaj', 'dupa')
    # db.addToBasket(6, 33)
    # db.addNewProduct("xiaomi mi 11", 150.5, 'tel', 14)
    db.disconnect()
