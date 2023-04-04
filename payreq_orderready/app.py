import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort, jsonify
from flask_mqtt import Mqtt
from pyngrok import ngrok

from pymongo import MongoClient
from datetime import datetime
import json

# database code
mongoClient = MongoClient(os.environ['MONGODB_URI'], 27017)
if os.environ["PHASE"] == "DEVELOPMENT":
    app_db = mongoClient.thekitchen_test # Database
if os.environ["PHASE"] == "PRODUCTION":
    app_db = mongoClient.thekitchen # Database


app = Flask(__name__, static_url_path='/ui', static_folder='web/')

# mqtt - etp
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
mqtt = Mqtt(app)

@app.route("/", methods=['GET'])
def hello_world():
    return "Hello, World!"

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
            tmp_order_col = app_db.open_table # Collection
            ans = tmp_order_col.find_one({"table_no": data['table_no']})
            print(ans)
            if ans is None:
                print("No order from table_no:", data['table_no'])
                pub_msg = json.dumps({"status":"payment","table_no":data['table_no'],"msg":"ERROR"})
                mqtt.publish(os.environ['PUB_TOPIC'],pub_msg)
            else:
                print("go to payment page", data['table_no'])
                pub_msg = json.dumps({"status":"payment","table_no":data['table_no'],"msg":"OK"})
                mqtt.publish(os.environ['PUB_TOPIC'],pub_msg)
    except:
        print("Err:", message.payload.decode('ascii'))

@app.route('/api/order_ready', methods=['GET'])
def publish_message():
    if os.environ["PHASE"] == "DEVELOPMENT":
        table_no = request.args.get('table_no')
        pub_msg = json.dumps({"status":"order_ready","table_no":table_no})
        mqtt.publish(os.environ['PUB_TOPIC'], pub_msg)
        return jsonify({"status": "order_ready"})
    return jsonify({"status": "ERROR"})

@app.route("/api/test_inject_tmp_order", methods=['POST'])
def test_inject_tmp_order():
    if os.environ["PHASE"] == "DEVELOPMENT":
        data = request.get_json()
        data['timestamp'] = datetime.now()
        tmp_order_col = app_db.open_table # Collection
        tmp_order_col.insert_one(data)
        return jsonify({"status": "OK"})
    return jsonify({"status": "ERROR"})

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

    app.run(debug=options.debug, port=options.port, host='0.0.0.0', use_reloader=False)