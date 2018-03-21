import unittest

import barmycodes


class BarmycodesTestCase(unittest.TestCase):
    def setUp(self):
        """ Setup for testing """
        barmycodes.app.config['TESTING'] = True
        self.app = barmycodes.app.test_client()

    def test_no_barcodes(self):
        """ When loading /, there should be no
        barcodes on the page. """
        index = self.app.get('/')
        assert b'Your barcodes will showup here.' in index.data

    def test_barcodes(self):
        """ When loading /?b[]=test there should be
        a barcode on the page."""
        index = self.app.get('/?b[]=test')
        assert b'<img class="barcode"' in index.data


if __name__ == '__main__':
    unittest.main()
