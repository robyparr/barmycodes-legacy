from flask import Flask, render_template, request

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
        barcode = Barcode("Code128", value, 200, 'mm').asImage('png')
        barcodes.append(barcode)

    # Render the template
    return render_template('index.html', barcodes=barcodes)


# Run the app
if __name__ == "__main__":
    app.run()
