
from flask import Flask, render_template, request, redirect, session, jsonify
from flask_pymongo import PyMongo
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)

# HOME
@app.route('/')
def home():

    products = mongo.db.products.find()

    return render_template(
        'index.html',
        products=products
    )

# PRODUCTS
@app.route('/products')
def products():

    products = mongo.db.products.find()

    comidas = []
    bebidas = []
    snacks = []

    for product in products:

        if product['category'] == 'Comidas':
            comidas.append(product)

        elif product['category'] == 'Bebidas':
            bebidas.append(product)

        elif product['category'] == 'Snacks':
            snacks.append(product)

    return render_template(
        'products.html',
        comidas=comidas,
        bebidas=bebidas,
        snacks=snacks
    )

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        identification = request.form['identification']

        existing_user = mongo.db.users.find_one({
            'identification': identification
        })

        if existing_user:
            return "Usuario ya existe"

        mongo.db.users.insert_one({
            'name': name,
            'identification': identification
        })

        session['user'] = name
        session['identification'] = identification

        return redirect('/cart')

    return render_template('register.html')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        name = request.form['name']
        identification = request.form['identification']

        user = mongo.db.users.find_one({
            'name': name,
            'identification': identification
        })

        if user:

            session['user'] = user['name']
            session['identification'] = user['identification']

            return redirect('/cart')

        return "Usuario no encontrado"

    return render_template('login.html')

# LOGOUT
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')

# CART
@app.route('/cart')
def cart():

    return render_template('cart.html')

# SAVE ORDER
@app.route('/submit-order', methods=['POST'])
def submit_order():

    if 'user' not in session:
        return redirect('/login')

    data = request.json

    mongo.db.orders.insert_one({

        'name': session['user'],
        'identification': session['identification'],
        'products': data['products'],
        'total': data['total']
    })

    return jsonify({
        'message': 'Pedido enviado'
    })

if __name__ == '__main__':
    app.run(debug=True)

