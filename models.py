from generate_pdf import generate_invoice_pdf

class Item:
    def __init__(self, id:int, name:str, stock:int, price:int):
        self.id = id
        self.name = name
        self.stock = stock
        self.price = price

    def __str__(self):
        return f'{self.id}:{self.name}x{self.stock}@{self.price}'

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'stock': self.stock, 'price': self.price}

class Invoice:
    def __init__(self, id:int, items:list, subtotal:int, taxes_percent:int, discount_percent:int):
        self.id = id
        self.items = items
        self.subtotal = subtotal
        self.taxes_percent = taxes_percent
        self.discount_percent = discount_percent
        self.discount = subtotal * discount_percent / 100
        self.tax = (subtotal-self.discount) * taxes_percent / 100
        self.total = subtotal + self.tax - self.discount

    def generate_pdf_from_invoice(self):
        generate_invoice_pdf(self)


    def to_dict(self):
        return {'id': self.id, 'items': [item.to_dict() for item in self.items], 'subtotal': self.subtotal, 'taxes_percent': self.taxes_percent, 'discount_percent': self.discount_percent, 'discount': self.discount, 'tax': self.tax, 'total': self.total}

