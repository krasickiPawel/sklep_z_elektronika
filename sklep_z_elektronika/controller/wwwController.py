from sklep_z_elektronika.controller.mainController import MainController
from flask import Flask, flash, render_template, request, redirect, url_for, session
from datetime import timedelta

mc = MainController()
app = Flask(__name__)                                                   # serwer Flask ktory zaimportowalem wyzej
app.secret_key = "p&n"
app.permanent_session_lifetime = timedelta(minutes=15)
currentProducts = dict()


def runApp():                                                           # wlacznik serwera pythonowego ktory umozliwia wyswietlanie stron w przegladarce
    app.run(debug=True)
    # app.run(host="0.0.0.0")


@app.route("/", methods=['GET', 'POST'])                                # strona glowna www (widok glowny klienta)
def index():
    if "loggedClient" not in session or not mc.clientCheckIfLogged(session.get("loggedClient")):
        return redirect(url_for("login"))
    else:
        if request.method == "POST":
            pass

        return render_template("products.html", productList=mc.showProducts(), loggedName=session.get('loggedClient'))


@app.route("/login", methods=['GET', 'POST'])
def login():                                                            # ekran logowania klienta
    if request.method == "POST":                                        # samowywolanie lub z innej podstrony
        if "login" in request.form:
            print("loguje...")
            clientID = mc.clientLogin(request.form.get("email-input"), request.form.get("password-input"))
            if clientID is not None:
                print("Gitara siema!")
                session["loggedClient"] = clientID
                currentProducts["products"] = mc.showProducts()
                print(currentProducts.get("products"))
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
        flash("Zostałeś poprawnie wylogowany")
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
            currentProducts["products"] = products
        else:
            flash("Nie znaleziono produktu o szukanej frazie")
        return redirect(url_for("index"))


@app.route("/register", methods=['GET', 'POST'])                        # TODO Natalka poćwicz na tym
def register():
    if request.method == "POST":
        pass

    return render_template("register.html")


@app.route("/history", methods=['GET', 'POST'])
def history():
    if "loggedClient" not in session or not mc.clientCheckIfLogged(session.get("loggedClient")):
        return redirect(url_for("login"))
    else:
        if request.method == "POST":
            pass

        return render_template("history.html")


@app.route("/basket", methods=['GET', 'POST'])
def basket():
    if "loggedClient" not in session or not mc.clientCheckIfLogged(session.get("loggedClient")):
        return redirect(url_for("login"))
    else:
        if request.method == "POST":
            pass

        return render_template("basket.html")


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