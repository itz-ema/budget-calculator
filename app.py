from flask import Flask, render_template, url_for, g
import sqlite3
DATABASE = "database.db"
app = Flask(__name__)
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html" )

@app.route("/categories")
def categories():
    sql = "SELECT * FROM category"
    reslut = query_db(sql)
    return reslut


@app.route("/calculator")
def calculator():
    sql = "SELECT name, SUM (amount_spent) AS 'TOTAL_AMOUNT_SPENT' FROM expenses GROUP BY 'name' ORDER BY 'TOTAL_AMOUNT_SPENT' DESC" 
    answer = query_db(sql)
    return answer

if __name__ == "__main__":
    app.run(debug= True)
