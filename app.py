from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample menu data
menu = [
    {"id": 1, "name": "Pizza", "price": 10.99},
    {"id": 2, "name": "Burger", "price": 7.99},
    {"id": 3, "name": "Pasta", "price": 8.99},
]

# Cart to store selected items
cart = []

@app.route('/')
def home():
    return render_template('home.html', menu=menu)

@app.route('/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    item = next((item for item in menu if item["id"] == item_id), None)
    if item:
        cart.append(item)
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    total = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@app.route('/checkout')
def checkout():
    cart.clear()
    return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True)