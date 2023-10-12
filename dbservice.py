import psycopg2
from flask import request 
try:
    conn = psycopg2.connect(
        database="myduka_class", user='postgres', password='12345', host='127.0.0.1', port= '5432')
except:
    print('unable to connect to the database')

def get_data(my_data):
    cur = conn.cursor()
    t = "select * from "+my_data
    cur.execute(t)
    data = cur.fetchall()
    return data
prods=get_data('products')
sales=get_data('sales')

def add_product(values):
    cur = conn.cursor()
    insert_product="INSERT INTO products(name,buying_price,selling_price,stock_quantity) values(%s,%s,%s,%s)"
    cur.execute(insert_product,values)
    conn.commit()

def add_sale(values):
    cur=conn.cursor()
    insert_sale="INSERT INTO sales(pid,quantity,created_at) values(%s,%s,now())"
    cur.execute(insert_sale,values)
    conn.commit()

def create_user(values):
    cursor = conn.cursor()
    insert_query = "INSERT INTO users (full_name, email, password) values (%s, %s, %s)"
    cursor.execute(insert_query,values)
    conn.commit()

def check_email_exists(email):
    cursor = conn.cursor()
    query = "SELECT EXISTS(SELECT 1 FROM users WHERE email = %s)"
    cursor.execute(query, (email,))
    exists = cursor.fetchone()[0]
    return exists

def check_email_password_match(email, password):
    cursor = conn.cursor()
    query = "SELECT id FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    result = cursor.fetchone()
    if result is not None:
        id = result[0]
        return id
    else:
        return None

def calc_profit():
    cur=conn.cursor()
    find_profit="SELECT date(created_at) as days,sum((products.selling_price-products.buying_price)*sales.quantity) as profit from sales join products on products.id=sales.pid group by days order by days;"
    cur.execute(find_profit)
    profit_per_day=cur.fetchall()
    return profit_per_day