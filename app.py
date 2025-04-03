from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database connection
DATABASE_PATH = r"C:\Users\robertsc2\Desktop\Basic Flask\database\menu_database"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Fetch menu items from all tables
def fetch_menu_items():
    conn = get_db_connection()
    cursor = conn.cursor()
    categories = ["FishOptions", "FriedSeafood", "FriedSides", "FriedExtras", "ChineseTakeaway", "Drinks", "Burgers"]
    menu = {}
    for category in categories:
        cursor.execute(f"SELECT ID, ItemName, Price, GF, VG, VEG FROM {category}")
        menu[category] = cursor.fetchall()
    conn.close()
    return menu

@app.route('/')
def home():
    cart = session.get("cart", [])
    return render_template('index.html', cart=cart)

@app.route('/menu')
def menu():
    menu_items = fetch_menu_items()
    cart = session.get("cart", [])
    return render_template('menu.html', menu=menu_items, cart=cart)

@app.route('/add_to_cart', methods=["POST"])
def add_to_cart():
    item = {
        "id": request.form["id"],
        "name": request.form["name"],
        "price": float(request.form["price"])
    }
    if "cart" not in session:
        session["cart"] = []
    session["cart"].append(item)
    return redirect(url_for('menu'))

@app.route('/clear_cart')
def clear_cart():
    session.pop("cart", None)
    return redirect(url_for('menu'))

if __name__ == '__main__':
    app.run(debug=True)