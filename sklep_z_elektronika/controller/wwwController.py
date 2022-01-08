from sklep_z_elektronika.controller.mainController import MainController
from flask import Flask, flash, render_template, request, redirect, url_for, session
from datetime import timedelta

mc = MainController()
app = Flask(__name__)                                                   # serwer Flask ktory zaimportowalem wyzej
app.secret_key = "p&n"
app.permanent_session_lifetime = timedelta(minutes=15)


def runApp():                                                           # wlacznik serwera pythonowego ktory umozliwia wyswietlanie stron w przegladarce
    app.run(debug=True)
    # app.run(host="0.0.0.0")


@app.route("/", methods=['GET', 'POST'])                                # strona glowna www
def index():                                                            # ekran logowania klienta
    if "loggedClient" not in session:
        return redirect(url_for("login"))
    else:
        if request.method == "POST":
            pass

        productList = None
        return render_template("products.html", productList=productList)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":                                        # samowywolanie lub z innej podstrony
        if "login" in request.form:
            print("loguje...")
            clientID = mc.clientLogin(request.form.get("email-input"), request.form.get("password-input"))
            if clientID is not None:
                print("Gitara siema!")
                session["loggedClient"] = clientID
                return redirect(url_for("index"))
            else:
                print("Nie udało się zalogować!")
                flash("Nie udało się zalogować! Wprowadź poprawny login i hasło lub przejdź do rejestracji.", "error")
        elif "register" in request.form:
            return redirect(url_for("register"))

    return render_template("login.html")                                # jesli strona jest wywolana wpisujac localhost:5000/ w pasek przegladarki


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        pass

    return render_template("register.html")


@app.route("/history", methods=['GET', 'POST'])
def history():
    if request.method == "POST":
        pass

    return render_template("history.html")


@app.route("/basket", methods=['GET', 'POST'])
def basket():
    if request.method == "POST":
        pass

    return render_template("basket.html")


@app.route("/emp", methods=['GET', 'POST'])
def emp():
    if "loggedEmployee" not in session:
        return redirect(url_for("empLogin"))
    else:
        if request.method == "POST":
            pass

        return render_template("employee.html")


@app.route("/empLogin", methods=['GET', 'POST'])
def empLogin():
    if request.method == "POST":                                        # samowywolanie lub z innej podstrony
        if "login" in request.form:
            employeeID = mc.employeeLogin(request.form.get("email-input"), request.form.get("password-input"))
            if employeeID is not None:
                print("Gitara siema!")
                session["loggedEmployee"] = employeeID
                return redirect(url_for("emp"))
            else:
                print("Nie udało się zalogować!")
                flash("Nie udało się zalogować! Wprowadź poprawny login i hasło lub przejdź do rejestracji.", "error")

    return render_template("empLogin.html")                                # jesli strona jest wywolana wpisujac localhost:5000/ w pasek przegladarki