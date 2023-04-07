import os
from flask import Flask, request, abort, render_template, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from pyngrok import ngrok

app = Flask(__name__)
channel_secret = "6dcd8aa193caedfd897cbabc7b2c4839"
channel_access_token = "FHDjjDGUYRyCWLXCWPVIWnZv173JAo6ql6+g/8OTB/XGymQXC4QKn1NoK6BKICtRvB9LDPkLRwS4qdlVdU1C2Iic3iPzEq8LIOPixGXV/Q2tUECE9tQglnECNAEV3e1QDtzFfxhDT8vHRaDE5OJfswdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route('/')
def hello_world():
    return 'Welcome to The Kitchen page!'

@app.route('/line_callback', methods=['POST'])
def line_callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    # body = request.get_json()
    # msg = body['events'][0]['message']['text']
    print(body)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'Callback OK'

@app.route('/send_line_msg', methods=['GET'])
def send_line_msg():
    user_id = request.args.get('userId')
    msg = request.args.get('text')
    try:
        line_bot_api.push_message(user_id, TextSendMessage(text=msg))
    except LineBotApiError as e:
        print(e)
        return "Error. Message not sent."
    return 'Message sent!'

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    os.system("taskkill /f /im ngrok.exe")
    ngrok.set_auth_token("2NJY7I2xjwOeIgGVYs6YVMrQi3Q_7P73HE3tpsf1bALADxrae")
    public_url = ngrok.connect(5000)
    url = public_url.public_url.replace('http','https') + '/line_callback'
    print(url)
    line_bot_api.set_webhook_endpoint(url)
    app.run(debug = True, port = 5000)