from __future__ import print_function, division
import __builtin__
from mripy.ijmpy import *
import unittest
from ij import WindowManager
from ij.gui import Roi
import sys, time

class MathTest(unittest.TestCase):
	
	def testAcos(self):
		value = acos(0.5)
		self.assertEquals(round(value, 3), 1.047)

	def testAsin(self):
		value = asin(0.5)
		self.assertEquals(round(value, 3), 0.524)

	def testAtan(self):
		value = atan(0.5)
		self.assertEquals(round(value, 3), 0.464)

	def testAtan2(self):
		value = atan2(2, 1)
		self.assertEquals(round(value,4), 1.1071)

	def testCos(self):
		res = cos(2*PI)
		self.assertEquals(res, 1)
		
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

	def testGetSequence(self):
		seq = Array.getSequence(4)
		self.assertEquals(len(seq), 4)
		self.assertEquals(seq[0], 0)
		self.assertEquals(seq[1], 1)
		self.assertEquals(seq[2], 2)
		self.assertEquals(seq[3], 3)

	def testGetStatistics(self):
		array = [1, 2, 3, 4, 5, 6, 7 ,8, 9, 10]
		min, max, mean, stddev = Array.getStatistics(array)
		self.assertEquals(min, 1)
		self.assertEquals(max, 10)
		self.assertEquals(mean, 5.5)
		self.assertEquals(round(stddev, 4), 3.0277) 

	def testPrint(self):
		array = [1, 2, 3, 'a', 'b']
		Array.print(array)
		content = IJ.getLog()
		lines = content.split("\n")
		self.assertEquals(lines[-2], "1, 2, 3, a, b")

	def testRankPositionsInt(self):
		array = [10, 9, 8, 7, 7, 6 ,5]
		ranks = Array.rankPositions(array)
		self.assertEquals(ranks[0], 6)
		self.assertEquals(ranks[1], 5)
		self.assertEquals(ranks[2], 3)
		self.assertEquals(ranks[3], 4)
		self.assertEquals(ranks[4], 2)
		self.assertEquals(ranks[5], 1)
		self.assertEquals(ranks[6], 0)

	def testRankPositionsString(self):
		array = ["the", "quick", "brown", "fox"]
		ranks = Array.rankPositions(array)
		self.assertEquals(ranks[0], 2)
		self.assertEquals(ranks[1], 3)
		self.assertEquals(ranks[2], 1)
		self.assertEquals(ranks[3], 0)

	def testResampleBigger(self):
		array = [1, 2, 3, 4, 5]
		resampled = Array.resample(array, 10)
		self.assertEquals(len(resampled), 10)
		self.assertEquals(resampled[0], 1)
		self.assertEquals(resampled[-1], 5)

	def testResampleSmaller(self):
		array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		resampled = Array.resample(array, 5)
		self.assertEquals(len(resampled), 5)
		self.assertEquals(resampled[0], 1)
		self.assertEquals(resampled[-1], 10)

	def testReverse(self):
		array = [1, 2, 3]
		Array.reverse(array)
		self.assertEquals(array[0], 3)
		self.assertEquals(array[1], 2)
		self.assertEquals(array[2], 1)

	def testShowOneArray(self):
		array = [1.234, 2.345, 3.456, 4.567]
		rt = Array.show(array);
		run('Close')
		self.assertEquals(rt.getTitle(), "array")
		self.assertEquals(rt.getColumnHeading(0), "Value")
		values = rt.getColumn(0)
		self.assertEquals(round(values[0], 3), 1.234)
		self.assertEquals(round(values[1], 3), 2.345)
		self.assertEquals(round(values[2], 3), 3.456)
		self.assertEquals(round(values[3], 3), 4.567)

	def testShowTwoArrays(self):
		array1 = [1.234, 2.345, 3.456, 4.567]
		array2 = [5.678, 6.789, 7.890, 8.901]
		rt = Array.show(array1, array2);
		run('Close')
		self.assertEquals(rt.getTitle(), "Arrays")
		self.assertEquals(rt.getColumnHeading(0), "array1")
		self.assertEquals(rt.getColumnHeading(1), "array2")
		values = rt.getColumn(0)
		self.assertEquals(round(values[0], 3), 1.234)
		self.assertEquals(round(values[1], 3), 2.345)
		self.assertEquals(round(values[2], 3), 3.456)
		self.assertEquals(round(values[3], 3), 4.567)
		values = rt.getColumn(1)
		self.assertEquals(round(values[0], 3), 5.678)
		self.assertEquals(round(values[1], 3), 6.789)
		self.assertEquals(round(values[2], 3), 7.890)
		self.assertEquals(round(values[3], 3), 8.901)

	def testShowArrayWithTitle(self):
		array = [1.234, 2.345, 3.456, 4.567]
		rt = Array.show('data', array);
		run('Close')
		self.assertEquals(rt.getTitle(), "data")
		self.assertEquals(rt.getColumnHeading(0), "Value")
		values = rt.getColumn(0)
		self.assertEquals(round(values[0], 3), 1.234)
		self.assertEquals(round(values[1], 3), 2.345)
		self.assertEquals(round(values[2], 3), 3.456)
		self.assertEquals(round(values[3], 3), 4.567)

	def testShowTwoArraysWithTitle(self):
		array1 = [1.234, 2.345, 3.456, 4.567]
		array2 = [5.678, 6.789, 7.890, 8.901]
		rt = Array.show('data', array1, array2);
		run('Close')
		self.assertEquals(rt.getTitle(), "data")
		self.assertEquals(rt.getColumnHeading(0), "array1")
		self.assertEquals(rt.getColumnHeading(1), "array2")
		values = rt.getColumn(0)
		self.assertEquals(round(values[0], 3), 1.234)
		self.assertEquals(round(values[1], 3), 2.345)
		self.assertEquals(round(values[2], 3), 3.456)
		self.assertEquals(round(values[3], 3), 4.567)
		values = rt.getColumn(1)
		self.assertEquals(round(values[0], 3), 5.678)
		self.assertEquals(round(values[1], 3), 6.789)
		self.assertEquals(round(values[2], 3), 7.890)
		self.assertEquals(round(values[3], 3), 8.901)

	def testShowTwoArraysWithIndexes(self):
		array1 = [1.234, 2.345, 3.456, 4.567]
		array2 = [5.678, 6.789, 7.890, 8.901]
		rt = Array.show('data (indexes)', array1, array2);
		run('Close')
		self.assertEquals(rt.getTitle(), "data")
		self.assertEquals(rt.getColumnHeading(0), "array1")
		self.assertEquals(rt.getColumnHeading(1), "array2")
		
		row = rt.getRowAsString(0)
		columns = row.split("\t")
		self.assertEquals(columns[0], '0')
		
		row = rt.getRowAsString(3)
		columns = row.split("\t")
		self.assertEquals(columns[0], '3')
		
		values = rt.getColumn(0)
		self.assertEquals(round(values[0], 3), 1.234)
		self.assertEquals(round(values[1], 3), 2.345)
		self.assertEquals(round(values[2], 3), 3.456)
		self.assertEquals(round(values[3], 3), 4.567)
		values = rt.getColumn(1)
		self.assertEquals(round(values[0], 3), 5.678)
		self.assertEquals(round(values[1], 3), 6.789)
		self.assertEquals(round(values[2], 3), 7.890)
		self.assertEquals(round(values[3], 3), 8.901)

	def testShowTwoArraysWithRowNumbers(self):
		array1 = [1.234, 2.345, 3.456, 4.567]
		array2 = [5.678, 6.789, 7.890, 8.901]
		rt = Array.show('data (row numbers)', array1, array2);
		run('Close')
		self.assertEquals(rt.getTitle(), "data")
		self.assertEquals(rt.getColumnHeading(0), "array1")
		self.assertEquals(rt.getColumnHeading(1), "array2")
		
		row = rt.getRowAsString(0)
		columns = row.split("\t")
		self.assertEquals(columns[0], '1')
		
		row = rt.getRowAsString(3)
		columns = row.split("\t")
		self.assertEquals(columns[0], '4')
		
		values = rt.getColumn(0)
		self.assertEquals(round(values[0], 3), 1.234)
		self.assertEquals(round(values[1], 3), 2.345)
		self.assertEquals(round(values[2], 3), 3.456)
		self.assertEquals(round(values[3], 3), 4.567)
		values = rt.getColumn(1)
		self.assertEquals(round(values[0], 3), 5.678)
		self.assertEquals(round(values[1], 3), 6.789)
		self.assertEquals(round(values[2], 3), 7.890)
		self.assertEquals(round(values[3], 3), 8.901)

	def testShowArrayResults(self):
		array = [1.234, 2.345, 3.456, 4.567]
		rt = Array.show('Results', array);
		self.assertEquals(rt.getTitle(), "Results")
		self.assertEquals(rt.getColumnHeading(0), "Value")
		values = rt.getColumn(0)
		self.assertEquals(round(values[0], 3), 1.234)
		self.assertEquals(round(values[1], 3), 2.345)
		self.assertEquals(round(values[2], 3), 3.456)
		self.assertEquals(round(values[3], 3), 4.567)
		run('Close')

	def testSlice(self):
		array = [1, 2, 3, 4, 5]
		# remove first element
		sliced = Array.slice(array, 1)
		self.assertEquals(sliced[0], 2)
		# remove last element
		sliced = Array.slice(array, 0, len(array)-1);
		self.assertEquals(sliced[-1], 4)
		# extract first two elements
		sliced = Array.slice(array, 0, 2)
		self.assertEquals(sliced[0], 1)
		self.assertEquals(sliced[1], 2)
		self.assertEquals(len(sliced), 2)
		# extract last two elements
		sliced = Array.slice(array, len(array)-2);
		self.assertEquals(sliced[0], 4)
		self.assertEquals(sliced[1], 5)
		self.assertEquals(len(sliced), 2)

	def testSort(self):
		array = ["delta", "alpha", "Gamma", "Beta"]
		Array.sort(array)
		self.assertEquals(array[0], 'alpha')
		self.assertEquals(array[1], 'Beta')
		self.assertEquals(array[2], 'delta')
		self.assertEquals(array[3], 'Gamma')
		array = [4, 2, 3, 1]
		Array.sort(array)
		self.assertEquals(array[0], 1)
		self.assertEquals(array[1], 2)
		self.assertEquals(array[2], 3)
		self.assertEquals(array[3], 4)

	def testTrim(self):
		array = [1, 2, 3, 4, 5, 6, 7, 8]
		trimmed = Array.trim(array, 3)
		self.assertEquals(len(trimmed), 3)
		self.assertEquals(trimmed[0], 1)
		self.assertEquals(trimmed[1], 2)
		self.assertEquals(trimmed[2], 3)
		array = [1, 2, 3]
		trimmed = Array.trim(array, 5)
		self.assertEquals(len(trimmed), 3)
		self.assertEquals(trimmed[0], 1)
		self.assertEquals(trimmed[1], 2)
		self.assertEquals(trimmed[2], 3)

	def testRotate(self):
		array = [0, 1, 2, "three", 4, 5, 6, 7, 8, 9]
		Array.rotate(array, 1)
		self.assertEquals(len(array), 10)
		self.assertEquals(array[0], 9)
		self.assertEquals(array[-1], 8)
		array = [0, 1, 2, "three", 4, 5, 6, 7, 8, 9]
		Array.rotate(array, -3)
		self.assertEquals(len(array), 10)
		self.assertEquals(array[0], 'three')
		self.assertEquals(array[-1], 2)

	def testGetVertexAngles(self):
		x = [260.0004, 242.7981, 197.8065, 142.1838, 97.1959, 79.9999, 97.2080, 142.2034, 197.8261, 242.8102]
		y = [170, 222.8958, 255.6012, 255.5979, 222.8874, 169.9895, 117.0956, 84.3954, 84.4054, 117.1212]
		angles = Array.getVertexAngles(x, y, 1)
		self.assertEquals(len(angles), 10)
		self.assertEquals(round(angles[0]), 36.0)
		self.assertEquals(round(angles[9]), 36.0)

class CallTest(unittest.TestCase):

	def testNoParameter(self):
		ver = call('ij.IJ.getVersion')
		containsPoint = (ver.find('.') >=0)
		containsSlash = (ver.find('/') >=0)
		self.assertEquals(containsPoint, True)
		self.assertEquals(containsSlash, True)

	def testWithParameter(self):
		 demoString = call("ij.Prefs.get", "demo.string", "Text for preferences file")
		 self.assertEquals(demoString, "Text for preferences file")

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

class AutoUpdateTest(unittest.TestCase):

	def testAutoUpdate(self):
		autoUpdate(False)
		self.assertEquals(isAutoUpdate(), False)
		autoUpdate(True)
		self.assertEquals(isAutoUpdate(), True)

class BeepTest(unittest.TestCase):

	def testBeep(self):
		beep()
		self.assertEquals(True, True)

class BitDepthTest(unittest.TestCase):
	def setUp(self):
		unittest.TestCase.setUp(self)
		run("Close All");

	def tearDown(self):
		unittest.TestCase.tearDown(self)
		run("Close All");
	
	def testBitDepth8(self):
		newImage("Ramp", "8-bit ramp", 256, 256, 1);
		bd = bitDepth()
		self.assertEquals(bd, 8)

	def testBitDepth16(self):
		newImage("Ramp", "16-bit ramp", 256, 256, 1);
		bd = bitDepth()
		self.assertEquals(bd, 16)

	def testBitDepth24(self):
		newImage("Ramp", "RGB ramp", 256, 256, 1);
		bd = bitDepth()
		self.assertEquals(bd, 24)

	def testBitDepth32(self):
		newImage("Ramp", "32-bit ramp", 256, 256, 1);
		bd = bitDepth()
		self.assertEquals(bd, 32)

class CalibrateTest(unittest.TestCase):
	def setUp(self):
		unittest.TestCase.setUp(self)
		run("Close All");

	def tearDown(self):
		unittest.TestCase.tearDown(self)
		run("Close All");

	def testCalibrateNone(self):
		newImage("Ramp", "8-bit ramp", 256, 256, 1);
		cv = calibrate(128)
		self.assertEquals(cv, 128)

	def testCalibrate(self):
		imp = newImage("Ramp", "8-bit ramp", 256, 256, 1);
		IJ.run(imp, "Calibrate...", "function=[Straight Line] unit=[Gray Value] text1=[0 255] text2=[0 1]");
		cv = calibrate(0)
		self.assertEquals(cv, 0)
		cv = calibrate(255)
		self.assertEquals(cv, 1)

class ChangeValuesTest(unittest.TestCase):
	def setUp(self):
		unittest.TestCase.setUp(self)
		run("Close All");

	def tearDown(self):
		unittest.TestCase.tearDown(self)
		run("Close All");

	def test8BitWithoutRoi(self):
		imp = newImage("Ramp", "8-bit ramp", 256, 256, 1);
		changeValues(100, 110, 255);
		self.assertEquals(getPixel(99, 0), 99)
		self.assertEquals(getPixel(100, 0), 255)
		self.assertEquals(getPixel(110, 0), 255)
		self.assertEquals(getPixel(111, 0), 111)

	def test8BitWithRoi(self):
		imp = newImage("Ramp", "8-bit ramp", 256, 256, 1);
		IJ.makeRectangle(10, 10, 10, 10)
		changeValues(0, 100, 255);
		self.assertEquals(getPixel(9, 15), 9)
		self.assertEquals(getPixel(10, 15), 255)
		self.assertEquals(getPixel(19, 15), 255)
		self.assertEquals(getPixel(20, 15), 20)

	def test16Bit(self):
		imp = newImage("Ramp", "16-bit ramp", 256, 256, 1);
		changeValues(100*256, 110*256, 255);
		self.assertEquals(getPixel(99, 0), 99*256)
		self.assertEquals(getPixel(100, 0), 255)
		self.assertEquals(getPixel(110, 0), 255)
		self.assertEquals(getPixel(111, 0), 111*256)

	def test32Bit(self):
		imp = newImage("Ramp", "32-bit ramp", 256, 256, 1);
		changeValues(100/256.0, 110/256.0, 1);
		self.assertEquals(getPixel(99, 0), 99/256.0)
		self.assertEquals(getPixel(100, 0), 1)
		self.assertEquals(getPixel(110, 0), 1)
		self.assertEquals(getPixel(111, 0), 111/256.0)

class CharCodeAtTest(unittest.TestCase):
	def testCharCodeAt(self):
		name = 'Bäcker'
		code = charCodeAt(name, 1)
		self.assertEquals(code, 228)

class D2STest(unittest.TestCase):
	def testD2S(self):
		res = d2s(2/3.0, 2)
		self.assertEquals(res, '0.67')
	
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

		# the new window, is not always the active window, manually make sure it is
		win = WindowManager.getWindow("Ramp-1")
		WindowManager.setCurrentWindow(win)
		width = getWidth()
		
		self.assertEqual(width, 512)												

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

	suite.addTest(MathTest('testAcos'))
	suite.addTest(MathTest('testAsin'))
	suite.addTest(MathTest('testAtan'))
	suite.addTest(MathTest('testAtan2'))
	suite.addTest(MathTest('testCos'))
	
	suite.addTest(ArrayTest('testConcat'))
	suite.addTest(ArrayTest('testCopy'))
	suite.addTest(ArrayTest('testDeleteValue'))
	suite.addTest(ArrayTest('testDeleteIndex'))
	suite.addTest(ArrayTest('testFill'))
	suite.addTest(ArrayTest('testFindMaxima'))
	suite.addTest(ArrayTest('testFindMinima'))
	suite.addTest(ArrayTest('testFourier'))
	suite.addTest(ArrayTest('testGetSequence'))
	suite.addTest(ArrayTest('testGetStatistics'))
	suite.addTest(ArrayTest('testPrint'))
	suite.addTest(ArrayTest('testRankPositionsInt'))
	suite.addTest(ArrayTest('testRankPositionsString'))
	suite.addTest(ArrayTest('testResampleBigger'))
	suite.addTest(ArrayTest('testResampleSmaller'))
	suite.addTest(ArrayTest('testReverse'))
	suite.addTest(ArrayTest('testShowOneArray'))
	suite.addTest(ArrayTest('testShowTwoArrays'))
	suite.addTest(ArrayTest('testShowArrayWithTitle'))
	suite.addTest(ArrayTest('testShowTwoArraysWithTitle'))
	suite.addTest(ArrayTest('testShowTwoArraysWithIndexes'))
	suite.addTest(ArrayTest('testShowTwoArraysWithRowNumbers'))
	suite.addTest(ArrayTest('testShowArrayResults'))
	suite.addTest(ArrayTest('testSlice'))
	suite.addTest(ArrayTest('testSort'))
	suite.addTest(ArrayTest('testTrim'))
	suite.addTest(ArrayTest('testRotate'))
	suite.addTest(ArrayTest('testGetVertexAngles'))

	suite.addTest(AutoUpdateTest('testAutoUpdate'))

	suite.addTest(BeepTest('testBeep'))

	suite.addTest(ChangeValuesTest('test8BitWithoutRoi'))
	suite.addTest(ChangeValuesTest('test8BitWithRoi'))
	suite.addTest(ChangeValuesTest('test16Bit'))
	suite.addTest(ChangeValuesTest('test32Bit'))
	
	suite.addTest(BitDepthTest('testBitDepth8'))
	suite.addTest(BitDepthTest('testBitDepth16'))
	suite.addTest(BitDepthTest('testBitDepth24'))
	suite.addTest(BitDepthTest('testBitDepth32'))

	suite.addTest(CalibrateTest('testCalibrateNone'))
	suite.addTest(CalibrateTest('testCalibrate'))

	suite.addTest(CallTest('testNoParameter'))
	suite.addTest(CallTest('testWithParameter'))

	suite.addTest(CharCodeAtTest('testCharCodeAt'))
	
	suite.addTest(CloseTest('testCloseNoParameter'))
	suite.addTest(CloseTest('testCloseWithParameter'))

	suite.addTest(D2STest('testD2S'))

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
