# GDSC Web Dev Task (Backend Development)

This GitHub repository is my (Manan Gandhi's) submission for the GDSC Web Dev Task 2.
The goal of the task was to develop an Inventory Management System. I have accomplished this task using the Flask framework in Python.

## Technologies Used
- Python
- Flask
- Flask-PyMongo
- MongoDB (Instance hosted on MongoDB Atlas)
- aspose-pdf (for generating PDF files)
- Postman (for testing the API)
- MongoDB Compass (for viewing the database)

## Item class and routes
### Attributes
- id: Unique identifier for the item
- name: Name of the item
- stock: Number of items in stock
- price: Price of the item

### Routes
- GET /get_all_items: Returns a list of all items in the inventory
    - Parameters - None
![Get All Items](https://github.com/MananGandhi1810/GDSC-Web-Dev-Task-2/blob/main/assets/get_all_items.png)

- GET /get_item?id={item_id}: Returns the item with the given id
    - Parameters - id (int)
![Get Item 1](https://github.com/MananGandhi1810/GDSC-Web-Dev-Task-2/blob/main/assets/get_item.png)

- POST /add_item: Adds a new item to the inventory
    - Parameters - name (str), stock (int), price (float)
![Add Item](https://github.com/MananGandhi1810/GDSC-Web-Dev-Task-2/blob/main/assets/add_item.png)

- PUT /update_item: Updates the item with the given id
    - Parameters - id (int), name (str), stock (int), price (float) (at least one of these parameters must be provided)
![Update Item](https://github.com/MananGandhi1810/GDSC-Web-Dev-Task-2/blob/main/assets/update_item.png)

- DELETE /delete_item?id={item_id}: Deletes the item with the given id
    - Parameters - id (int)
![Delete Item](https://github.com/MananGandhi1810/GDSC-Web-Dev-Task-2/blob/main/assets/delete_item.png)

## Invoice class and routes
### Attributes
- id: Unique identifier for the invoice
- items: List of items in the invoice
- subtotal: Total price of the invoice before discount and tax
- taxes_percent: Percentage of taxes to be applied to the invoice
- tax: Total amount of taxes to be applied to the invoice
- discount_percent: Percentage of discount to be applied to the invoice
- discount: Total amount of discount to be applied to the invoice
- total: Total price of the invoice after discount and tax

## Methods
- generate_pdf: Generates a PDF file of the invoice and saves it in the `invoices` folder, runs every time an invoice is created or updated (example: [invoice1.pdf](https://github.com/MananGandhi1810/GDSC-Web-Dev-Task-2/blob/main/invoices/invoice1.pdf))

### Routes
- GET /get_all_invoices: Returns a list of all invoices
    - Parameters - None
    ![Get All Invoices](https://github.com/MananGandhi1810/GDSC-Web-Dev-Task-2/blob/main/assets/get_all_invoices.png)

- GET /get_invoice?id={invoice_id}: Returns the invoice with the given id
    - Parameters - id (int)
    ![Get Invoice](https://github.com/MananGandhi1810/GDSC-Web-Dev-Task-2/blob/main/assets/get_invoice.png)

- GET /get_invoice_pdf?id={invoice_id}: Returns the invoice with the given id in PDF format (example: [invoice1.pdf](https://github.com/MananGandhi1810/GDSC-Web-Dev-Task-2/blob/main/invoices/invoice1.pdf))
    - Parameters - id (int)
    ![Get Invoice PDF](https://github.com/MananGandhi1810/GDSC-Web-Dev-Task-2/blob/main/assets/get_invoice_pdf.png)

- POST /new_invoice: Adds a new invoice
    - Parameters - items (list of dicts), taxes_percent (float), discount_percent (float)
    ![New Invoice](https://github.com/MananGandhi1810/GDSC-Web-Dev-Task-2/blob/main/assets/new_invoice.png)

- PUT /update_invoice: Updates the invoice with the given id
    - Parameters - id (int), items (list of dicts), taxes_percent (float), discount_percent (float) (at least one of these parameters must be provided)
    ![Update Invoice](https://github.com/MananGandhi1810/GDSC-Web-Dev-Task-2/blob/main/assets/update_invoice.png)

- DELETE /delete_invoice?id={invoice_id}: Deletes the invoice with the given id
    - Parameters - id (int)
    ![Delete Invoice](https://github.com/MananGandhi1810/GDSC-Web-Dev-Task-2/blob/main/assets/delete_invoice.png)