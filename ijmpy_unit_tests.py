from __future__ import print_function, division
import __builtin__
import sys, time, unittest, math, os
from ij import WindowManager
from ij.gui import Roi
from ij.macro import Interpreter
from mripy.ijmpy import *

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

	def testExp(self):
		res1 = exp(1)
		res2 = exp(2)
		self.assertEquals(res1, math.e)
		self.assertEquals(round(res2, 14), round(math.e**2, 14))

	def testFloor(self):
		res = floor(3.78)
		self.assertEquals(res, 3)
		
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
		close('Results')
		array = [1.234, 2.345, 3.456, 4.567]
		rt = Array.show('Results', array);
		self.assertEquals(rt.getTitle(), "Results")
		self.assertEquals(rt.getColumnHeading(0), "Value")
		values = rt.getColumn(0)
		self.assertEquals(round(values[0], 3), 1.234)
		self.assertEquals(round(values[1], 3), 2.345)
		self.assertEquals(round(values[2], 3), 3.456)
		self.assertEquals(round(values[3], 3), 4.567)
		close('Results')

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

class DoCommandTest(unittest.TestCase):
	def setUp(self):
		unittest.TestCase.setUp(self)
		run("Close All");

	def tearDown(self):
		unittest.TestCase.tearDown(self)
		run("Close All");

	def testDoCommand(self):
		newImage("HyperStack", "8-bit composite-mode label", 400, 400, 1, 1, 20);
		doCommand("Start Animation");
		scriptIsStillRunning = True
		self.assertEquals(scriptIsStillRunning, True)

class DoWandTest(unittest.TestCase):
	def setUp(self):
		unittest.TestCase.setUp(self)
		run("Close All");

	def tearDown(self):
		unittest.TestCase.tearDown(self)
		run("Close All");

	def testDoWand(self):	
		imp = newImage("test", "8-bit black", 256, 256, 1);
		IJ.makeRectangle(10, 10, 100, 100)
		IJ.setForegroundColor(255, 255, 255);
		run("Fill", "slice");
		run("Select None");

		doWand(50, 50);
		roi = IJ.getImage().getRoi()

		self.assertEquals(len(roi.getContainedPoints()), 10000)

class DrawTest(unittest.TestCase):
	def setUp(self):
		unittest.TestCase.setUp(self)
		run("Close All");
		imp = newImage("test", "8-bit black", 256, 256, 1);
		
	def tearDown(self):
		unittest.TestCase.tearDown(self)
		run("Close All");

	def testDrawLine(self):
		IJ.setForegroundColor(255, 255, 255)
		drawLine(10, 10, 100, 100);
		v1 = getPixel(9, 9);
		v2 = getPixel(10, 10);
		v3 = getPixel(50, 50);
		v4 = getPixel(100, 100);
		v5 = getPixel(101, 101);

		self.assertEquals(v1, 0)
		self.assertEquals(v2, 255)
		self.assertEquals(v3, 255)
		self.assertEquals(v4, 255)
		self.assertEquals(v5, 0)

	def testDrawOval(self):
		IJ.setForegroundColor(255, 255, 255)
		drawOval(128, 128, 50, 50);
		roi = doWand(150, 150)
		self.assertEquals(len(roi.getContainedPoints()), 1877)
		
	def testDrawRect(self):
		IJ.setForegroundColor(255, 255, 255)
		drawRect(128, 128, 50, 50);
		roi = doWand(150, 150)
		self.assertEquals(len(roi.getContainedPoints()), 2304)

	def testDrawString(self):
		IJ.setForegroundColor(255, 255, 255)
		drawString("The quick brown fox...", 50, 50);
		roi = doWand(54, 38);
		self.assertEquals(len(roi.getContainedPoints()), 15)

class EndsWithTest(unittest.TestCase):
	def testEndsWith(self):
		self.assertEquals(endsWith('ijmpy.py','py'), True)
		self.assertEquals(endsWith('ijmpy.py','ijm'), False) 

class EvalTest(unittest.TestCase):
	def testEvalScript(self):
		resText = eval("script", '"ijmpy".bold();')
		self.assertEquals(resText, '<b>ijmpy</b>');

	def testEvalJS(self):
		resText = eval("js", '"ijmpy".blink();')
		self.assertEquals(resText, '<blink>ijmpy</blink>');

	def testEvalBsh(self):
		resText = eval("bsh", '2 + 2;')
		self.assertEquals(resText, '4');

	def testEvalPython(self):
		resText = eval('python', 'import ij\nij.IJ.log("py")')
		log = IJ.getLog()
		log = log.split('\n')
		self.assertEquals(log[-2], "py")

	def testEvalMacro(self):
		resText = eval('sqrt(getArgument())', '9')
		log = IJ.getLog()
		log = log.split('\n')
		self.assertEquals(log[-2], "3")

class ExecTest(unittest.TestCase):
	def testExec(self):
		out = Exec('echo', 'hi echo')
		self.assertEquals(out, 'hi echo\n')

class ExtTest(unittest.TestCase):
	def setUp(self):
		unittest.TestCase.setUp(self)
		run("Close All");
	def tearDown(self):
		unittest.TestCase.tearDown(self)
		run("Close All");
	def testExt(self):
		IJ.run("New Image5D", "name=Untitled type=8-bit fill=Ramp width=256 height=256 channels=3 slices=1 frames=1");
		Ext.install('sc.fiji.i5d.plugin.Image5D_Extensions')
		Ext.setDisplayMode('overlay')
		dm = Ext.getDisplayMode()
		self.assertEquals(dm, 'overlay')
		Ext.setDisplayMode('color')
		dm = Ext.getDisplayMode()
		self.assertEquals(dm, 'color')

class FileTest(unittest.TestCase):
	def setUp(self):
		unittest.TestCase.setUp(self)
		if os.path.exists('./test.txt'):
			os.remove('./test.txt')
		if os.path.exists('./test'):
			os.rmdir('./test')

	def tearDown(self):
		unittest.TestCase.tearDown(self)
		if os.path.exists('./test.txt'):
			os.remove('./test.txt')
		if os.path.exists('./test'):
			os.rmdir('./test')
			
	def testAppend(self):
		File.append('THE END', './test.txt')
		with open('./test.txt', 'r') as aFile:
			content = aFile.read()
		lines = content.split('\n')
		self.assertEquals(lines[-1], 'THE END') 

	def testOpen(self):
		aFile = File.open('./test.txt')
		print(aFile, 'test test')
		File.close(aFile)

		with open ("/home/baecker/test.txt", "r") as myfile:
			data=myfile.readlines()[0]

		self.assertEquals(data, 'test test')

	def testClose(self):
		aFile = File.open('./test.txt')
		print(aFile, 'test test')
		File.close(aFile)

		self.assertEquals(aFile.closed, True)

	def testCopy(self):
		aFile = File.open('./test.txt')
		print(aFile, 'test test')
		File.close(aFile)
		File.copy('./test.txt', './test2.txt')
		with open ("./test2.txt", "r") as myfile:
			data=myfile.readlines()[0]

		self.assertEquals(data, 'test test')
		os.remove('./test2.txt')

	def testDateLastModified(self):
		before = time.ctime()
		f = File.open('test.txt')
		print(f, "test test")
		File.close(f)
		mtime = time.ctime(os.path.getmtime("test.txt"))
		after = time.ctime()
		self.assertEquals(before<=mtime, True)
		self.assertEquals(mtime<=after, True)

	def testDelete(self):
		f = File.open('test.txt')
		print(f, "test test")
		File.close(f)
		self.assertEquals(os.path.isfile('test.txt'), True)

		File.delete('test.txt')
		self.assertEquals(os.path.isfile('test.txt'), False)

	def testDirectory(self):
		aDir = File.directory
		self.assertEquals(os.path.isdir(aDir) or aDir=='', True)

	def testGetDefaultDir(self):
		cDir = File.getDefaultDir()
		self.assertEquals(os.path.isdir(cDir), True)

	def testSetDefaultDir(self):
		dd = File.getDefaultDir()
		os.mkdir('./ijmpytest')
		File.setDefaultDir('./ijmpytest')
		self.assertEquals(File.getDefaultDir(), dd + '/ijmpytest')
		File.setDefaultDir(dd)
		File.delete('./ijmpytest')
		
	def testExists(self):
		res = File.exists('.')
		self.assertEquals(res, True)
		res = File.exists('/mumpitz')
		self.assertEquals(res, False)
		f = File.open('test.txt')
		print(f, "test test")
		File.close(f)
		res = File.exists('test.txt')
		self.assertEquals(res, True)

	def testGetName(self):
		name = File.getName('a/b/c/blobs.tif')
		self.assertEquals(name, 'blobs.tif')

	def testGetNameWithoutExtension(self):
		name = File.getNameWithoutExtension('a/b/c/blobs.tif')
		self.assertEquals(name, 'blobs')

	def testGetDirectory(self):
		aDir = File.getDirectory('a/b/c/blobs.tif')
		self.assertEquals(aDir, 'a/b/c')

	def testGetParent(self):
		parent = File.getParent('/a/b/c')
		self.assertEquals(parent, '/a/b')

	def testIsDirectory(self):
		self.assertEquals(File.isDirectory("./"), True)
		self.assertEquals(File.isDirectory("./test.txt"), False)

	def testLastModified(self):
		before = round(time.time(), 0) - 1
		f = File.open('test.txt')
		print(f, "test test")
		File.close(f)
		lastModified = File.lastModified('./test.txt')
		after = time.time()
		print(before, lastModified, after)
		self.assertEquals(before<=lastModified, True)
		self.assertEquals(lastModified<=after, True)

	def testLength(self):
		f = File.open('test.txt')
		print(f, "test test")
		File.close(f)
		l = File.length('test.txt')
		self.assertEquals(l, 9)

	def testMakeDirectory(self):
		File.makeDirectory('test')
		self.assertEquals(File.isDirectory('test'), True)
		File.delete('test')

	def testName(self):
		aName = File.name
		aDir = File.directory		
		self.assertEquals(os.path.isfile(aDir+'/'+aName) or aName=='' or aDir=='', True)

	def testNameWithoutExtension(self):
		aNameWithExt = File.name
		aNameWithoutExt = File.nameWithoutExtension
		n = len(aNameWithExt.split('.')) - len(aNameWithoutExt.split('.')) 
		self.assertEquals(aNameWithExt=='' or (n>=0 and n<2), True)

	def testOpenAsString(self):
		f = File.open('test.txt')
		print(f, "test test")
		File.close(f)
		text = File.openAsString('test.txt')
		self.assertEquals(text, "test test\n")

	def testOpenAsRawString(self):
		iconPath = IJ.getDirectory('imagej') + 'images/icon.png'
		out = File.openAsRawString(iconPath)
		self.assertEquals(len(out), 5000)

	def testOpenUrlAsString(self):
		content = File.openUrlAsString('https://imagej.net/developer/macro/functions.html') 
		self.assertEquals(content.split('\n')[0].startswith('<!DOCTYPE'), True)
		content = File.openUrlAsString('malformed') 
		self.assertEquals(content.split('\n')[0].startswith('<Error'), True)
		content = File.openUrlAsString('https://gibtsnicht') 
		self.assertEquals(content.split('\n')[0].startswith('<Error'), True)

	def testRename(self):
		f = File.open('test.txt')
		print(f, "test test")
		File.close(f)
		res = File.rename('test.txt', 'test2.txt')
		self.assertEquals(res, True)
		res = File.rename('test2.txt', 'test.txt')

	def testSaveString(self):
		File.saveString('test test', 'test.txt')
		content = File.openAsString('test.txt')
		self.assertEquals(content, 'test test\n')
	
	def testSeparator(self):
		sep = File.separator
		self.assertEquals(sep=="/" or sep=='\\', True)

class FillTest(unittest.TestCase):
	def setUp(self):
		unittest.TestCase.setUp(self)
		run("Close All");
		imp = newImage("test", "8-bit black", 256, 256, 1);
		
	def tearDown(self):
		unittest.TestCase.tearDown(self)
		run("Close All");

	def testFill(self):
		IJ.setForegroundColor(255, 255, 255)
		imp = fill()
		mean = IJ.getValue(imp, 'Mean')
		self.assertEquals(mean, 255)
		run("Close All");
		newImage("test", "8-bit black", 256, 256, 1);
		IJ.makeRectangle(64, 64, 128, 128)
		imp = fill()
		IJ.run("Select None")
		mean = IJ.getValue(imp, 'Mean')
		self.assertEquals(mean, 63.75)

	def testFillOval(self):
		IJ.setForegroundColor(255, 255, 255)
		fillOval(128, 128, 50, 50);
		roi = doWand(150, 150)
		self.assertEquals(len(roi.getContainedPoints()), 1976)

	def testFillRect(self):
		IJ.setForegroundColor(255, 255, 255)
		fillRect(128, 128, 50, 50);
		roi = doWand(150, 150)
		self.assertEquals(len(roi.getContainedPoints()), 2500)

class FitTest(unittest.TestCase):
	def testDoFit(self):
		x = [0, 1, 2, 3, 4, 5]
		y = [0, 0.9, 4.5, 8, 18, 24]
		Fit.doFit("Straight Line", x, y)
		a = round(Fit.p(0), 4)
		b = round(Fit.p(1), 4)
		self.assertEquals(a, -3.2524)
		self.assertEquals(b, 4.9943)

		x = [0, 1, 2, 3]
		y = [0, 1, 0, -1]
		equation = "y = a * sin(b*x+c)"
		Fit.doFit(equation, x, y)
		a = round(Fit.p(0), 4)
		b = round(Fit.p(1), 4)
		c = round(Fit.p(2), 4)
		self.assertEquals(a, 1.0000)
		self.assertEquals(b, 1.5708)
		self.assertEquals(c, 0.0000)

		x = [0, 1, 2, 3]
		y = [0, 1, 0, -1]
		equation = "y = a * sin(b*x+c)"
		Fit.doFit(equation, x, y, [1, 1.2, 0])
		a = round(Fit.p(0), 4)
		b = round(Fit.p(1), 4)
		c = round(Fit.p(2), 4)
		self.assertEquals(a, 1.0000)
		self.assertEquals(b, 1.5708)
		self.assertEquals(c, 0.0000)

	def testRSquared(self):
		x = [0, 1, 2, 3, 4, 5]
		y = [0, 0.9, 4.5, 8, 18, 24]
		Fit.doFit("Straight Line", x, y)
		rSq = round(Fit.rSquared, 4)
		self.assertEquals(rSq, 0.9218)

	def testP(self):
		x = [0, 1]
		y = [-1, 0]
		Fit.doFit("Straight Line", x, y)	# y = a + b*x 
		a = Fit.p(0)
		b = Fit.p(1)
		self.assertEquals(a, -1)
		self.assertEquals(b, 1)

	def testNParams(self):
		x = [0, 1, 2, 3]
		y = [0, 1, 0, -1]
		equation = "y = a * sin(b*x+c)"
		Fit.doFit(equation, x, y, [1, 1.2, 0])
		self.assertEquals(Fit.nParams, 3)

	def testF(self):
		x = [0, 1]
		y = [-1, 0]
		Fit.doFit("Straight Line", x, y)	# y = a + b*x 
		f2 = Fit.f(2)
		f3 = Fit.f(3)
		self.assertEquals(f2, 1)
		self.assertEquals(f3, 2)
		
	def testNEquations(self):
		self.assertEquals(Fit.nEquations>=25, True)

	def testGetEquation(self):
		name, formula = Fit.getEquation(0)
		self.assertEquals(name, 'Straight Line')
		self.assertEquals(formula, 'y = a+bx')
		name, formula = Fit.getEquation(4)
		self.assertEquals(name, 'Exponential')
		self.assertEquals(formula, 'y = a*exp(bx)')

	def testPlot(self):
		x = [0, 1, 2, 3]
		y = [0, 1, 0, -1]
		equation = "y = a * sin(b*x+c)"
		Fit.doFit(equation, x, y)
		Fit.plot
		title = IJ.getImage().getTitle()
		self.assertEquals(title, equation)
		close()

	def testLogResults(self):
		print('\\Clear')
		Fit.logResults
		x = [0, 1, 2, 3]
		y = [0, 1, 0, -1]
		equation = "y = a * sin(b*x+c)"
		Fit.doFit(equation, x, y)
		content = IJ.getLog()
		lines = content.split("\n")
		self.assertEquals(lines[1], 'Formula: ' + equation)
		print('\\Clear')

class FloodFillTest(unittest.TestCase):
	def setUp(self):
		unittest.TestCase.setUp(self)
		run("Close All")

	def tearDown(self):
		unittest.TestCase.tearDown(self)
		run("Close All")
		IJ.setForegroundColor(255, 255, 255);
		
	def testFloodFill4(self):
		imp = newImage("test", "RGB black", 256, 256, 1);
		IJ.makeRectangle(10, 10, 100, 100)
		IJ.setForegroundColor(255, 255, 255);
		run("Fill", "slice");
		run("Select None");

		IJ.setForegroundColor(0, 0, 255);
		floodFill(55, 55)
		values = IJ.getImage().getPixel(55, 55)
		self.assertEquals(values[0], 0)
		self.assertEquals(values[1], 0)
		self.assertEquals(values[2], 255)

		values = IJ.getImage().getPixel(11, 11)
		self.assertEquals(values[0], 0)
		self.assertEquals(values[1], 0)
		self.assertEquals(values[2], 255)

		values = IJ.getImage().getPixel(99, 99)
		self.assertEquals(values[0], 0)
		self.assertEquals(values[1], 0)
		self.assertEquals(values[2], 255)

	def testFloodFill8(self):
		imp = newImage("test", "RGB black", 256, 256, 1);
		IJ.makeRectangle(10, 10, 100, 100)
		IJ.setForegroundColor(255, 255, 255);
		run("Fill", "slice");
		run("Select None");

		IJ.setForegroundColor(0, 0, 255);
		floodFill(55, 55, '8-connected', imp)
		
		values = imp.getPixel(55, 55)
		self.assertEquals(values[0], 0)
		self.assertEquals(values[1], 0)
		self.assertEquals(values[2], 255)

		values = IJ.getImage().getPixel(11, 11)
		self.assertEquals(values[0], 0)
		self.assertEquals(values[1], 0)
		self.assertEquals(values[2], 255)

		values = IJ.getImage().getPixel(99, 99)
		self.assertEquals(values[0], 0)
		self.assertEquals(values[1], 0)
		self.assertEquals(values[2], 255)

class FromCharCodeTest(unittest.TestCase):
	def testFromCharCode(self):
		aStr = fromCharCode(65, 66, 67)
		self.assertEquals(aStr, 'ABC')

class GetSelectionBoundsTest(unittest.TestCase):
	def setUp(self):
		unittest.TestCase.setUp(self)
		run("Close All");
		imp = newImage("test", "8-bit black", 256, 256, 1);
		
	def tearDown(self):
		unittest.TestCase.tearDown(self)
		run("Close All");

	def testGetSelectionBoundsNoRoi(self):
		x, y, width, height = getSelectionBounds()
		self.assertEquals(x, 0)
		self.assertEquals(y, 0)
		self.assertEquals(width, 256)
		self.assertEquals(height, 256)

	def testGetSelectionBoundsWithRoi(self):
		IJ.makeRectangle(10, 12, 10, 20)
		x, y, width, height = getSelectionBounds()
		self.assertEquals(x, 10)
		self.assertEquals(y, 12)
		self.assertEquals(width, 10)
		self.assertEquals(height, 20)

	def testGetBoundingRect(self):
		x, y, width, height = getBoundingRect()
		self.assertEquals(x, 0)
		self.assertEquals(y, 0)
		self.assertEquals(width, 256)
		self.assertEquals(height, 256)

class GetDateAndTimeTest(unittest.TestCase):
	def testGetDateAndTime(self):
		year, month, _, day, hour, minute, second, _ = getDateAndTime()
		self.assertEquals(year>2019, True)
		self.assertEquals(month>=0 and month<12, True)
		self.assertEquals(day>0 and day<32, True)
		self.assertEquals(hour>=0 and hour<=24, True)
		self.assertEquals(minute>=0 and minute<60, True)
		self.assertEquals(second>=0 and second<60, True)

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

class NResultsTest(unittest.TestCase):
	def setUp(self):
		unittest.TestCase.setUp(self)
		newImage("Ramp", "8-bit ramp", 256, 256, 1);
		
	def tearDown(self):
		unittest.TestCase.tearDown(self)
		run("Close All");
		close("Results");
		
	def testNResults(self):
		n1 = nResults()
		self.assertEquals(n1, 0)
		IJ.makeRectangle(10, 10, 10, 10)
		roiManager("add")
		roiManager("measure")
		self.assertEquals(nResults(), 1)
		
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
		print('\\Clear');

	def tearDown(self):
		unittest.TestCase.tearDown(self)
		run("Close All");
		print('\\Clear');

	def testRunNoParameter(self):
		newImage("Ramp", "8-bit ramp", 256, 256, 1);

		run("Invert");
		self.assertEqual(getPixel(0, 0), 255)

	def testRunWithParameterString(self):
		image = newImage("Ramp", "8-bit ramp", 256, 256, 1);
		image.show();
		Interpreter.batchMode = True
		run("Scale...", "x=2 y=2 width=512 height=512 interpolation=Bilinear create");
		Interpreter.batchMode = False
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
	suite.addTest(MathTest('testExp'))
	suite.addTest(MathTest('testFloor'))
	
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
	suite.addTest(DoCommandTest('testDoCommand'))
	suite.addTest(DoWandTest('testDoWand'))

	suite.addTest(DrawTest('testDrawLine'))
	suite.addTest(DrawTest('testDrawOval'))
	suite.addTest(DrawTest('testDrawRect'))
	suite.addTest(DrawTest('testDrawString'))

	suite.addTest(EndsWithTest('testEndsWith'))

	suite.addTest(EvalTest('testEvalScript'))
	suite.addTest(EvalTest('testEvalJS'))
	suite.addTest(EvalTest('testEvalBsh'))
	suite.addTest(EvalTest('testEvalPython'))
	suite.addTest(EvalTest('testEvalMacro'))

	suite.addTest(ExecTest('testExec'))

	suite.addTest(ExtTest('testExt'))

	suite.addTest(FileTest('testAppend'))
	suite.addTest(FileTest('testOpen'))
	suite.addTest(FileTest('testClose'))
	suite.addTest(FileTest('testCopy'))
	suite.addTest(FileTest('testDateLastModified'))
	suite.addTest(FileTest('testDelete'))
	suite.addTest(FileTest('testDirectory'))
	suite.addTest(FileTest('testExists'))
	suite.addTest(FileTest('testGetName'))
	suite.addTest(FileTest('testGetNameWithoutExtension'))
	suite.addTest(FileTest('testGetDirectory'))
	suite.addTest(FileTest('testGetDefaultDir'))
	suite.addTest(FileTest('testSetDefaultDir'))
	suite.addTest(FileTest('testGetParent'))
	suite.addTest(FileTest('testIsDirectory'))
	suite.addTest(FileTest('testLastModified'))
	suite.addTest(FileTest('testLength'))
	suite.addTest(FileTest('testMakeDirectory'))
	suite.addTest(FileTest('testName'))
	suite.addTest(FileTest('testNameWithoutExtension'))
	suite.addTest(FileTest('testOpenAsString'))
	suite.addTest(FileTest('testOpenAsRawString'))
	suite.addTest(FileTest('testOpenUrlAsString'))
	suite.addTest(FileTest('testRename'))
	suite.addTest(FileTest('testSaveString'))
	suite.addTest(FileTest('testSeparator'))

	suite.addTest(FillTest('testFill'))
	suite.addTest(FillTest('testFillOval'))
	suite.addTest(FillTest('testFillRect'))

	suite.addTest(FitTest('testDoFit'))
	suite.addTest(FitTest('testRSquared'))
	suite.addTest(FitTest('testP'))
	suite.addTest(FitTest('testNParams'))
	suite.addTest(FitTest('testF'))
	suite.addTest(FitTest('testNEquations'))
	suite.addTest(FitTest('testGetEquation'))
	suite.addTest(FitTest('testPlot'))
	suite.addTest(FitTest('testLogResults'))

	suite.addTest(FloodFillTest('testFloodFill4'))
	suite.addTest(FloodFillTest('testFloodFill8'))

	suite.addTest(FromCharCodeTest('testFromCharCode'))

	suite.addTest(GetDateAndTimeTest('testGetDateAndTime'))
	
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
	suite.addTest(NResultsTest('testNResults'))
	suite.addTest(RoiManagerTest('testRoiManagerAnd'))
	suite.addTest(RoiManagerTest('testRoiManagerAdd'))
	suite.addTest(RoiManagerTest('testRoiManagerSelectOneRoi'))
	suite.addTest(RoiManagerTest('testRoiManagerSelectMultipleRois'))

	suite.addTest(RunTest('testRunNoParameter'))
	suite.addTest(RunTest('testRunWithParameterString'))

	suite.addTest(GetSelectionBoundsTest('testGetSelectionBoundsNoRoi'))
	suite.addTest(GetSelectionBoundsTest('testGetSelectionBoundsWithRoi'))
	suite.addTest(GetSelectionBoundsTest('testGetBoundingRect'))

	suite.addTest(ThresholdTest('testSetAutoThreshold'))
	return suite

runner = unittest.TextTestRunner(sys.stdout, verbosity=1)
runner.run(suite())

