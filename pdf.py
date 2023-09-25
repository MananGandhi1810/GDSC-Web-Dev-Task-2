import aspose.pdf as ap

def generate_invoice_pdf(invoice):
    document = ap.Document()
    page = document.pages.add()

    text = ap.text.TextFragment('Invoice')
    text.text_state.font_size = 25

    text.horizontal_alignment = ap.HorizontalAlignment.CENTER
    text.vertical_alignment = ap.VerticalAlignment.TOP

    page.paragraphs.add(text)


    table = ap.Table()
    table.column_widths = '75 75 75 75 75'
    table.default_cell_border = ap.BorderInfo(ap.BorderSide.ALL, 0.1)
    table.default_cell_padding = ap.MarginInfo(5, 5, 5, 5)
    table.horizontal_alignment = ap.HorizontalAlignment.CENTER

    row = table.rows.add()
    row.cells.add('ID')
    row.cells.add('Name')
    row.cells.add('Stock')
    row.cells.add('Price')
    row.cells.add('Total')

    for item in invoice.items:
        row = table.rows.add()
        row.cells.add(item.id)
        row.cells.add(item.name)
        row.cells.add(item.stock)
        row.cells.add(item.price)
        row.cells.add(item.stock * item.price)

    page.paragraphs.add(table)

    print('Saving invoice.pdf')
    document.save('invoice.pdf')