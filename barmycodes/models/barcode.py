from reportlab.lib import units
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing
import base64


class Barcode:
    """Model of a barcode object. This class handles the generation
    and parsing of barcodes to image strings."""

    unit_mapping = {'inch': units.inch, 'mm': units.mm}

    DEFAULT_WIDTH_CODE128 = 200
    DEFAULT_WIDTH_QR = 100

    def __init__(self, type, text_value, width=None, height=None, unit=None):
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

        width, height, scale = self._determine_dimensions(barcode, width, height, unit)

        # Create the drawing
        self.drawing = Drawing(width, height)
        self.drawing.scale(scale, scale)
        self.drawing.add(barcode, name='barcode')


    def _determine_dimensions(self, barcode, width, height, unit):
        """Determine the dimensions and scale of the barcode."""

        # Determine the width
        if width:
            width = float(width) * self.unit_mapping.get(unit, units.mm)
        else:
            width = self.DEFAULT_WIDTH_CODE128 if self.type == 'Code128' \
                else self.DEFAULT_WIDTH_QR

            width *= self.unit_mapping.get(unit, units.mm)

        # Determine the scale
        scale = width / barcode.width

        # Determine the height
        if height:
            height = float(height) * self.unit_mapping.get(unit, units.mm)
        else:
            # Determine the barcode height automatically.
            # Based on code found here:
            # http://stackoverflow.com/a/13350788
            height = barcode.height * scale


        return (width, height, scale)


    def save(self, location, filename, formats):
        """ Save the barcode """
        self.drawing.save(formats, location, fnRoot=filename)

    def as_string(self, format):
        """Return the barcode as a string in the specified format."""
        return self.drawing.asString(format)

    def as_image(self, format):
        """Return the barcode as an image in the specified format."""
        image_string = self.drawing.asString(format)
        return base64.b64encode(image_string).decode('ascii')

    @property
    def width(self):
        """Get the width of the barcode drawing."""
        return self.drawing.width

    @property
    def height(self):
        """Get the height of the barcode drawing."""
        return self.drawing.height


if __name__ == '__main__':
    Barcode("Code128", "Test", 200).save(
        location='.',
        filename='test_barcode',
        formats=['png']
    )
