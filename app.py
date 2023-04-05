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

# database code
mongoClient = MongoClient(os.environ['MONGODB_URI'], 27017)
if os.environ["PHASE"] == "DEVELOPMENT":
    app_db = mongoClient.thekitchen_test # Database
if os.environ["PHASE"] == "PRODUCTION":
    app_db = mongoClient.thekitchen # Database


app = Flask(__name__, static_url_path='/ui', static_folder='web/')

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

@app.route("/", methods=['GET'])
def hello_world():
    return "Hello, World!"

#KEVIN Part
# Define a route for the invoice page
@app.route('/invoice/<id>')
def invoice(id):
    # Retrieve the invoice data from MongoDB
    invoice = app_db.invoice.find_one({"_id": int(id)})
    # Render the HTML template with the invoice data
    return render_template('invoice.html', invoice=invoice)




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
        menu_info.append(document["price"])
        menu_info.append(document["name"])
        menu_info.append(document["category"])
    return jsonify({"status": "OK", "Menu_information": menu_info})
        

@app.route("/date", methods=['GET'])
def date():
    timestamp = request.args.get('timestamp')
    order_collection = app_db.order # Collection
    cursor = order_collection.find({"timestamp": timestamp})
    print(cursor)
    return jsonify({"status": "OK"})

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

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text + ', me too')
    )



if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    # NGROK and flask
    ngrok.set_auth_token(os.environ['NGROK_TOKEN'])
    public_url = ngrok.connect(options.port)
    url = public_url.public_url.replace('http', 'https') + '/callback'
    print(url)
    line_bot_api.set_webhook_endpoint(url)
    app.run(debug=options.debug, port=options.port, host='0.0.0.0', use_reloader=False)