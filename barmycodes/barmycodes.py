from flask import Flask, render_template

from barmycodes.lib.barcode import Barcode

# Setup Flask app
app = Flask(__name__)
app.config.from_object('barmycodes.config')
app.config.from_envvar('BARMYCODES_CONFIG', silent=True)

# Routes
@app.route("/")
@app.route("/<value>")
def index(value=None):
	barcode = None
	if value:
		barcode = Barcode("Code128", value, 200, 'mm').asImage('png')

	return render_template('index.html', barcode=barcode)


if __name__ == "__main__":
	app.run()