import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    #owned shares, prices of each stock, totalvalue of shares, current cash, grand total value.

    #get first symbol, shares
    portfolio = db.execute("SELECT symbol, shares FROM portfolio WHERE id = :id", id=session["user_id"])

    #lookup symbol, then add to dictonary list, holdings = total value of that stock

    sum41 = 0

    for i in range(len(portfolio)):
        quote2 = lookup(portfolio[i]['symbol'])

        #add to dictonary list

        portfolio[i]['stockprice'] = quote2['price']
        portfolio[i]['company'] = quote2['name']
        portfolio[i]['holdings'] = round( portfolio[i]['shares'] * portfolio[i]['stockprice'], 2)
        sum41 = sum41 + portfolio[i]['holdings']

    #current cash and sum up
    cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
    cashnum = round(cash[0]['cash'], 2)
    sum41= round(sum41 + cashnum, 2)

    return render_template("index.html", portfolio = portfolio, cash = cashnum, sum41 = sum41)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:

        global symbol
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("wrong Symbol input")

        global shares
        shares = request.form.get("shares")
        shares = int(shares)

        if shares < 0:
            return apology("please enter a positive number")

        global quote1
        quote1 = lookup(symbol)
        rows = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])

        global cash1
        cash1 = rows[0]["cash"]

        global total1
        total1 = shares * quote1["price"]
        return redirect("/buy2")


@app.route("/buy2", methods=["GET", "POST"])
@login_required
def buy2():
    if request.method == "GET":
        return render_template("buy2.html", shares=shares, name=quote1["name"] , price=quote1["price"], symbol=quote1["symbol"], cash=cash1 )
    else:
        cashafter = cash1 - total1
        rows = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])

        #cash check
        if cashafter < 0:
            return apology("u need more cash yo")

        else:
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=cashafter, id=session["user_id"])

            ##new table or update history table
            result= db.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='history'")
            if not result:
                db.execute("CREATE TABLE history (transid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, id INT NOT NULL, symbol TEXT NOT NULL, shares NUMERIC NOT NULL, price NUMERIC NOT NULL, cashbefore NUMERIC NOT NULL, cashafter NUMERIC NOT NULL, date datetime NOT NULL, action TEXT NOT NULL)")

            #insert
            db.execute("INSERT INTO history (id, symbol, shares, price, cashbefore, cashafter, date, action) VALUES (:id, :symbol, :shares, :price, :cashbefore, :cashafter, CURRENT_TIMESTAMP, :action)",
            id=session["user_id"], symbol=symbol, shares=shares, price=quote1["price"], cashbefore=cash1, cashafter=cashafter, action = "buy" )

            ##new table or update portfolio table
            result2= db.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='portfolio'")
            if not result2:
                db.execute("CREATE TABLE portfolio (id INTEGER NOT NULL, symbol TEXT NOT NULL , shares NUMERIC NOT NULL)")

            #check if shares exists for current user
            sharecheck = db.execute("SELECT COUNT(*) FROM portfolio WHERE (id = :id AND symbol = :symbol)", id=session["user_id"], symbol=symbol)

            if sharecheck[0]['COUNT(*)'] == 0:
                db.execute("INSERT §INTO portfolio (id, symbol, shares) VALUES (:id, :symbol, :shares)", id=session["user_id"], symbol=symbol, shares=shares )

            else:
                #add shares to current
                sharecount = db.execute("SELECT shares FROM portfolio WHERE (id = :id AND symbol = :symbol)", id=session["user_id"], symbol=symbol )

                sharenew = sharecount[0]['shares'] + int(shares)

                db.execute("UPDATE portfolio SET shares = :shares WHERE (id = :id AND symbol = :symbol)", shares=sharenew, id= session["user_id"], symbol=symbol)

            return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT symbol, shares, price, date FROM history WHERE id = :id ", id= session["user_id"] )

    return render_template("history.html", history = history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    else:
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("wrong Symbol input")

        quote = lookup(symbol)

        return render_template("quoted.html", name=quote["name"] , price=quote["price"], symbol=quote["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")

        if not username:
            return apology("Username was not correctly entered")

        password = request.form.get("password")
        if not password:
            return apology("Password was not correctly entered")

        confirmation = request.form.get("confirmation")
        if not confirmation:
            return apology("Confirmation Password was not correclty entered")

        if not confirmation == password:
            return apology("passwords did not match")

        hash1 = generate_password_hash(password)

        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=hash1)
        return redirect("/login")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        return render_template("sell.html")
    else:
        global symbol
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("wrong Symbol input")

        global shares
        shares = request.form.get("shares")
        shares = int(shares)

        if shares < 0:
            return apology("please enter a positive number")

        #check if share exists
        sharefind = db.execute("SELECT COUNT(*) FROM portfolio WHERE (id = :id AND symbol = :symbol)", id=session["user_id"], symbol=symbol)

        if sharefind[0]['COUNT(*)'] == 0:
            return apology("you dont seem to own that stock")

        global quote1
        quote1 = lookup(symbol)
        rows = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])


        global cash1
        cash1 = rows[0]["cash"]

        global total1
        total1 = shares * quote1["price"]
        return redirect("/sell2")

@app.route("/sell2", methods=["GET", "POST"])
@login_required
def sell2():
    """Sell shares of stock"""
    if request.method == "GET":
        return render_template("sell2.html", shares=shares, name=quote1["name"] , price=quote1["price"], symbol=quote1["symbol"], cash=cash1 )

    else:
        #check shares of user portfolio

        sharecheck = db.execute("SELECT * FROM portfolio WHERE (id = :id AND symbol = :symbol)", id=session["user_id"], symbol=symbol)
        sharecheck1 = sharecheck[0]['shares']

        if  shares > sharecheck1 :
            return apology("You dont have enough shares")

        sharesafter = sharecheck1 - shares
        cashafter = cash1 + total1

        #update

        if sharesafter == 0:
            db.execute("DELETE FROM portfolio WHERE (id = :id AND symbol = :symbol) ", id=session["user_id"] , symbol = symbol)
        else:
            db.execute("UPDATE portfolio SET shares = :sharesafter WHERE (id = :id AND symbol = :symbol)", sharesafter = sharesafter , id=session["user_id"] , symbol = symbol)

        db.execute("UPDATE users SET cash = :cashafter WHERE id= :id", cashafter = cashafter, id=session["user_id"])

        #transaction history

        db.execute("INSERT INTO history (id, symbol, shares, price, cashbefore, cashafter, date, action) VALUES (:id, :symbol, :shares, :price, :cashbefore, :cashafter, CURRENT_TIMESTAMP, :action)",
        id=session["user_id"], symbol=symbol, shares=-shares, price=quote1["price"], cashbefore=cash1, cashafter=cashafter, action = "sell")

        return redirect("/")

@app.route("/addmoney", methods=["GET", "POST"])
@login_required
def addmoney():
    if request.method == "GET":
        return render_template("addmoney.html")

    else:
        money = request.form.get("money")

        cashget = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])

        cash = int(cashget[0]['cash']) + int(money)

        db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash =cash , id = session["user_id"])

        #transaction history

        db.execute("INSERT INTO history (id, symbol, shares, price, cashbefore, cashafter, date, action) VALUES ( :id, :symbol, :shares, :price, :cashbefore, :cashafter, CURRENT_TIMESTAMP, :action)",
        id=session["user_id"], symbol="money", shares=0, price=int(money), cashbefore=cashget[0]['cash'], cashafter=cash, action = "addmoney")

        return render_template("EZmoney.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
