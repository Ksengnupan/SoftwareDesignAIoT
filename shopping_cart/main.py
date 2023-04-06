from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
#from flask_cors import CORS, cross_origin
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27018/")
db = client["thekitchen"]

@app.route('/')
def menu_items():
    main_items = db.menu.find({"category":"MainDish"})
    dessert_items = db.menu.find({"category":"Desserts"})
    table = 8
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
    filter = {'_id': ObjectId(data)}
    print(filter)
    new_data = {'$set': {'status': 'finished'}}
    db.open_order.update_one(filter, new_data)
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

if __name__ == '__main__':
    app.run(debug=True)