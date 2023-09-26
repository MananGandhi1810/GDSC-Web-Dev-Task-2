import aspose.pdf as ap

def generate_invoice_pdf(invoice):
    document = ap.Document()
    page = document.pages.add()

    subtotal = ap.text.TextFragment('Invoice')
    subtotal.text_state.font_size = 25

    subtotal.horizontal_alignment = ap.HorizontalAlignment.CENTER
    subtotal.vertical_alignment = ap.VerticalAlignment.TOP

    page.paragraphs.add(subtotal)


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
        row.cells.add(str(item.id))
        row.cells.add(str(item.name))
        row.cells.add(str(item.stock))
        row.cells.add(str(item.price))
        row.cells.add(str(item.stock * item.price))

    page.paragraphs.add(table)

    padding = ap.text.TextFragment(' ')
    padding.text_state.font_size = 10
    page.paragraphs.add(padding)

    subtotal = ap.text.TextFragment(f'Subtotal: {invoice.subtotal}')
    subtotal.text_state.font_size = 10
    subtotal.horizontal_alignment = ap.HorizontalAlignment.RIGHT
    
    page.paragraphs.add(subtotal)

    tax_percent = ap.text.TextFragment(f'Tax %: {invoice.taxes_percent}%')
    tax_percent.text_state.font_size = 10
    tax_percent.horizontal_alignment = ap.HorizontalAlignment.RIGHT

    page.paragraphs.add(tax_percent)

    tax = ap.text.TextFragment(f'Tax: {invoice.tax}')
    tax.text_state.font_size = 10
    tax.horizontal_alignment = ap.HorizontalAlignment.RIGHT

    page.paragraphs.add(tax)

    discount_percent = ap.text.TextFragment(f'Discount %: {invoice.discount_percent}%')
    discount_percent.text_state.font_size = 10
    discount_percent.horizontal_alignment = ap.HorizontalAlignment.RIGHT

    page.paragraphs.add(discount_percent)

    discount = ap.text.TextFragment(f'Discount: {invoice.discount}')
    discount.text_state.font_size = 10
    discount.horizontal_alignment = ap.HorizontalAlignment.RIGHT

    page.paragraphs.add(discount)

    total = ap.text.TextFragment(f'Total: {invoice.total}')
    total.text_state.font_size = 10
    total.text_state.font_style = ap.text.FontStyles.BOLD
    total.horizontal_alignment = ap.HorizontalAlignment.RIGHT

    page.paragraphs.add(total)

    document.save(f'invoices\invoice{invoice.id}.pdf')