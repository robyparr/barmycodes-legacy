from flask import Flask, render_template, request, Response, redirect
from scout_apm.flask import ScoutApm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO

from .models.barcode import Barcode
from .config import Config

# Setup Flask app
app = Flask(__name__)
app.config.from_object(Config)
ScoutApm(app)


def _get_barcodes(args, ignore_dimensions=True):
    """Generate barcodes from the request arguments.
    Utility method for the routes.
    """

    # Values to generate barcodes from
    barcode_values = args.getlist('b[]')
    barcode_type = args.get('type', 'Code128')

    if not barcode_type in ('Code128', 'QR'):
        barcode_type = 'Code128'

    # Determine PDF size params
    measurement = args.get('measurement')
    width = args.get('width')
    height = args.get('height')

    # Generate barcodes
    barcodes = []
    for value in barcode_values:
        if not value:
            continue

        # Generate the barcode
        barcode = Barcode(
            barcode_type,
            value,
            width=(width if width and not ignore_dimensions else None),
            height=(height if height and not ignore_dimensions else None),
            unit=(measurement if measurement in ('inch', 'mm') and not ignore_dimensions else 'mm')
        )

        barcodes.append(barcode)

    return barcodes

# Routes
@app.route("/", methods=['GET'])
def index():
    """Displays the app page with or without barcodes.
    If the querystring params 'b[]' are set, barcodes will
    be generated from the values.
    """

    barcodes = _get_barcodes(request.args)

    # Render the template
    data = {
        'barcodes': barcodes,
        'barcode_values': '\n'.join([b.text_value for b in barcodes])
    }
    return render_template('index.html', data=data)


@app.route("/png", methods=['GET'])
def png():
    """Generate a PNG image for a single barcode."""

    # Get a single barcode's information
    barcode_value = request.args.get('b[]')
    barcode_type = request.args.get('type', 'Code128')

    if not barcode_type in ['Code128', 'QR']:
        barcode_type = 'Code128'

    # Make sure we have a value
    if not barcode_value:
        return redirect('/')

    # Generate the barcode
    barcode = Barcode(barcode_type, barcode_value)

    # Create the response
    response = Response(
        barcode.as_string('png'),
        mimetype='image/png'
    )

    response.headers['Content-Disposition'] = 'attachment; filename=barmycodes.png'

    return response


@app.route("/pdf", methods=['GET'])
def pdf():
    """Renders a PDF with barcodes generated from the
    querystring params 'b[].'
    """

    barcodes = _get_barcodes(request.args, ignore_dimensions=False)

    # Start PDF generation
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setTitle('barmycodes.pdf')

    # Generate barcodes and add to PDF
    for barcode in barcodes:
        # Add the barcode to the PDF
        barcode_buffer = BytesIO(barcode.as_string('png'))
        pdf.drawImage(ImageReader(barcode_buffer), 1, 1)
        barcode_buffer.close()

        pdf.setPageSize((barcode.width, barcode.height))
        pdf.showPage()

    pdf.save()

    response = Response(
        buffer.getvalue(),
        mimetype='application/pdf',
    )

    response.headers['Content-Disposition'] = 'inline; filename=barmycodes.pdf'

    buffer.close()
    return response

@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.html', data='')

# Run the app
if __name__ == "__main__":
    app.run()
