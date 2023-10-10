import psycopg2
from flask import Flask,render_template
try:
    conn = psycopg2.connect(
        database="myduka_class", user='postgres', password='12345', host='127.0.0.1', port= '5432')
except:
    print('unable to connect to the database')

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


app.run(debug=True)


