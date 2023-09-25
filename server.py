from flask import Flask, request, jsonify, send_file
from flask_pymongo import PyMongo
from models import Item, Invoice
import os

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://manan:manan123@inventory-db.da37xt6.mongodb.net/inventory'

mongo = PyMongo(app)
items_db = mongo.db.items
invoices_db = mongo.db.invoices

@app.route('/get_all_items', methods=['GET'])
def get_all_items():
    items = list(items_db.find())
    for item in items:
        item.pop('_id')
    return jsonify(items)

@app.route('/get_item', methods=['GET'])
def get_item():
    item_id = int(request.args.get('id'))
    if not item_id:
        return jsonify({'message': 'No item id provided!'})
    item = items_db.find_one({'id': item_id})
    if not item:
        return jsonify({'message': 'No item found!'})
    item.pop('_id')
    return jsonify(item)

@app.route('/add_item', methods=['POST'])
def add_item():
    item_id = items_db.find_one(sort=[('id', -1)])['id'] + 1 if items_db.count_documents({}) > 0 else 1
    name = request.json.get('name')
    stock = request.json.get('stock')
    price = request.json.get('price')
    if not name or not stock or not price:
        return jsonify({'message': 'Missing parameters!'})
    item = Item(item_id, name, stock, price)
    items_db.insert_one(item.to_dict())
    return jsonify({'message': 'Item added successfully!', 'item_id': item_id})

@app.route('/update_item', methods=['PUT'])
def update_item():
    item_id = request.json.get('id')
    name = request.json.get('name')
    stock = request.json.get('stock')
    price = request.json.get('price')
    if not item_id:
        return jsonify({'message': 'No item id provided!'})
    item = items_db.find_one({'id': item_id})
    if not item:
        return jsonify({'message': 'No item found!'})
    if not name and not stock and not price:
        return jsonify({'message': 'No parameters provided!'})
    if name:
        item['name'] = name
    if stock:
        item['stock'] = stock
    if price:
        item['price'] = price
    items_db.update_one({'id': item_id}, {'$set': item})        
    return jsonify({'message': 'Item updated successfully!'})

@app.route('/delete_item', methods=['DELETE'])
def delete_item():
    item_id = request.args.get('id')
    if not item_id:
        return jsonify({'message': 'No item id provided!'})
    item = items_db.find_one({'id': item_id})
    if not item:
        return jsonify({'message': 'No item found!'})
    items_db.delete_one({'id': item_id})
    return jsonify({'message': 'Item deleted successfully!'})


@app.route('/get_all_invoices', methods=['GET'])
def get_all_invoices():
    invoices = list(invoices_db.find())
    for invoice in invoices:
        invoice.pop('_id')
    return jsonify(invoices)

@app.route('/get_invoice', methods=['GET'])
def get_invoice():
    invoice_id = int(request.args.get('id'))
    if not invoice_id:
        return jsonify({'message': 'No invoice id provided!'})
    invoice = invoices_db.find_one({'id': invoice_id})
    if not invoice:
        return jsonify({'message': 'No invoice found!'})
    invoice.pop('_id')
    return jsonify(invoice)


@app.route('/new_invoice', methods=['POST'])
def new_invoice():
    invoice_id = invoices_db.find_one(sort=[('id', -1)])['id'] + 1 if invoices_db.count_documents({}) > 0 else 1
    #items -> list of dicts, each dict has id, stock
    items = request.json.get('items')
    if not items:
        return jsonify({'message': 'No items provided!'})
    items_list = []
    for item in items:
        items_db_item = items_db.find_one({'id': item['id']})
        if not items_db_item:
            return jsonify({'message': f'Item for Item ID {item["id"]} not found!'})
        if items_db_item['stock'] < item['stock']:
            return jsonify({'message': f'Not enough stock for Item ID {item["id"]}!'})
        items_list.append(Item(items_db_item['id'], items_db_item['name'], item['stock'], items_db_item['price']))
    subtotal = sum([item.stock * item.price for item in items_list])
    taxes_percent = request.json.get('taxes_percent')
    discount_percent = request.json.get('discount_percent')
    if not taxes_percent:
        taxes_percent = 0
    if not discount_percent:
        discount_percent = 0
    invoice = Invoice(invoice_id, items_list, subtotal, taxes_percent, discount_percent)
    invoices_db.insert_one(invoice.to_dict())
    for item in invoice.items:
        items_db_item = items_db.find_one({'id': item.id})
        items_db_item['stock'] -= item.stock
        items_db.update_one({'id': item.id}, {'$set': items_db_item})
    invoice.generate_pdf_from_invoice()
    return jsonify({'message': 'Invoice generated successfully!', 'invoice_id': invoice_id})
        

@app.route('/delete_invoice', methods=['DELETE'])
def delete_invoice():
    invoice_id = request.args.get('id')
    if not invoice_id:
        return jsonify({'message': 'No invoice id provided!'})
    invoice = invoices_db.find_one({'id': invoice_id})
    if not invoice:
        return jsonify({'message': 'No invoice found!'})
    invoices_db.delete_one({'id': invoice_id})
    os.remove(f'invoice{invoice_id}.pdf')
    return jsonify({'message': 'Invoice deleted successfully!'})

@app.route('/update_invoice', methods=['PUT'])
def update_invoice():
    invoice_id = request.json.get('id')
    if not invoice_id:
        return jsonify({'message': 'No invoice id provided!'})
    invoice = invoices_db.find_one({'id': invoice_id})
    if not invoice:
        return jsonify({'message': 'No invoice found!'})
    items = request.json.get('items')
    discount_percent = request.json.get('discount_percent')
    taxes_percent = request.json.get('taxes_percent')
    if not items and not discount_percent and not taxes_percent:
        return jsonify({'message': 'No parameters provided!'})
    if items:
        items_list = []
        for item in items:
            items_db_item = items_db.find_one({'id': item['id']})
            prev_stock = 0
            for prev_item in invoice['items']:
                if prev_item['id'] == item['id']:
                    prev_stock = prev_item['stock']
                    break
            if not items_db_item:
                return jsonify({'message': f'Item for Item ID {item["id"]} not found!'})
            if items_db_item['stock'] < item['stock']:
                return jsonify({'message': f'Not enough stock for Item ID {item["id"]}!'})
            items_list.append(Item(items_db_item['id'], items_db_item['name'], item['stock'], items_db_item['price']))
            items_db_item['stock'] -= item['stock'] - prev_stock
        subtotal = sum([item.stock * item.price for item in items_list])
        invoice['items'] = items_list
    if discount_percent:
        invoice['discount_percent'] = discount_percent
    if taxes_percent:
        invoice['taxes_percent'] = taxes_percent
    invoice = Invoice(invoice_id, invoice['items'], subtotal, invoice['taxes_percent'], invoice['discount_percent'])
    invoices_db.update_one({'id': invoice_id}, {'$set': invoice.to_dict()})

@app.route('/get_invoice_pdf', methods=['GET'])
def get_invoice_pdf():
    invoice_id = request.args.get('id')
    if not invoice_id:
        return jsonify({'message': 'No invoice id provided!'})
    invoice = invoices_db.find_one({'id': invoice_id})
    if not invoice:
        return jsonify({'message': 'No invoice found!'})
    return send_file(f'invoice{invoice_id}.pdf', as_attachment=True)

app.run(debug=True)