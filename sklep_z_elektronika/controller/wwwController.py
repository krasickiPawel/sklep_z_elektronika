from sklep_z_elektronika.controller.mainController import MainController
from flask import Flask, flash, render_template, request, redirect, url_for, session
from datetime import timedelta


mc = MainController("host", "user", "password", "database")
sessionTimeInSeconds = None
app = Flask(__name__)                                                   # serwer Flask ktory zaimportowalem wyzej


def runApp(host, user, password, database, givenSessionTime, secretKey, public=False):       # wlacznik serwera pythonowego ktory umozliwia wyswietlanie stron w przegladarce
    global mc
    global sessionTimeInSeconds

    mc = MainController(host, user, password, database)
    sessionTimeInSeconds = givenSessionTime
    app.permanent_session_lifetime = timedelta(seconds=sessionTimeInSeconds)
    app.secret_key = secretKey

    if public:
        app.run(host="0.0.0.0")
    else:
        app.run(debug=True)


@app.route("/", methods=['GET', 'POST'])                                # strona glowna www (widok glowny klienta)
def index():
    if "loggedClient" not in session or not mc.clientCheckIfLogged(session.get("loggedClient")):
        return redirect(url_for("login"))
    else:
        if request.method == "POST":
            for key in request.form:
                if key.startswith("buy."):
                    productID = key.partition('.')[-1]
                    productName = mc.clientAddToBasket(session.get("loggedClient"), productID)
                    if productName is not None:
                        flash(f"Dodano {productName} do koszyka.")                    # dodawanie do koszyka
                    else:
                        flash("Nie udało się dodać produktu do koszyka.")

        productList = mc.showProducts(session.get("loggedClient"), "client")
        productListLen = len(productList)
        parsedProductList = []
        rowList = []
        for i in range(productListLen):
            if i % 3 == 2:
                rowList.append(productList[i])
                parsedProductList.append(rowList.copy())
                rowList.clear()
            else:
                rowList.append(productList[i])
        parsedProductList.append(rowList.copy())

        return render_template("products.html", productList=parsedProductList, loggedID=session.get('loggedClient'))


@app.route("/login", methods=['GET', 'POST'])
def login():                                                            # ekran logowania klienta
    if "loggedClient" not in session or not mc.clientCheckIfLogged(session.get("loggedClient")):
        if request.method == "POST":                                        # samowywolanie lub z innej podstrony
            if "login" in request.form:
                print("loguje...")
                clientID = mc.clientLogin(request.form.get("email-input"), request.form.get("password-input"))
                if clientID is not None:
                    print("Gitara siema!")
                    session["loggedClient"] = clientID
                    mc.prepareProductsToShow(session.get("loggedClient"), "client", mc.getAllProductsFromDB())
                    mc.cleanMemory(session.get("loggedClient"), sessionTimeInSeconds, "client")
                    return redirect(url_for("index"))
                else:
                    print("Nie udało się zalogować!")
                    flash("Nie udało się zalogować! Wprowadź poprawny login i hasło lub przejdź do rejestracji.", "error")
            elif "register" in request.form:
                return redirect(url_for("register"))

        return render_template("login.html")                                # jesli strona jest wywolana wpisujac localhost:5000/ w pasek przegladarki
    else:
        return redirect(url_for("index"))


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    if "loggedClient" not in session or not mc.clientCheckIfLogged(session.get("loggedClient")):
        return redirect(url_for("login"))
    else:
        mc.clientLogout(session.get("loggedClient"))
        session.pop("loggedClient")
        flash("Zostałeś wylogowany")
        return redirect(url_for("login"))


@app.route("/search", methods=['GET', 'POST'])                          # TODO dużo do poprawy - zrobić jakoś filtrowanie i wyswietlanie produktow
def search():
    if "loggedClient" not in session or not mc.clientCheckIfLogged(session.get("loggedClient")):
        return redirect(url_for("login"))
    else:
        if request.method == "POST":
            pass
        phrase = request.form.get("search-input")
        products = mc.searchProductUsingName(phrase)
        if products is not None:
            mc.prepareProductsToShow(session.get("loggedClient"), "client", products)
        else:
            mc.prepareProductsToShow(session.get("loggedClient"), "client", mc.getAllProductsFromDB())
            flash("Nie znaleziono produktu o szukanej frazie")
        return redirect(url_for("index"))


@app.route("/register", methods=['GET', 'POST'])                        # TODO Natalka poćwicz na tym
def register():
    if request.method == "POST":
        for key in request.form:
            if key.startswith("register."):
                name = request.form.get("name-input")
                surname = request.form.get("surname-input")
                email = request.form.get("email-input")
                phoneNumber = request.form.get("phone-input")
                address = request.form.get("address-input")
                password = request.form.get("password-input")

                success = mc.clientRegister(name, surname, email, phoneNumber, address, password)
                if success:
                    flash("Zostałeś zarejestrowany!")
                    return redirect(url_for("login"))
                else:
                    flash("Nie udało się zarejestrować. Podany adres e-mail jest już w bazie.")
                    return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/shop", methods=['GET'])
def shop():
    if "loggedClient" not in session or not mc.clientCheckIfLogged(session.get("loggedClient")):
        return redirect(url_for("login"))
    else:
        mc.prepareProductsToShow(session.get("loggedClient"), "client", mc.getAllProductsFromDB())
        return redirect(url_for("index"))


@app.route("/history", methods=['GET', 'POST'])
def history():
    if "loggedClient" not in session or not mc.clientCheckIfLogged(session.get("loggedClient")):
        return redirect(url_for("login"))
    else:
        if request.method == "POST":
            pass

        shopHist = mc.clientShowShopHist(session.get("loggedClient"))
        if len(shopHist) > 0:
            shopHistEmpty = False
        else:
            shopHistEmpty = True

        return render_template("history.html", shopHist=shopHist, shopHistEmpty=shopHistEmpty)


@app.route("/basket", methods=['GET', 'POST'])
def basket():
    if "loggedClient" not in session or not mc.clientCheckIfLogged(session.get("loggedClient")):
        return redirect(url_for("login"))
    else:
        if request.method == "POST":
            for key in request.form:
                if key.startswith("remove."):
                    orderID = key.partition('.')[-1]
                    if not mc.clientRemoveFromBasket(session.get("loggedClient"), orderID):
                        flash("Usuwanie produktu z koszyka nie powiodło się!")
                if key.startswith("buyAll"):
                    if mc.clientBuyProductsInBasket(session.get("loggedClient")):
                        flash("Gratulujemy wyboru! Zamówione produkty czekają na opłacenie i weryfikację przez pracownika.")
                    else:
                        flash("Wystąpiły problemy podczas składania zamówienia na produkty znajdujące się w twoim "
                              "koszyku. Możliwe, że niektóre produkty są już niedostępne.")

        basketList, totalPrice = mc.clientShowFormattedBasket(session.get("loggedClient"))

        if len(basketList) == 0:
            basketEmpty = True
        else:
            basketEmpty = False

        return render_template("basket.html", orderList=basketList, totalPrice=totalPrice, basketEmpty=basketEmpty)


@app.route("/emp", methods=['GET', 'POST'])
def emp():
    if "loggedEmployee" not in session or not mc.employeeCheckIfLogged(session.get("loggedEmployee")):
        return redirect(url_for("loginEmp"))
    else:
        if request.method == "POST":
            for key in request.form:
                if key.startswith("remove."):
                    productID = key.partition('.')[-1]
                    session["productIDToEditRemove"] = productID
                    return redirect(url_for("deleteItemsEmp"))
                if key.startswith("edit."):
                    productID = key.partition('.')[-1]
                    session["productIDToEditRemove"] = productID
                    return redirect(url_for("editItemsEmp"))

        productList = mc.showProducts(session.get("loggedEmployee"), "employee")
        productListLen = len(productList)
        parsedProductList = []
        rowList = []
        for i in range(productListLen):
            if i % 3 == 2:
                rowList.append(productList[i])
                parsedProductList.append(rowList.copy())
                rowList.clear()
            else:
                rowList.append(productList[i])
        parsedProductList.append(rowList.copy())

        return render_template("productsEmp.html", productList=parsedProductList, modify=session.get('modify'))


@app.route("/productsEmp", methods=['GET', 'POST'])
def productsEmp():
    if "loggedEmployee" not in session or not mc.employeeCheckIfLogged(session.get("loggedEmployee")):
        return redirect(url_for("loginEmp"))
    else:
        mc.prepareProductsToShow(session.get("loggedEmployee"), "employee", mc.getAllProductsFromDB())
        session["modify"] = False
        return redirect(url_for("emp"))


@app.route("/loginEmp", methods=['GET', 'POST'])
def loginEmp():
    if "loggedEmployee" not in session or not mc.employeeCheckIfLogged(session.get("loggedEmployee")):
        if request.method == "POST":                                        # samowywolanie lub z innej podstrony
            if "login" in request.form:
                employeeID = mc.employeeLogin(request.form.get("email-input"), request.form.get("password-input"))
                if employeeID is not None:
                    print("Gitara siema!")
                    session["loggedEmployee"] = employeeID
                    mc.cleanMemory(session.get("loggedEmployee"), sessionTimeInSeconds, "employee")
                    return redirect(url_for("productsEmp"))
                else:
                    print("Nie udało się zalogować!")
                    flash("Nie udało się zalogować! Wprowadź poprawny login i hasło.", "error")

        return render_template("loginEmp.html")                                # jesli strona jest wywolana wpisujac localhost:5000/ w pasek przegladarki
    else:
        return redirect(url_for("emp"))


@app.route("/logoutEmp", methods=['GET', 'POST'])
def logoutEmp():
    if "loggedEmployee" not in session or not mc.employeeCheckIfLogged(session.get("loggedEmployee")):
        return redirect(url_for("loginEmp"))
    else:
        mc.employeeLogout(session.get("loggedClient"))
        session.pop("loggedEmployee")
        flash("Zostałeś wylogowany")
        return redirect(url_for("loginEmp"))


@app.route("/productsUnavailableEmp", methods=['GET', 'POST'])                             # widok glowny pracownika
def productsUnavailableEmp():
    if "loggedEmployee" not in session or not mc.employeeCheckIfLogged(session.get("loggedEmployee")):
        return redirect(url_for("loginEmp"))
    else:
        if request.method == "POST":
            pass
        mc.prepareProductsToShow(session.get("loggedEmployee"), "employee", mc.employeeShowProductsUnavailable())
        session["modify"] = False
        return redirect(url_for("emp"))


@app.route("/ordersInProgressEmp", methods=['GET', 'POST'])                             # widok glowny pracownika
def ordersInProgressEmp():
    if "loggedEmployee" not in session or not mc.employeeCheckIfLogged(session.get("loggedEmployee")):
        return redirect(url_for("loginEmp"))
    else:
        if request.method == "POST":
            for key in request.form:
                if key.startswith("confirm."):
                    orderID = key.partition('.')[-1]
                    mc.employeeConfirmOrder(orderID)
                    flash("Zrealizowano zamówienie!")
                    return redirect(url_for("ordersInProgressEmp"))
                if key.startswith("cancel."):
                    orderID = key.partition('.')[-1]
                    mc.employeeCancelOrder(orderID)
                    flash("Odrzuciłeś zamówienie!")
                    return redirect(url_for("ordersInProgressEmp"))

        orderList = mc.employeeShowViewOrderInProgress()
        if len(orderList) > 0:
            ordersEmpty = False
        else:
            ordersEmpty = True

        return render_template("viewOrders.html", orderList=orderList, inProgress=True, ordersEmpty=ordersEmpty)


@app.route("/ordersCompletedEmp", methods=['GET', 'POST'])  # widok glowny pracownika
def ordersCompletedEmp():
    if "loggedEmployee" not in session or not mc.employeeCheckIfLogged(session.get("loggedEmployee")):
        return redirect(url_for("loginEmp"))
    else:
        if request.method == "POST":
            pass

        orderList = mc.employeeShowViewOrderCompleted()
        if len(orderList) > 0:
            ordersEmpty = False
        else:
            ordersEmpty = True

        return render_template("viewOrders.html", orderList=orderList, inProgress=False, ordersEmpty=ordersEmpty)


@app.route("/ordersCanceledEmp", methods=['GET', 'POST'])  # widok glowny pracownika
def ordersCanceledEmp():
    if "loggedEmployee" not in session or not mc.employeeCheckIfLogged(session.get("loggedEmployee")):
        return redirect(url_for("loginEmp"))
    else:
        if request.method == "POST":
            pass

        orderList = mc.employeeShowViewOrderCanceled()
        if len(orderList) > 0:
            ordersEmpty = False
        else:
            ordersEmpty = True

        return render_template("viewOrders.html", orderList=orderList, inProgress=False, ordersEmpty=ordersEmpty)


@app.route("/modifyItemsEmp", methods=['GET', 'POST'])
def modifyItemsEmp():
    if "loggedEmployee" not in session or not mc.employeeCheckIfLogged(session.get("loggedEmployee")):
        return redirect(url_for("loginEmp"))
    else:
        session["modify"] = True
        mc.prepareProductsToShow(session.get("loggedEmployee"), "employee", mc.getAllProductsFromDB())
        return redirect(url_for("emp"))


@app.route("/addItemsEmp", methods=['GET', 'POST'])                     # przekierowanie po edit = False
def addItemsEmp():
    if "loggedEmployee" not in session or not mc.employeeCheckIfLogged(session.get("loggedEmployee")):
        return redirect(url_for("loginEmp"))
    else:
        session["edit"] = False
        session["delete"] = False
        return redirect(url_for("addEditEmp"))


@app.route("/editItemsEmp", methods=['GET', 'POST'])                     # przekierowanie po ustawieniu True
def editItemsEmp():
    if "loggedEmployee" not in session or not mc.employeeCheckIfLogged(session.get("loggedEmployee")):
        return redirect(url_for("loginEmp"))
    else:
        session["edit"] = True
        session["delete"] = False
        return redirect(url_for("addEditEmp"))


@app.route("/deleteItemsEmp", methods=['GET', 'POST'])
def deleteItemsEmp():
    if "loggedEmployee" not in session or not mc.employeeCheckIfLogged(session.get("loggedEmployee")):
        return redirect(url_for("loginEmp"))
    else:
        session["edit"] = False
        session["delete"] = True
        return redirect(url_for("addEditEmp"))


@app.route("/addEditEmp", methods=['GET', 'POST'])
def addEditEmp():
    if "loggedEmployee" not in session or not mc.employeeCheckIfLogged(session.get("loggedEmployee")):
        return redirect(url_for("loginEmp"))
    else:
        if request.method == "POST":
            for key in request.form:
                if key.startswith("add."):
                    mc.employeeAddProduct(request.form.get("name-input"), request.form.get("price-input"),
                                          request.form.get("category-input"), request.form.get("amount-input"))

                    flash("Dodano nowy produkt!")
                    return redirect(url_for("productsEmp"))

                elif key.startswith("edit."):
                    session["edit"] = False
                    productID = key.partition('.')[-1]
                    mc.employeeEditProduct(productID, request.form.get("edit-name-input"), request.form.get("edit-price-input"),
                                           request.form.get("edit-category-input"), request.form.get("edit-amount-input"))

                    flash("Edytowano produkt!")
                    return redirect(url_for("productsEmp"))

                elif key.startswith("delete."):
                    session["delete"] = False
                    productID = key.partition('.')[-1]
                    mc.employeeDeleteProduct(productID)

                    flash("Usunięto produkt!")
                    return redirect(url_for("productsEmp"))

                elif key.startswith("cancel."):
                    session["delete"] = False
                    return redirect(url_for("modifyItemsEmp"))

        if session.get("edit") or session.get("delete"):
            product = mc.searchProductUsingID(session.get("productIDToEditRemove"))[0]
        else:
            product = None

        return render_template("productAddEdit.html", edit=session.get("edit"), delete=session.get("delete"), product=product)


@app.route("/searchEmp", methods=['GET', 'POST'])
def searchEmp():
    if "loggedEmployee" not in session or not mc.employeeCheckIfLogged(session.get("loggedEmployee")):
        return redirect(url_for("loginEmp"))
    else:
        if request.method == "POST":
            for key in request.form:
                if key.startswith("searchProductName."):
                    phrase = request.form.get("product-name-input")
                    products = mc.searchProductUsingName(phrase)
                    if products is not None:
                        mc.prepareProductsToShow(session.get("loggedEmployee"), "employee", products)
                    else:
                        mc.prepareProductsToShow(session.get("loggedEmployee"), "employee", mc.getAllProductsFromDB())
                        flash("Nie znaleziono produktu o szukanej frazie")

                    # session["modify"] = False
                    return redirect(url_for("emp"))

                elif key.startswith("searchProductID."):
                    productID = request.form.get("product-id-input")
                    products = mc.searchProductUsingID(productID)
                    if len(products) > 0:
                        mc.prepareProductsToShow(session.get("loggedEmployee"), "employee", products)
                    else:
                        mc.prepareProductsToShow(session.get("loggedEmployee"), "employee", mc.getAllProductsFromDB())
                        flash("Nie znaleziono produktu o podanym id")

                    return redirect(url_for("emp"))

                elif key.startswith("searchOrderID."):
                    orderID = request.form.get("order-id-input")
                    session["orderIDToBeViewed"] = orderID
                    return redirect(url_for("singleOrder"))

        return render_template("searchEmp.html")


@app.route("/singleOrder", methods=['GET', 'POST'])
def singleOrder():
    if "loggedEmployee" not in session or not mc.employeeCheckIfLogged(session.get("loggedEmployee")):
        return redirect(url_for("loginEmp"))
    else:
        orderList = mc.employeeSearchOrderUsingID(session.get("orderIDToBeViewed"))
        if len(orderList) > 0:
            return render_template("viewOrders.html", orderList=orderList, inProgress=True, ordersEmpty=False)
        else:
            flash("Nie znaleziono zamówienia o podanym id")
            return redirect(url_for("searchEmp"))
