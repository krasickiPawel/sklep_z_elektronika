from sklep_z_elektronika.controller.mainController import MainController
from flask import Flask, flash, render_template, request, redirect, url_for, session
from datetime import timedelta


mc = MainController()
sessionTimeInSeconds = 900

app = Flask(__name__)                                                   # serwer Flask ktory zaimportowalem wyzej
app.secret_key = "p&n"
app.permanent_session_lifetime = timedelta(seconds=sessionTimeInSeconds)


def runApp():                                                           # wlacznik serwera pythonowego ktory umozliwia wyswietlanie stron w przegladarce
    app.run(debug=True)
    # app.run(host="0.0.0.0")


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
        pass

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


@app.route("/emp", methods=['GET', 'POST'])                             # widok glowny pracownika
def emp():
    if "loggedEmployee" not in session:
        return redirect(url_for("loginEmp"))
    else:
        if request.method == "POST":
            pass

        return render_template("employee.html")


@app.route("/loginEmp", methods=['GET', 'POST'])
def loginEmp():
    if request.method == "POST":                                        # samowywolanie lub z innej podstrony
        if "login" in request.form:
            employeeID = mc.employeeLogin(request.form.get("email-input"), request.form.get("password-input"))
            if employeeID is not None:
                print("Gitara siema!")
                session["loggedEmployee"] = employeeID
                return redirect(url_for("emp"))
            else:
                print("Nie udało się zalogować!")
                flash("Nie udało się zalogować! Wprowadź poprawny login i hasło.", "error")

    return render_template("loginEmp.html")                                # jesli strona jest wywolana wpisujac localhost:5000/ w pasek przegladarki