from sklep_z_elektronika.model.databaseCommunication import DatabaseCommunication, ClientCommunicationWithDatabase


if __name__ == '__main__':
    db = DatabaseCommunication('localhost', 'root', 'mysql123', 'test_elektronika')
    cc = ClientCommunicationWithDatabase(db)
    cc.databaseCommunication.connect()

    username = "login1"
    password = "123"
    name = "test rejestracji1"
    surname = "xd1"
    email = "test1@email.test"
    phoneNumber = "545 324 212"
    address = "add"

    success = cc.register(username, password, name, surname, email, phoneNumber, address)
    print(success)

    success, _id = cc.login(username, password)
    print(success, _id, cc.getUserData(_id)[0])
    if success == 1:
        user = u



    # print(cc.searchProductUsingName('i'))
    # success, _id = cc.login("pawcio", "123")
    # print(success, _id)
    # db.connect()
    # db.login('papaj', 'dupa')
    # db.addToBasket(6, 33)
    # db.addNewProduct("xiaomi mi 11", 150.5, 'tel', 14)
    # db.disconnect()
    cc.databaseCommunication.disconnect()
