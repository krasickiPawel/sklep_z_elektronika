from sklep_z_elektronika.controller.mainController import MainController
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta

mc = MainController()
app = Flask(__name__)                       # serwer Flask ktory zaimportowalem wyzej
app.secret_key = "p&n"
app.permanent_session_lifetime = timedelta(hours=1)


def runApp():                               # wlacznik serwera pythonowego ktory umozliwia wyswietlanie stron w przegladarce
    app.run(debug=True)
    # app.run(host="0.0.0.0")


@app.route("/", methods=['GET', 'POST'])    # strona glowna www
def index():                                # ekran logowania klienta
    if request.method == "POST":            # samowywolanie lub z innej podstrony
        if "login" in request.form:
            clientID = mc.clientLogin(request.form.get("email"), request.form.get("password"))
            if clientID is not None:
                session["loggedClient"] = clientID
                return redirect(url_for("products"))
            # else:                         # tu jakis messageBox
            #     print("Nie udało się zalogować!")
        elif "register" in request.form:
            return redirect(url_for("register"))

    return render_template("index.html")    # jesli strona jest wywolana wpisujac localhost:5000/ w pasek przegladarki


@app.route("/products", methods=['GET', 'POST'])
def products():
    if request.method == "POST":
        pass

    productList = None
    return render_template("products.html", productList=productList)


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
