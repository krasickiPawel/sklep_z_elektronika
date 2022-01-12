from src.view.www import app, runApp
import os


def fileRead(fileName):
    with open(fileName) as file:
        configInfo = file.readlines()
    for i in range(len(configInfo)):
        configInfo[i] = configInfo[i].removesuffix("\n")
    return configInfo


def main():
    fileToRead = os.path.abspath('config.txt')
    config = fileRead(fileToRead)

    if config is not None and len(config) == 8:
        public, debug, host, user, password, database, givenSessionTime, secretKey = config
        public = bool(int(public))
        debug = bool(int(debug))
        givenSessionTime = int(givenSessionTime)

        runApp(host, user, password, database, givenSessionTime, secretKey, public, debug)
    else:
        print("Brak odpowiedniego pliku konfiguracyjnego lub nie zawiera on wszystkich parametrów!")
        exit()


if __name__ == '__main__':
    main()

    # name = "main"
    # surname = "surmain"
    # email = "main@test.test"
    # phoneNumber = "000 000 000"
    # address = "main 22"
    # password = "passmain"
    #
    # loggedClient = None
    # loggedEmployee = None
    #
    # mc = MainController()


    # rejestracja nowego klienta
    # success = mc.clientRegister(name, surname, email, phoneNumber, address, password)
    # if success:
    #     print("Zarejestrowano")
    # else:
    #     print("Nie udało się zarejestrować")


    # logowanie klienta
    # clientID = mc.clientLogin(email, password)
    # if clientID is not None:
    #     loggedClient = clientID
    #     print("Zalogowano")
    # else:
    #     print("Nie udało się zalogować!")


    # wyswietlanie produktow
    # products = mc.showProducts()
    # if products is not None:
    #     for product in products:
    #         if product.getAmount() == 0:
    #             print("Produkt niedostępny", product.getProductID(), product.getName(), product.getPrice(),
    #                   product.getCategory(), product.getAmount())
    #         else:
    #             print(product.getProductID(), product.getName(), product.getPrice(), product.getCategory(),
    #               product.getAmount())
    # else:
    #     print("Chwilowo produkty są niedostępne")


    # wyszukiwanie produktu po nazwie
    # products = mc.searchProductUsingName("msi")
    # if products is not None:
    #     for product in products:
    #         print(product.getProductID(), product.getName(), product.getPrice(), product.getCategory(),
    #               product.getAmount())
    # else:
    #     print("Nie znaleziono produktu o szukanej frazie")


    # wyswietlanie historii zamowien klienta
    # shopHist = mc.clientShowShopHist(clientID)
    # if len(shopHist) == 0:
    #     print("Jeszcze nic nie zamówiłeś")
    # else:
    #     for histOrder in shopHist:
    #         print(histOrder.getOrderID(), histOrder.getProductName(), histOrder.getProductPrice(), histOrder.getOrderStatus())


    # dodawanie produktow do koszyka
    # productID = 5
    # success = mc.clientAddToBasket(clientID, productID)
    # print(success)
    # if success:
    #     basketProductList = mc.clientShowFormattedBasket(clientID)
    #     for basketProduct in basketProductList:
    #         print(basketProduct[0], basketProduct[1], basketProduct[2], basketProduct[3])
    # else:
    #     print("Dodawanie produktu do koszyka nie powiodło się!")


    # wyswietlanie sformatowanego koszyka
    # basketProductList = mc.clientShowFormattedBasket(clientID)
    # if len(basketProductList) == 0:
    #     print("Koszyk jest pusty")
    # else:
    #     for basketProduct in basketProductList:
    #         print(basketProduct[0], basketProduct[1], basketProduct[2], basketProduct[3])


    # wyswietlanie calego (brzydkiego) koszyka
    # basketOrderList = mc.clientShowBasketOrders(clientID)
    # if len(basketOrderList) == 0:
    #     print("Koszyk jest pusty")
    # else:
    #     for order in basketOrderList:
    #         print(order.getOrderID(), order.getProductID(), order.getStatus())


    # usuwanie zamowienia z koszyka
    # orderID = 10
    # success = mc.clientRemoveFromBasket(clientID, orderID)
    # print(success)
    # if success:
    #     basketProductList = mc.clientShowFormattedBasket(clientID)
    #     for basketProduct in basketProductList:
    #         print(basketProduct[0], basketProduct[1], basketProduct[2], basketProduct[3])
    # else:
    #     print("Nie udało się usunąć produktu z koszyka!")


    # kupowanie produktow znajdujacych sie w koszyku
    # successfullyBought = mc.clientBuyProductsInBasket(clientID)
    # for order in successfullyBought:
    #     product = mc.searchProductUsingID(order.productID)
    #     print("Zamówiono:", product.getName(), product.getCategory(), product.getPrice())
    # basketProductList = mc.clientShowFormattedBasket(clientID)
    # for basketProduct in basketProductList:
    #     print("Niedostępne:", basketProduct[0], basketProduct[1], basketProduct[2], basketProduct[3])


    # wylogowywanie klienta
    # mc.clientLogout(clientID)
    # print("Zostałeś wylogowany!")