from __future__ import print_function
import __builtin__
from mripy.ijmpy import *
import unittest
from ij import WindowManager
from ij.gui import Roi
import sys

class CloseTest(unittest.TestCase):
	def setUp(self):
		unittest.TestCase.setUp(self)
		run("Close All");

	def tearDown(self):
		unittest.TestCase.tearDown(self)
		run("Close All");

	def testCloseNoParameter(self):
		newImage("Ramp", "8-bit ramp", 256, 256, 1);
		self.assertEqual(nImages(), 1);

		close();
		self.assertEqual(nImages(), 0)

	def testCloseWithParameter(self):
		newImage("Ramp", "8-bit ramp", 256, 256, 1);
		newImage("Ramp2", "8-bit ramp", 256, 256, 1);
		self.assertEqual(nImages(), 2);

		close("*");
		self.assertEqual(nImages(), 0)

class GetPixelTest(unittest.TestCase):
	def setUp(self):
		unittest.TestCase.setUp(self)
		run("Close All");

	def tearDown(self):
		unittest.TestCase.tearDown(self)
		run("Close All");

	def testGetPixelGrey(self):
		newImage("Ramp", "8-bit ramp", 256, 256, 1);
		self.assertEquals(getPixel(128, 128), 128)

	def testGetPixelGreyFloatCoords(self):
		newImage("Ramp", "8-bit ramp", 256, 256, 1);
		self.assertEquals(getPixel(128.5, 128.5), 128.5)

	def testGetPixelGrey16Bit(self):
		newImage("Ramp", "16-bit ramp", 256, 256, 1);
		self.assertEquals(getPixel(128, 128), 32768)

	def testGetPixelColor(self):
		newImage("Ramp", "RGB ramp", 256, 256, 1);
		value = getPixel(128, 128);
		red = (value>>16)&0xff;  # extract red byte (bits 23-17)
		green = (value>>8)&0xff; # extract green byte (bits 15-8)
		blue = value&0xff;       # extract blue byte (bits 7-0)
		self.assertEquals(red, 128)
		self.assertEquals(green, 128)
		self.assertEquals(blue, 128)

class NewImageTest(unittest.TestCase):
	def setUp(self):
		unittest.TestCase.setUp(self)
		run("Close All");

	def tearDown(self):
		unittest.TestCase.tearDown(self)
		run("Close All");

	def testNewImage(self):
		newImage("Ramp", "8-bit ramp", 256, 256, 1);
		self.assertEqual(nImages(), 1);

	def testNewHyperstack(self):
		newImage("Ramp", "8-bit ramp", 256, 256, 2, 3, 4);
		self.assertEqual(nImages(), 1);

class NImagesTest(unittest.TestCase):
	def setUp(self):
		unittest.TestCase.setUp(self)
		run("Close All");

	def tearDown(self):
		unittest.TestCase.tearDown(self)
		run("Close All");

	def testNImages(self):
		newImage("Ramp", "8-bit ramp", 256, 256, 1);
		newImage("Ramp", "8-bit ramp", 256, 256, 1);
		newImage("Ramp", "8-bit ramp", 256, 256, 1);

		self.assertEqual(nImages(), 3);

class RoiManagerTest(unittest.TestCase):
	def setUp(self):
		unittest.TestCase.setUp(self)
		run("Close All");
		newImage("Ramp", "8-bit ramp", 256, 256, 1);
		roiManager("reset");

	def tearDown(self):
		unittest.TestCase.tearDown(self)
		run("Close All");
		roiManager("reset");

	def testRoiManagerAnd(self):
		IJ.makeRectangle(10, 10, 10, 10)
		roiManager("add");
		IJ.makeRectangle(15, 15, 10, 10)
		roiManager("add");
		roiManager("and");
		self.assertEqual(IJ.getImage().getRoi().getType(), Roi.RECTANGLE)

	def testRoiManagerAdd(self):
		IJ.makeRectangle(10, 10, 10, 10)
		roiManager("add");
		IJ.makeRectangle(15, 15, 10, 10)
		roiManager("add");
		self.assertEquals(roiManager("count"), 2)

	def testRoiManagerSelectOneRoi(self):
		IJ.makeRectangle(10, 10, 10, 10)
		roiManager("add");
		IJ.makeRectangle(15, 15, 10, 10)
		roiManager("add");
		roiManager("select", 1);
		self.assertEquals(roiManager("index"), 1)

	def testRoiManagerSelectMultipleRois(self):
		IJ.makeRectangle(10, 10, 10, 10)
		roiManager("add");
		IJ.makeRectangle(15, 15, 10, 10)
		roiManager("add");
		IJ.makeRectangle(30, 30, 10, 10)
		roiManager("add");
		IJ.makeRectangle(26, 26, 10, 10)
		roiManager("add");
		roiManager("select", [1,2])
		roiManager("delete")
		self.assertEquals(roiManager("count"), 2)
		
class RunTest(unittest.TestCase):
	def setUp(self):
		unittest.TestCase.setUp(self)
		run("Close All");

	def tearDown(self):
		unittest.TestCase.tearDown(self)
		run("Close All");

	def testRunNoParameter(self):
		newImage("Ramp", "8-bit ramp", 256, 256, 1);

		run("Invert");
		self.assertEqual(getPixel(0, 0), 255)

	def testRunWithParameterString(self):
		newImage("Ramp", "8-bit ramp", 256, 256, 1);

		run("Scale...", "x=2 y=2 width=512 height=512 interpolation=Bilinear create");
		self.assertEqual(getWidth(), 512)													# arbitrarily passes and fails! Why?

class ThresholdTest(unittest.TestCase):
	def setUp(self):
		unittest.TestCase.setUp(self)
		run("Close All");
		newImage("Ramp", "8-bit ramp", 256, 256, 1);

	def tearDown(self):
		unittest.TestCase.tearDown(self)
		run("Close All");

	def testSetAutoThreshold(self):
		setAutoThreshold();
		lower, upper = getThreshold();
		self.assertEqual(lower, 0)
		self.assertEqual(upper, 127)

def suite():
	suite = unittest.TestSuite()

	suite.addTest(CloseTest('testCloseNoParameter'))
	suite.addTest(CloseTest('testCloseWithParameter'))

	suite.addTest(GetPixelTest('testGetPixelGrey'))
	suite.addTest(GetPixelTest('testGetPixelGreyFloatCoords'))
	suite.addTest(GetPixelTest('testGetPixelGrey16Bit'))
	suite.addTest(GetPixelTest('testGetPixelColor'))

	suite.addTest(NewImageTest('testNewImage'))
	suite.addTest(NewImageTest('testNewHyperstack'))

	suite.addTest(NImagesTest('testNImages'))

	suite.addTest(RoiManagerTest('testRoiManagerAnd'))
	suite.addTest(RoiManagerTest('testRoiManagerAdd'))
	suite.addTest(RoiManagerTest('testRoiManagerSelectOneRoi'))
	suite.addTest(RoiManagerTest('testRoiManagerSelectMultipleRois'))

	suite.addTest(RunTest('testRunNoParameter'))
	suite.addTest(RunTest('testRunWithParameterString'))

	suite.addTest(ThresholdTest('testSetAutoThreshold'))

	return suite

runner = unittest.TextTestRunner(sys.stdout, verbosity=1)
runner.run(suite())
