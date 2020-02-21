from __future__ import print_function
import __builtin__
from mripy.ijmpy import *
import unittest
from ij import WindowManager
from ij.gui import Roi
import sys

class ArrayTest(unittest.TestCase):
	def testConcat(self):
		array1 = newArray(1, 2, 3)
		array2 = newArray("a", "b")
		element1 = "c"
		element2 = 4
		array = Array.concat(element1, array1)
		self.assertEquals(len(array), 4)
		self.assertEquals(array[0], "c")
		self.assertEquals(array[1], 1)
		array = Array.concat(array, element2)
		self.assertEquals(len(array), 5)
		self.assertEquals(array[-1], 4)
		self.assertEquals(array[-2], 3)
		array = Array.concat(array, array2)
		self.assertEquals(len(array), 7)
		self.assertEquals(array[-1], "b")
		self.assertEquals(array[0], "c")

	def testCopy(self):
		array = newArray(1, 2, 3, 4)
		copyOfArray = Array.copy(array)
		copyOfArray[1] = 2.5
		self.assertEquals(copyOfArray[0], 1)
		self.assertEquals(copyOfArray[1], 2.5)
		self.assertEquals(copyOfArray[2], 3)
		self.assertEquals(copyOfArray[3], 4)
		self.assertEquals(array[1], 2)

	def testDeleteValue(self):
		array = newArray(1,0,2,3,0,0,4,0,5,0,0,6,0,0,0,7)
		array = Array.deleteValue(array, 0)
		self.assertEquals(len(array), 7)

	def testDeleteIndex(self):
		array = [1, 2, 3, 4]
		res1 = Array.deleteIndex(array, 0)
		res2 = Array.deleteIndex(array, 1)
		res3 = Array.deleteIndex(array, 2)
		res4 = Array.deleteIndex(array, 3)
		self.assertEquals(len(res1), 3)
		self.assertEquals(res1[0], 2)
		self.assertEquals(len(res2), 3)
		self.assertEquals(res2[1], 3)
		self.assertEquals(len(res3), 3)
		self.assertEquals(res3[2], 4)
		self.assertEquals(len(res4), 3)
		self.assertEquals(res4[2], 3)

	def testFill(self):
		array = [1, 2, 3, 4]
		Array.fill(array, 5)
		self.assertEquals(len(array), 4)
		self.assertEquals(array[0], 5)
		self.assertEquals(array[1], 5)
		self.assertEquals(array[2], 5)
		self.assertEquals(array[3], 5)

	def testFindMaxima(self):
		array = [1, 2, 3, 4, 5, 4, 3, 2, 3, 4, 5, 6, 7, 8, 7, 6, 6, 5]
		maxima = Array.findMaxima(array, 1)
		self.assertEquals(maxima[0], 13)
		self.assertEquals(maxima[1], 4)

	def testFindMinima(self):
		array = [10, 9, 8, 7, 6, 7, 8, 9, 10, 10, 9, 8, 7, 6, 7, 8, 9, 9]
		minima = Array.findMinima(array, 1)
		self.assertEquals(minima[0], 13)
		self.assertEquals(minima[1], 4)

	def testFourier(self):
		array = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
		fourier = Array.fourier(array)
		self.assertEquals(fourier[0], 0.25)
		self.assertEquals(round(fourier[8],4), 0.3536)
		
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

class LengthOfTest(unittest.TestCase):
	def testArray(self):
		emptyList = []
		stringList1 = ["a"]
		intList3 = [1, 2, 3]
		self.assertEqual(lengthOf(emptyList), 0);
		self.assertEqual(lengthOf(stringList1), 1);
		self.assertEqual(lengthOf(intList3), 3);

	def testString(self):
		emptyString = ''
		string1 = 'a'
		string3 = 'abc'
		self.assertEqual(lengthOf(emptyString), 0);
		self.assertEqual(lengthOf(string1), 1);
		self.assertEqual(lengthOf(string3), 3);

class NewArrayTest(unittest.TestCase):
	def testNewWithSize(self):
		emptyList = newArray(0);
		notEmptyList = newArray(3)
		self.assertEquals(lengthOf(emptyList), 0)
		self.assertEquals(lengthOf(notEmptyList), 3)
		self.assertEquals(notEmptyList[1], 0)

	def testNewWithElements(self):
		stringList = newArray("a", "b", "c",)
		intList = newArray(1, 2)
		self.assertEquals(lengthOf(stringList), 3)
		self.assertEquals(lengthOf(intList), 2)

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

	suite.addTest(ArrayTest('testConcat'))
	suite.addTest(ArrayTest('testCopy'))
	suite.addTest(ArrayTest('testDeleteValue'))
	suite.addTest(ArrayTest('testDeleteIndex'))
	suite.addTest(ArrayTest('testFill'))
	suite.addTest(ArrayTest('testFindMaxima'))
	suite.addTest(ArrayTest('testFindMinima'))
	suite.addTest(ArrayTest('testFourier'))
	
	suite.addTest(CloseTest('testCloseNoParameter'))
	suite.addTest(CloseTest('testCloseWithParameter'))

	suite.addTest(GetPixelTest('testGetPixelGrey'))
	suite.addTest(GetPixelTest('testGetPixelGreyFloatCoords'))
	suite.addTest(GetPixelTest('testGetPixelGrey16Bit'))
	suite.addTest(GetPixelTest('testGetPixelColor'))

	suite.addTest(LengthOfTest('testArray'))
	suite.addTest(LengthOfTest('testString'))

	suite.addTest(NewArrayTest('testNewWithSize'))
	suite.addTest(NewArrayTest('testNewWithElements'))
	
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
