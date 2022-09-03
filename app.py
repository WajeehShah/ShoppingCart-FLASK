import os
from simplySQL import SQL
from flask_session import Session
from flask import Flask, render_template, redirect, request, session, jsonify
from datetime import datetime

DATABASE_URL = os.environ.get('DATABASE_URL', None)

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

app.config["SESSION_PERMANENT"] = False
Session(app)

db = SQL ('postgresql://postgres:root@localhost/wajeeh') 

@app.route("/")
def index():
    shirts = db.execute("SELECT * FROM shirts ORDER BY team ASC")
    shirtsLen = len(shirts)
    
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    if 'user' in session:
        shoppingCart = db.execute("SELECT * FROM cart WHERE uid=:uid", uid=str(session["uid"]))
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["subtotal"]
            totItems += shoppingCart[i]["qty"]
        shirts = db.execute("SELECT * FROM shirts ORDER BY team ASC")
        shirtsLen = len(shirts)
        return render_template ("index.html", shoppingCart=shoppingCart, shirts=shirts, shopLen=shopLen, shirtsLen=shirtsLen, total=total, totItems=totItems, display=display, session=session )
    return render_template ( "index.html", shirts=shirts, shoppingCart=shoppingCart, shirtsLen=shirtsLen, shopLen=shopLen, total=total, totItems=totItems, display=display)



@app.route("/buy/")
def buy():
    
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    qty = int(request.args.get('quantity'))
    if session:
    
        id = int(request.args.get('id'))
        goods = db.execute("SELECT * FROM shirts WHERE id = :id", id=id)
        if(goods[0]["onsale"] == 1):
            price = goods[0]["onsaleprice"]
        else:
            price = goods[0]["price"]
        team = goods[0]["team"]
        image = goods[0]["image"]
        subtotal = qty * price
    
        db.execute("INSERT INTO cart (id, qty, team, image, price, subtotal, uid) VALUES (:id, :qty, :team, :image, :price, :subtotal, :uid)", id=id, qty=qty, team=team, image=image, price=price, subtotal=subtotal, uid=str(session["uid"]))
        shoppingCart = db.execute("SELECT * FROM cart WHERE uid=:uid", uid=str(session["uid"]))
        shopLen = len(shoppingCart)
    
        for i in range(shopLen):
            total += shoppingCart[i]["subtotal"]
            totItems += shoppingCart[i]["qty"]
    
        shirts = db.execute("SELECT * FROM shirts ORDER BY team ASC")
        shirtsLen = len(shirts)
    
        return render_template ("index.html", shoppingCart=shoppingCart, shirts=shirts, shopLen=shopLen, shirtsLen=shirtsLen, total=total, totItems=totItems, display=display, session=session )


@app.route("/update/")
def update():
    
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    qty = int(request.args.get('quantity'))
    if session:
    
        id = int(request.args.get('id'))
        db.execute("DELETE FROM cart WHERE id = :id and uid = :uid", id=id, uid=str(session["uid"]))
        
        goods = db.execute("SELECT * FROM shirts WHERE id = :id", id=id)
        if(goods[0]["onsale"] == 1):
            price = goods[0]["onsaleprice"]
        else:
            price = goods[0]["price"]
        team = goods[0]["team"]
        image = goods[0]["image"]
        subtotal = qty * price
        
        db.execute("INSERT INTO cart (id, qty, team, image, price, subtotal, uid) VALUES (:id, :qty, :team, :image, :price, :subtotal, :uid)", id=id, qty=qty, team=team, image=image, price=price, subtotal=subtotal, uid=str(session["uid"]))
        shoppingCart = db.execute("SELECT * FROM cart WHERE uid=:uid", uid=str(session["uid"]))
        shopLen = len(shoppingCart)
        
        for i in range(shopLen):
            total += shoppingCart[i]["subtotal"]
            totItems += shoppingCart[i]["qty"]
    
        return render_template ("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session )




@app.route("/remove/", methods=["GET", "POST"])
def remove():
    
    out = int(request.args.get("id"))
    
    db.execute("DELETE from cart WHERE id=:id", id=out)
    
    totItems, total, display = 0, 0, 0
    
    shoppingCart = db.execute("SELECT * FROM cart WHERE uid=:uid", uid=str(session["uid"]))
    shopLen = len(shoppingCart)
    for i in range(shopLen):
        total += shoppingCart[i]["subtotal"]
        totItems += shoppingCart[i]["qty"]
    
    display = 1
    
    return render_template ("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session )


@app.route("/login/", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/new/", methods=["GET"])
def new():
    
    return render_template("new.html")


@app.route("/logged/", methods=["POST"] )
def logged():
    
    user = request.form["username"].lower()
    pwd = request.form["password"]
    if user == "" or pwd == "":
        return render_template ( "login.html" )
    
    query = "SELECT * FROM users WHERE username = :user AND password = :pwd"
    rows = db.execute ( query, user=user, pwd=pwd )


    if len(rows) == 1:
        session['user'] = user
        session['time'] = datetime.now( )
        session['uid'] = str(rows[0]["id"])

    if 'user' in session:
        return redirect ( "/" )

    return render_template ( "login.html", msg="Wrong username or password." )



@app.route("/register/", methods=["POST"] )
def registration():

    username = request.form["username"]
    password = request.form["password"]
    confirm = request.form["confirm"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    if password != confirm:
        return render_template("new.html", msg="Passwords did not match !!")

    rows = db.execute( "SELECT * FROM users WHERE username = :username ", username = username )

    if len( rows ) > 0:
        return render_template ( "new.html", msg="Username already exists!" )

    new = db.execute ( "INSERT INTO users (username, password, fname, lname, email) VALUES (:username, :password, :fname, :lname, :email)",
                    username=username, password=password, fname=fname, lname=lname, email=email )

    return render_template ( "login.html" )


@app.route("/cart/")
def cart():
    if 'user' in session:

        totItems, total, display = 0, 0, 0

        shoppingCart = db.execute("SELECT * FROM cart WHERE uid=:uid", uid=str(session["uid"]))

        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["subtotal"]
            totItems += shoppingCart[i]["qty"]

    return render_template("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session)


if __name__ == '__main__':
    app.run()
