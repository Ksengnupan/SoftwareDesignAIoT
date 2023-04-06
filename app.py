import os
import sys
from argparse import ArgumentParser

from pymongo import MongoClient
from flask_cors import CORS, cross_origin

from flask import Flask, request, abort, jsonify,render_template
from flask_mqtt import Mqtt
from pyngrok import ngrok

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from datetime import datetime
import json
from bson.objectid import ObjectId

app = Flask(__name__)

# mqtt - etp
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
mqtt = Mqtt(app)

# database code
mongoClient = MongoClient(os.environ['MONGODB_URI'], 27017)
if os.environ["PHASE"] == "DEVELOPMENT":
    app_db = mongoClient.thekitchen_test # Database
if os.environ["PHASE"] == "PRODUCTION":
    app_db = mongoClient.thekitchen # Database


CORS(app, support_credentials=True)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

#KEVIN Part
# Define a route for the invoice page
@app.route('/invoice/<id>')
def invoice(id):
    # Retrieve the open table data from MongoDB
    open_table_data = app_db.open_order.find({"table": id})
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
        app_db.order.insert_one(invoice_doc)
        app_db.open_order.delete_many({"table":str(table_id)})
        del invoice_doc['_id']
    del invoice_doc['timestamp']
    del invoice_doc['table']
    del invoice_doc['status']

    # Render the invoice template with the invoice document and grand total
    return render_template('invoice.html', invoice=invoice_doc, table_id=table_id, date=datetime.now(), grand_total=grand_total)

#Pan's Part
@app.route("/api/order_list", methods=['POST'])
def order_list():
    if os.environ["PHASE"] == "DEVELOPMENT":
        data = request.get_json()
        date=datetime.now()
        date_only = date.strftime('%Y-%m-%d')
        #date_only=date.toString("yyyy-MM-dd")
        data['timestamp'] = date_only
        order_col = app_db.order # Collection
        order_col.insert_one(data)
        return jsonify({"status": "OK"})
    return jsonify({"status": "ERROR"})

@app.route("/api/menu", methods=['POST'])
def menu():
    if os.environ["PHASE"] == "DEVELOPMENT":
        data = request.get_json()
        #data['timestamp'] = datetime.now()
        menu_col = app_db.menu # Collection
        menu_col.insert_one(data)
        return jsonify({"status": "OK"})
    return jsonify({"status": "ERROR"})


@app.route("/check_menu", methods=['GET'])
def check_menu():
    menu_id = request.args.get('menu_id')
    menu_collection = app_db.menu # Collection
    cursor = menu_collection.find({"menu_id": int(menu_id)})
    menu_info = []
    for document in cursor:
        print(document)

        menu_info.append(document["name"])
        menu_info.append(document["price"])
        #menu_info.append(document["img_url"])
    return jsonify(menu_info)
        
    #return jsonify({"status": "OK", "Menu_information": menu_info})
        

@app.route('/')
def menu_items():
    print("Main Menu Page")
    main_items = app_db.menu.find({"category":"MainDish"})
    dessert_items = app_db.menu.find({"category":"Desserts"})
    table = int(request.args.get('table'))
    return render_template('nang_menu.html', items1=main_items, items2=dessert_items, table=table)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    cart_items =request.get_json()
    timestamp = datetime.now()
    cart_items.update({"status": "processing"})
    cart_items.update({"timestamp": timestamp})
    print(cart_items)
    order_col = app_db.open_order # Collection
    order_col.insert_one(cart_items)
    return "OK"
    
@app.route('/order_display')
def order_display():
    if request.method == 'GET':
        now = datetime.now().strftime('%m/%d/%Y')
        data = app_db.open_order # Collection
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
    app_db.open_order.update_one(filter, new_data)

    # etp
    pub_msg = json.dumps({"status":"order_ready","table":table})
    mqtt.publish(os.environ['PUB_TOPIC'], pub_msg)

    return "Status updated successfully" 

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    print(body)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


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
            tmp_order_col = app_db.open_order # Collection
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