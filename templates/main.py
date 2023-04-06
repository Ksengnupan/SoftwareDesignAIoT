from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
#from flask_cors import CORS, cross_origin
from datetime import datetime
from bson.objectid import ObjectId

import os
import sys
# import logging
from argparse import ArgumentParser

from flask_mqtt import Mqtt
from pyngrok import ngrok
import json

# logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

# mqtt - etp
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
mqtt = Mqtt(app)

# Connect to MongoDB
client = MongoClient("mongodb://group2_thekitchen-mongo_db-1:27017/")
# client = MongoClient("mongodb://localhost:27018/")
db = client["thekitchen"]

@app.route('/')
def menu_items():
    print("Main Menu Page")
    main_items = db.menu.find({"category":"MainDish"})
    dessert_items = db.menu.find({"category":"Desserts"})
    table = int(request.args.get('table'))
    return render_template('nang_menu.html', items1=main_items, items2=dessert_items, table=table)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    cart_items =request.get_json()
    timestamp = datetime.now()
    cart_items.update({"status": "processing"})
    cart_items.update({"timestamp": timestamp})
    print(cart_items)
    order_col = db.open_order # Collection
    order_col.insert_one(cart_items)
    return "OK"
    
@app.route('/order_display')
def order_display():
    if request.method == 'GET':
        now = datetime.now().strftime('%m/%d/%Y')
        data = db.open_order # Collection
        orders_db = data.find({"status":"processing"})
        #return "OK"
        orders = list(orders_db)
        now = datetime.now().strftime('%m/%d/%Y')
        #return jsonify(orders)
        return render_template('order_display.html', date=now, orders= orders)
    
@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    data = request.get_json()
    data_list = list(data)
    _id = data[0]
    table = data[1]
    filter = {'_id': ObjectId(_id)}
    print(filter)
    new_data = {'$set': {'status': 'finished'}}
    db.open_order.update_one(filter, new_data)

    # etp
    pub_msg = json.dumps({"status":"order_ready","table":table})
    mqtt.publish(os.environ['PUB_TOPIC'], pub_msg)

    return "Status updated successfully" 

# Define a route for the invoice page
@app.route('/invoice/<id>')
def invoice(id):
    # Retrieve the open table data from MongoDB
    open_table_data = db.open_order.find({"table": id})
    table_id = ''
    invoice_doc = dict()

    # Loop through the open_table_data and construct the invoice document
    for table in open_table_data:
        # Remove unnecessary fields from the table data
        del table['_id']
        del table['timestamp']
        
        # Get the table ID and remove it from the table data
        table_id = int(table['table'])
        del table['table']

        # Loop through the remaining fields in the table data and add them to the invoice document
        for key, value in table.items():
            if key not in invoice_doc:
                invoice_doc[key] = value
            elif "quantity" in invoice_doc[key]:
                # If the field already exists in the invoice document and it has a "quantity" field, add the quantities
                invoice_doc[key]["quantity"] += value["quantity"]
    
    # Calculate the total for each item in the invoice document
    for key, value in invoice_doc.items():
        if "quantity" in value:
            invoice_doc[key]["total"] = int(value["quantity"]) * int(value["price"])

    # Calculate the grand total for the entire invoice
    grand_total = 0
    for key, value in invoice_doc.items():
        if "total" in value:
            grand_total += value["total"]

    # Add the table ID and timestamp to the invoice document
    invoice_doc['table'] = table_id
    invoice_doc['timestamp'] = datetime.now()

    # Insert the invoice document into the order collection and remove the open table data
    if table_id!="":
        db.order.insert_one(invoice_doc)
        db.open_order.delete_many({"table":str(table_id)})
        del invoice_doc['_id']
    del invoice_doc['timestamp']
    del invoice_doc['table']
    del invoice_doc['status']

    # Render the invoice template with the invoice document and grand total
    return render_template('invoice.html', invoice=invoice_doc, table_id=table_id, date=datetime.now(), grand_total=grand_total)

# mqtt - etp
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe(os.environ['SUB_TOPIC'])

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    try:
        data = json.loads( message.payload.decode('ascii') )
        print(data)
        if data['status'] == "payment":
            tmp_order_col = db.open_order # Collection
            ans = tmp_order_col.find_one({"table": data['table']})
            print(ans)
            if ans is None:
                print("No order from table_no:", data['table'])
                pub_msg = json.dumps({"status":"payment","table":data['table'],"msg":"No Order"})
                mqtt.publish(os.environ['PUB_TOPIC'],pub_msg)
            else:
                print("go to payment page", data['table'])
                pub_msg = json.dumps({"status":"payment","table":data['table'],"msg":"OK"})
                mqtt.publish(os.environ['PUB_TOPIC'],pub_msg)
    except:
        print("Err:", message.payload.decode('ascii'))


if __name__ == "__main__":
    # app.run(debug=True)
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=5000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    # NGROK and flask
    ngrok.set_auth_token(os.environ['NGROK_TOKEN'])
    public_url = ngrok.connect(options.port)
    url = public_url.public_url.replace('http', 'https') + '/'
    app.logger.warning("Not OK")
    print("HHHH", flush=True)
    print(url)
    app.run(debug=True, port=options.port, host='0.0.0.0', use_reloader=False)