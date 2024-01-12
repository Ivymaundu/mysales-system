import psycopg2
from flask import Flask,render_template,request,redirect,session,flash
from dbservice import get_data,add_product,create_user,check_email_password_match,add_sale,calc_profit
try:
    conn = psycopg2.connect(
        database="myduka_class", user='postgres', password='12345', host='127.0.0.1', port= '5432')
except:
    print('unable to connect to the database')

app=Flask(__name__)

app.secret_key = "sales%.system"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/shop")
def shop():
     return render_template("myshop.html")

@app.route("/cart")
def cart():
     return render_template("shoppingcart.html")
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/products")
def products():
    myprods = get_data("products")   
    return render_template("products.html", myprods = myprods)

@app.route("/add-products", methods=["Post"])
def addproduct():
        name           =  request.form["name"]
        buying_price   =  request.form["buying_price"]
        selling_price  =  request.form["selling_price"]
        stock_quantity =  request.form["stock_quantity"]
        values = (name,buying_price,selling_price,stock_quantity)

        add_product(values)

        return redirect("/products")

@app.route("/sales")
def sales():
    products= get_data("products")  
    sales= get_data("sales") 

    return render_template("sales.html", myprods = products, mysales=sales)

@app.route("/add-sales", methods=["Post"])
def addsale():
        pid = request.form["pid"]
        quantity= request.form["quantity"]
        values = (pid,quantity)

        add_sale(values)

        return redirect("/sales")

@app.route("/register", methods= ["POST"])
def create_account():
    if request.method=="POST":
        name=request.form["full_name"]
        email=request.form["email"]
        password=request.form["password"]
        values=(name,email,password)
        create_user(values)
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["POST","GET"])
def access_account():
        email = request.form["email"]
        password = request.form["password"]
       
        check_email_password_match(email,password)
        return  render_template("/dashboard.html")

@app.route("/profit")
def profit():
    dates=[]
    profits=[]
    for i in calc_profit():
        dates.append(str(i[0]))
        profits.append(float(i[1]))
    return render_template("profit.html",dates=dates,profits=profits)

@app.route("/logout")
def logout():
    session.pop('email', None)
    flash('logout successfully')
    return render_template('login.html')


app.run(debug=True)