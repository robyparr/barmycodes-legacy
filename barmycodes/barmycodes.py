from flask import Flask, render_template, request, Response, redirect
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO

from barmycodes.models.barcode import Barcode

# Setup Flask app
app = Flask(__name__)
app.config.from_object('barmycodes.config')
app.config.from_envvar('BARMYCODES_CONFIG', silent=True)


# Routes
@app.route("/", methods=['GET'])
def index():
    """Displays the app page with or without barcodes.
    If the querystring params 'b[]' are set, barcodes will
    be generated from the values.
    """

    # Values to generate barcodes from
    barcode_values = request.args.getlist('b[]')

    # List of generated barcodes
    barcodes = []

    # Create barcodes for each barcode value
    for value in barcode_values:
        if not value:
            break
        barcode = Barcode("Code128", value, width=200, unit='mm')
        barcodes.append(barcode)

    # Render the template
    data = {
        'barcodes': barcodes,
        'barcode_values': '\n'.join(barcode_values)
    }
    return render_template('index.html', data=data)

@app.route("/pdf", methods=['GET'])
def pdf():
    """Renders a PDF with barcodes generated from the
    querystring params 'b[].'
    """

    # Values to generate barcodes from
    barcode_values = request.args.getlist('b[]')

    # Determine PDF size params
    measurement = request.args.get('measurement')
    width = request.args.get('width')
    height = request.args.get('height')

    # Start PDF generation
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    # Generate barcodes and add to PDF
    for value in barcode_values:
        if not value:
            break

        # Generate the barcode
        barcode = Barcode(
            "Code128",
            value,
            width=(width if width else 200),
            height=(height if height else None),
            unit=(measurement if measurement in ('inch', 'mm') else 'mm')
        )

        # Add the barcode to the PDF
        barcode_buffer = BytesIO(barcode.as_string('png'))
        pdf.drawImage(ImageReader(barcode_buffer), 1, 1)
        barcode_buffer.close()

        pdf.setPageSize((barcode.width, barcode.height))
        pdf.showPage()

    pdf.save()

    response = Response(
        buffer.getvalue(),
        mimetype='application/pdf'
    )

    buffer.close()
    return response

# Run the app
if __name__ == "__main__":
    app.run()