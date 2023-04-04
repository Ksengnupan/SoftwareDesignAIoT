from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)

@app.route('/')
def show_orders(item):
    return render_template('orders.html')