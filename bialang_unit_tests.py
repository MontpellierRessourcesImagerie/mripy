from mripy.bialang import *
import unittest
from ij import WindowManager, IJ
from ij.gui import Roi
import sys

class findEdgesTest(unittest.TestCase):

	def setUp(self):
		unittest.TestCase.setUp(self)
		IJ.run("Close All");

	def tearDown(self):
		unittest.TestCase.tearDown(self)
		IJ.run("Close All");

	def testRectangle(self):
		image = IJ.createImage("test", "8-bit black", 255, 255, 1)
		image.show()
		IJ.setForegroundColor(255,255,255);
		image.getProcessor().fillRect(10, 10, 100, 100)
		
		findEdges(image);

		v1 = image.getPixel(8,8)[0]
		v2 = image.getPixel(9,9)[0]
		v3 = image.getPixel(10,10)[0]
		v4 = image.getPixel(11,11)[0]
	
		self.assertEquals(v1, 0)
		self.assertEquals(v2, 255)
		self.assertEquals(v3, 255)
		self.assertEquals(v4, 0)

def suite():
	suite = unittest.TestSuite()

	suite.addTest(findEdgesTest('testRectangle'))

	return suite

runner = unittest.TextTestRunner(sys.stdout, verbosity=1)
runner.run(suite())