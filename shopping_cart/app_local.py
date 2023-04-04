import os
import sys
import itertools
from argparse import ArgumentParser

from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from jinja2 import Environment
from flask_mqtt import Mqtt
from pymongo import MongoClient
from datetime import datetime
import json
from pyngrok import ngrok

# database code
mongoClient = MongoClient(os.environ['MONGODB_URI'], 27017)
if os.environ["PHASE"] == "DEVELOPMENT":
    app_db = mongoClient.thekitchen # Database

env = Environment()
env.globals.update(enumerate=enumerate)

app = Flask(__name__)
app.secret_key = 'secret_key'

# initialize empty orders list
orders = []

# shopping_cart route
@app.route('/add_to_cart', methods=['GET', 'POST'])
def shopping_cart():
    if 'cart' not in session:
        session['cart'] = {}

    if 'orders' not in session:
        session['orders'] = []

    if request.method == 'POST':
        item = request.form['item_name']
        quantity = int(request.form['quantity'])
        unit_price = int(request.form['unit_price'])
        if item in session['cart']:
            session['cart'][item]['quantity'] += quantity
        else:
            session['cart'][item] = {'quantity': quantity, 'unit_price': unit_price}
        flash(f"{quantity} x {item} added to cart.")
        # set table number in session
        session['table_no'] = request.form['tableNo']
        return redirect(url_for('shopping_cart'))

    items = [{'item': item, 'quantity': session['cart'][item]['quantity'], 'unit_price': session['cart'][item]['unit_price']} for item in session['cart']]
    orders = session['orders'] # Define orders as a list
    return render_template('shopping_cart.html', items=items, session=session)




@app.route("/api/inject_order", methods=['POST'])
def inject_order():
    if os.environ["PHASE"] == "DEVELOPMENT":
        data = request.get_json()
        data['timestamp'] = datetime.now()
        order_col = app_db.order # Collection
        order_col.insert_one(data)
        return jsonify({"status": "OK"})
    return jsonify({"status": "ERROR"})

@app.route('/update/<item>', methods=['POST'])
def update_item(item):
    quantity = int(request.form['quantity'])
    session['cart'][item] = quantity
    flash(f"{item} quantity updated to {quantity}.")
    return redirect(url_for('shopping_cart'))


@app.route('/delete/<item>', methods=['POST'])
def delete_item(item):
    session['cart'].pop(item, None)
    flash(f"{item} deleted from cart.")
    return redirect(url_for('shopping_cart'))

# order route
@app.route('/order', methods=['GET', 'POST'])
def order_cart():
    if request.method == 'POST':
        ordered_items = sorted(session['cart'].items())
        session['cart'] = {}

        # Generate a timestamp for the order
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Save the order and timestamp to the orders list
        orders = session['orders'] # Get the current orders list
        orders.append((ordered_items, timestamp, session['table_no'])) # Append the new order to the list with table number
        session['orders'] = orders # Store the updated orders list in the session

        # Add the order to the MongoDB database
        if os.environ["PHASE"] == "DEVELOPMENT":
            data = {
                'items': ordered_items,
                'timestamp': timestamp,
                'table_no': session['table_no']
            }
            order_col = app_db.order # Collection
            order_col.insert_one(data)

        return redirect(url_for('orders'))

    return redirect(url_for('shopping_cart'))



# orders route
@app.route('/orders')
def orders():
    orders = session['orders'] # Define orders as a list
    return render_template('order_display.html', orders=orders)
 
@app.route('/order_display')
def order_display():
    return render_template('order_display.html')
 
@app.route('/clear_order/<int:index>', methods=['POST'])
def clear_order(index):
    session['orders'].pop(index)
    flash('Order cleared.')
    return redirect(url_for('orders'))


if __name__ == '__main__':
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    ngrok.set_auth_token(os.environ['NGROK_TOKEN'])
    public_url = ngrok.connect(options.port)
    url = public_url.public_url.replace('http', 'https') + '/callback'
    print(' * Tunnel URL:', url)

    app.run(debug=options.debug, port=options.port)
