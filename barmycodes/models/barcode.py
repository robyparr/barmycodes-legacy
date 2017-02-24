from reportlab.lib import units
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing
import base64

class Barcode:

	def __init__(self, type, text_value, width, unit = None):
		""" Initialize the barcode. This creates the actual
		barcode and sets it up for further action. """

		# Set class variables
		self.type = type
		self.text_value = text_value

		# Create the barcode
		barcode = createBarcodeDrawing(
			type, 
			value=text_value, 
			humanReadable=True
		)

		# Determine the unit to use for measurement, if any
		if unit == 'mm':
			width *= units.mm

		elif unit == 'inch':
			width *= units.inch
		
		# Determine the barcode height automatically.
		# Based on code found here:
		# http://stackoverflow.com/a/13350788
		barcode_scale = width / barcode.width
		height = barcode.height * barcode_scale

		# Create the drawing
		self.drawing = Drawing(width, height)
		self.drawing.scale(barcode_scale, barcode_scale)
		self.drawing.add(barcode, name='barcode')


	def save(self, location, filename, formats):
		""" Save the barcode """
		self.drawing.save(formats, location, fnRoot=filename)

	def asImage(self, format):
		image_string = self.drawing.asString(format)
		return base64.b64encode(image_string).decode('ascii')


if __name__ == '__main__':
	Barcode("Code128", "Test", 200).save(
		location='.', 
		filename='test_barcode', 
		formats=['png']
	)