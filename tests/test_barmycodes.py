import os
import barmycodes
import unittest
import tempfile

class BarmycodesTestCase(unittest.TestCase):

	def setUp(self):
		""" Setup for testing """
		barmycodes.app.config['TESTING'] = True
		self.app = barmycodes.app.test_client()

	def test_no_barcodes(self):
		index = self.app.get('/')
		assert b'No barcodes.' in index.data

	def test_barcodes(self):
		index = self.app.get('/test')
		assert b'<img class="barcode"' in index.data

if __name__ == '__main__':
	unittest.main()