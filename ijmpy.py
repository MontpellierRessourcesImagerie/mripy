''' 
ijmpy is a python wrapper of the imagej-macro-language

It allows to move ij-macro code to python (mostly) without modifications (yes, you can keep the ';')
The aim is to facilitate the step of moving from macro to scripting. You can record your 
macro, use the familiar macro language and learn how to profit from the better code organization
and data-structures (list, tupels, dictionary, ...) in python.

written 2020 by `Volker Baecker`_, `Montpellier Ressources Imagerie`_, Biocampus Montpellier, UM, INSERM, CNRS

.. _`Volker Baecker`: https://github.com/volker-baecker
.. _`Montpellier Ressources Imagerie`: http://www.mri.cnrs.fr

Have fun!

Unimplemented functions
=======================

abs()
-----

When you call 'abs()' the python 'abs()' function is called. The behaviour should be identical.

Other differences with the ij-macro language
============================================

output parameter
----------------

Functions that take output parameter in the macro language are implemented without these parameters 
and return the results as an n-tupel instead.

For example, use:

	min, max, mean, stddev = Array.getStatistics(anArray)

instead of

	Array.getStatistics(anArray, min, max, mean, stddev)

Only in the case that the parameter modified in the function is an array, it is modified in place.
For example:

	Array.fill(array, 0)
	Array.reverse(array)
'''
from __future__ import print_function, division 						# we will overwrite python's print command
import __builtin__														# to use the python print command: __builtin__.print(<text>)
from java.lang import Double, String
from java.awt import Font, Color
from ij import IJ, WindowManager, Prefs
from ij.process import FloatProcessor, ColorProcessor
from ij.plugin import Colors
from ij.plugin.frame import RoiManager
from ij.plugin.filter import MaximumFinder, Analyzer
from ij.process import FHT
from ij.util import Tools
from ij.measure import ResultsTable
from ij.gui import Roi, GenericDialog, NonBlockingGenericDialog
from collections import deque 
import math, sys, importlib

AUTO_UPDATE = True
NaN = Double.NaN
PI = math.pi

def acos(n):
	'''
	Returns the inverse cosine (in radians) of n.
	'''
	return math.acos(n)
	
class Array(object):
	'''
	These functions operate on arrays. Refer to the `ArrayFunctions`_ macro for examples. 

	.. _`ArrayFunctions`: https://imagej.net/macros/examples/ArrayFunctions.txt
	'''

	INCLUDE_EDGES = 0
	EXLUDE_EDGES = 1
	CIRCULAR_ARRAY = 2
	NO_WINDOW = "none"
	HAMMING = "Hamming"
	HANN = "Hann"
	FLAT_TOP = "flat-top"
	
	@classmethod 
	def concat(cls, *args):
		'''
		Returns a new array created by joining two or more arrays or values (examples_). 

		.. _`examples`: https://imagej.net/macros/examples/ArrayConcatExamples.txt
		'''
		result = list()
		for arrayOrElement in args:
			if isinstance(arrayOrElement, list):
				current = arrayOrElement
			else:
				current = list()
				current.append(arrayOrElement)
			result = result + current
		return result

	@classmethod
	def copy(cls, aList):
		'''
		Returns a copy of array. 
		'''
		return list(aList)

	@classmethod
	def deleteValue(cls, array, value):
		'''
		Returns a version of array where all numeric or string elements in the array that contain 
		value have been deleted (examples_). 
		
		Requires 1.52o. 

		.. _`examples`: https://imagej.net/macros/examples/ArrayDeleteDemo.txt
		'''
		filtered = [x for x in array if x!=value]
		return filtered

	@classmethod
	def deleteIndex(cls, array, index):
		'''
		Returns a version of array where the element with the specified index has been deleted. 
		
		Requires 1.52o. 
		'''
		a1 = array[0:index]
		a2 = array[index+1:len(array)]
		return  a1 + a2

	@classmethod
	def fill(cls, array, value):
		'''
		Assigns the specified numeric value to each element of array. 
		'''
		for i in range(0, len(array)):
			array[i] = value
		return array
		
	@classmethod
	def findMaxima(cls, array, tolerance, edgeMode=EXLUDE_EDGES):
		'''
		Returns an array holding the peak positions (sorted with descending strength). 
		
		'Tolerance' is the minimum amplitude difference needed to separate two peaks. 
		With v1.51n and later, there is an optional 'edgeMode' argument: 
		0=include edges, 1=exclude edges(default), 2=circular array. `Examples`_.

		.. _`Examples`: https://imagej.net/macros/examples/FindMaxima1D.txt
		'''
		maxima = MaximumFinder.findMaxima(array, tolerance, edgeMode)
		return maxima

	@classmethod
	def findMinima(cls, array, tolerance, edgeMode=EXLUDE_EDGES):
		'''
		Returns an array holding the minima positions. 
		'''
		minima = MaximumFinder.findMinima(array, tolerance, edgeMode)
		return minima

	@classmethod
	def fourier(cls, array, windowType=NO_WINDOW):
		'''
		Calculates and returns the Fourier amplitudes of array. 
		
		WindowType can be "none", "Hamming", "Hann", or "flat-top", 
		or may be omitted (meaning "none"). 
		
		See the `TestArrayFourier`_ macro for an example and more documentation. 

		.. _`TestArrayFourier`: https://imagej.net/macros/examples/TestArrayFourier.txt
		'''
		wt = [cls.NO_WINDOW, cls.HAMMING, cls.HANN, cls.FLAT_TOP].index(windowType)
		result = FHT().fourier1D(array, wt)
		return result

	@classmethod
	def getSequence(cls, n):
		'''
		 Returns an array containing the numeric sequence 0,1,2...n-1. 
		'''
		return range(n)

	@classmethod
	def getStatistics(cls, aList):
		'''
		Returns the min, max, mean, and stdDev of array, which must contain all numbers. 

		The ij-macro function takes output parameters. The ijmpy version only takes the list as
		parameter and returns the tupel of the calculated values (min, max, mean, stdDev). This
		means instead of 

			Array.getStatistics(anArray, min, max, mean, stddev)

		you have to write

			min, max, mean, stddev = Array.getStatistics(anArray)

		It could be implemented as  
		
			min, max, mean, stddev = Array.getStatistics(anArray, min, max, mean, stddev)

		But then 

			Array.getStatistics(anArray, min, max, mean, stddev)
		
		would silently fail.
		'''
		sum = sum2 = 0
		min = Double.POSITIVE_INFINITY;
		max = Double.NEGATIVE_INFINITY

		for value in aList:
			sum = sum + value
			sum2 = sum2 + (value*value)
			if value<min:
				min = value
			if value>max:
				max = value
		n = len(aList)
		mean = sum / float(n)
		stdDev = ((n*sum2)-(sum*sum))/float(n)
		stdDev = math.sqrt(stdDev / float(n-1))
		return min, max, mean, stdDev

	@classmethod
	def print(cls, aList):
		'''
		Prints the array on a single line.
		'''
		string = str(aList)
		string = string.replace('[', '').replace(']', '').replace("'", "")
		IJ.log(string)
		return string

	@classmethod
	def rankPositions(cls, array):
		'''
		Returns, as an array, the rank position indexes of array, starting with the index of the smallest value (`example`_). 

		.. _`example`: https://imagej.net/macros/examples/ArraySortingDemo.txt
		'''

		return Tools.rank(array)

	@classmethod
	def resample(cls, array, len):
		'''
		Returns an array which is linearly resampled to a different length.
		'''
		return Tools.resampleArray(array, len)

	@classmethod
	def reverse(cls, array):
		'''
		Reverses (inverts) the order of the elements in array. 

		Note that the method reverses the list passed as a parameter. For convenience it also
		returns the refernce to the list.
		'''
		return array.reverse()

	@classmethod
	def show(cls, *args):
		'''
		Displays one or more arrays in a Results window (`examples`_). 
		
		If title (optional) is "Results", the window will be the active Results window, otherwise, 
		it will be a dormant Results window (see also `IJ.renameResults`_). If title ends with "(indexes)", 
		a 0-based Index column is shown. If title ends with "(row numbers)", the row number column is shown. 

		.. _`examples`: https://imagej.net/macros/examples/ShowArrayDemo.txt
		.. _`IJ.renameResults`: https://imagej.net/developer/macro/functions.html#IJ.renameResults 
		'''

		if len(args)==0 or (len(args)==1 and not isinstance(args[0], list)):			#@TODO: refactor!!!
			raise Exception('Array show needs at least one array')

		title = "Arrays"
		if len(args)==1 or (len(args)==2 and isinstance(args[0], str)):					# one array with or without title
			if isinstance(args[0], str):
				title = args[0]
				array = args[1]
			else:
				title = __getNameOfArg(args[0])
				array = args[0]
			column = "Value"
			indexes = False;
			rowNumbers = False;
			if title.find('(indexes)')>=0:
				indexes = True
				title = title.replace('(indexes)', '').strip()
			if title.find('(row numbers)')>=0:
				rowNumbers = True
				title = title.replace('(row numbers)', '').strip()
			if (indexes): 
				rt.showRowNumbers(False)	
				rt.showRowIndexes(True)
			if (rowNumbers): 
				rt.showRowIndexes(False)
				rt.showRowNumbers(True)	
			if (title.lower()=='results'):
				rt = Analyzer.getResultsTable()
			else:
				rt = ResultsTable()
			for value in array:
				rt.incrementCounter()
				rt.addValue(column, value)
			rt.show(title)
			return rt
			
		indexes = False											# More than one array
		rowNumbers = False
		if (isinstance(args[0], str)):
			title = args[0]
			if title.find('(indexes)')>=0:
				indexes = True
				title = title.replace('(indexes)', '').strip()
			if title.find('(row numbers)')>=0:
				rowNumbers = True
				title = title.replace('(row numbers)', '').strip()
		if (title.lower()=='results'):
			rt = Analyzer.getResultsTable()
		else:
			rt = ResultsTable()
		isFirstColumn = True;
		for array in args:
			if isinstance(array, str):
				continue
			row = 0	
			for value in array:
				column = __getNameOfArg(array)
				if (isFirstColumn):
					rt.incrementCounter()
					rt.addValue(column, value)
				else:
					rt.setValue(column, row, value)
					row = row + 1
			isFirstColumn = False
		if (indexes): 
			rt.showRowNumbers(False)	
			rt.showRowIndexes(True)
		if (rowNumbers): 
			rt.showRowIndexes(False)
			rt.showRowNumbers(True)	
		rt.show(title)
		return rt

	@classmethod
	def slice(cls, array, start, stop=None):
		'''
		Extracts a part of an array and returns it. (`examples`_).

		.. _`examples`: https://imagej.net/macros/examples/ArraySliceExamples.txt
		'''
		if (stop is None):
			stop = len(array)
		return array[start:stop]

	@classmethod
	def sort(cls, array):
		'''
		Sorts array, which must contain all numbers or all strings. String sorts are case-insensitive in v1.44i or later. 
		'''
		if (len(array)==0):
			return array
		if (isinstance(array[0],  str)):
			return array.sort(key=lambda y: y.lower())
		return array.sort()

	@classmethod
	def trim(cls, array, n):
		'''
		Returns an array that contains the first n elements of array. 
		'''
		return array[:n]

	@classmethod
	def rotate(cls, array, d):
		'''
		Rotates the array elements by 'd' steps (positive 'd' = rotate right). Requires 1.51n. `Examples`_. 

		.. _`Examples`: https://imagej.net/macros/examples/RotateArray.txt
		'''
		if len(array) == 0:
			return array
		rotated = deque(array) 
		rotated.rotate(d)
		for i in range(0, len(array)):
			array[i] = rotated[i]
		return array 

	@classmethod
	def getVertexAngles(cls, xArr, yArr, arm):
		'''
		From a closed contour given by 'xArr', 'yArr', an array is returned holding vertex angles in degrees 
		(straight=0, convex = positive if contour is clockwise). 
		
		Set 'arm'=1 to calculate the angle from the closest vertex points left and right, or use arm>1 for 
		more distant neighbours and smoother results. Requires 1.51n. `Examples`_.

		.. _`Examples`: https://imagej.net/macros/examples/VertexAngles.txt
		'''
		if len(xArr)!=len(yArr):
			raise Exception('Same size expected')
		length = len(xArr)
		vAngles = [0]*length
		x = xArr
		y = yArr
		for mid in range(0, length):
			left = (mid + 10 * length - arm) % length
			right = (mid + arm) % length
			dotprod = (x[right] - x[mid]) * (x[left] - x[mid]) + (y[right] - y[mid]) * (y[left] - y[mid])
			crossprod = (x[right] - x[mid]) * (y[left] - y[mid]) - (y[right] - y[mid]) * (x[left] - x[mid])
			phi = 180.0 - 180.0 / math.pi * math.atan2(crossprod, dotprod)
			while phi >= 180.0:
				phi -= 360.0
			vAngles[mid] = phi
		return vAngles

def asin(n):
	'''
	Returns the inverse sine (in radians) of n.
	'''
	return math.asin(n)

def atan(n):
	'''
	Calculates the inverse tangent (arctangent) of n. 
	
	Returns a value in the range -PI/2 through PI/2. 
	'''
	return math.atan(n)

def atan2(y, x):
	'''
	Calculates the inverse tangent of y/x and returns an angle in the range -PI to PI, 
	using the signs of the arguments to determine the quadrant. 
	
	Multiply the result by 180/PI to convert to degrees. 
	'''
	return math.atan2(y, x)

def autoUpdate(aBoolean):
	'''
	If boolean is true, the display is refreshed each time lineTo(), drawLine(), drawString(), etc. are called,
	otherwise, the display is refreshed only when updateDisplay() is called or when the macro terminates. 
	'''
	global AUTO_UPDATE
	AUTO_UPDATE = aBoolean
	
def isAutoUpdate():
	'''
	Returns true if auto-update is active and false otherwise.
	'''
	global AUTO_UPDATE
	return AUTO_UPDATE

def beep():
	'''
	Emits an audible beep.
	'''
	IJ.beep()

def bitDepth():
	'''
	Returns the bit depth of the active image: 8, 16, 24 (RGB) or 32 (float). 
	'''
	return IJ.getImage().getBitDepth()

def calibrate(value):
	'''
	Uses the calibration function of the active image to convert a raw pixel value to a density calibrated value. 
	
	The argument must be an integer in the range 0-255 (for 8-bit images) or 0-65535 (for 16-bit images). 
	Returns the same value if the active image does not have a calibration function. 
	'''
	cValue = IJ.getImage().getCalibration().getCValue(value)
	return cValue

def call(classAndMethodName, *args):
	'''
	Calls a public static method in a Java class, passing an arbitrary number of string arguments, and returning a string. 
	
	Refer to the `CallJavaDemo`_ macro and the `ImpProps`_ plugin for examples. 

	.. _`CallJavaDemo`: https://imagej.net/macros/CallJavaDemo.txt
	.. _`ImpProps`: https://imagej.net/plugins/imp-props.html
	'''
	index = classAndMethodName.rfind('.')
	className = classAndMethodName[0:index]
	methodName = classAndMethodName[index+1:len(classAndMethodName)]
	aClass = importlib.import_module(className)
	res = getattr(aClass, methodName)(*args)
	return res

def changeValues(low, high, newValue):
	'''
	Changes pixels in the image or selection that have a value in the range v1-v2 to v3. 
	
	For example, changeValues(0,5,5) changes all pixels less than 5 to 5, and changeValues(0x0000ff,0x0000ff,0xff0000) 
	changes all blue pixels in an RGB image to red. 
	
	In ImageJ 1.52d or later, use changeValues(NaN,NaN,value) to replaces NaN values. 
	'''
	image = IJ.getImage()
	ip = image.getProcessor()
	roi = image.getRoi()
	width = image.getWidth()
	height = image.getHeight()
	isFloat = image.getBitDepth()==32
	if image.getBitDepth()==24: 
		low = int(low&0xffffff)
		high = int(high&0xffffff)
	if roi is None:
		roi = Roi(0,0,width,height)
	replaceNaN = False
	if Double.isNaN(low) and Double.isNaN(high):
		replaceNaN = True
	for p in roi:
		if isFloat:
			value = ip.getPixelValue(p.x,p.y)
		else:
			value = ip.getPixel(p.x,p.y)&0xffffff;
		if (value>=low and value<=high) or replaceNaN:
			if isFloat:
				ip.putPixelValue(p.x, p.y, newValue)
			else:
				ip.putPixel(p.x, p.y, int(newValue));
	image.updateAndDraw()

def charCodeAt(aString, index):
	'''
	Returns the Unicode value of the character at the specified index in string. 
	
	Index values can range from 0 to lengthOf(string). 
	Use the fromCharCode() function to convert one or more Unicode characters to a string.
	'''
	if index<0 or index>len(aString)-1:
		raise Exception("Index ("+str(index)+") is outside of the "+str(0)+"-"+str(len(aString)-1)+" range")
	uString = aString.decode("utf-8")
	ch = uString[index]
	return ord(ch)	

def close(pattern=""):
	'''
	Closes the active image. 
	
	This function has the advantage of not closing the "Log" or "Results" window when you meant 
	to close the active image. Use run("Close") to close non-image windows.
	
	close(pattern)
		Closes windows whose title matches 'pattern', which can contain the wildcard characters '*' (matches any character sequence)
		and '?' (matches single character). For example, close("Histo*") could be used to dispose all histogram windows. 
		Non-image windows like "Roi Manager" have to be specified without wildcards. For text windows, wildcards are allowed if 
		'pattern' ends with ".txt", ".ijm", ".js" etc. Use close("*") to close all image windows. Use close(pattern, "keep") 
		to not close text or image windows with changes. If 'pattern' is "\\Others", all images except the front image are closed. 
		The most recent macro window is never closed.
	
	close("*")
		Closes all image windows.
	
	close("\\Others")
		Closes all images except for the front image. 
	'''
	if (pattern==""):
		value = IJ.runMacro("close();")
	else:	
		macro = 'close("'+pattern+'")'
		value = IJ.runMacro(macro)
	return value

def cos(angle):
	'''
	Returns the cosine of an angle (in radians). 
	'''
	return math.cos(angle)

def d2s(n, decimalPlaces):
	'''
	Converts the number n into a string using the specified number of decimal places. 
	
	Uses scientific notation if 'decimalPlaces is negative. Note that d2s stands for "double to string". 

	Note: In python 2 the division a/b is an integer division. To use float division make one of the operands a float, or 
	change the general behaviour with 
	
		from __future__ import division
	'''
	return IJ.d2s(n, decimalPlaces)

def debug(arg):
	'''
	Start debugging.
	
	We can't use the ij-debugger for python. Call pdb instead, but this will only
	work when running from an interactive shell not from the editor.
	'''
	import pdb; pdb.set_trace()

class Dialog:
	'''
	Dialog.create(title) creates a modal dialog box with the specified title, or use Dialog.createNonBlocking("Title") to create a non-modal dialog. 
	
	Call Dialog.addString(), Dialog.addNumber(), etc. to add components to the dialog. Call Dialog.show() to display the dialog 
	and Dialog.getString(), Dialog.getNumber(), etc. to retrieve the values entered by the user. 
	
	Refer to the `DialogDemo`_ macro for an example.

	.. _`DialogDemo`: https://imagej.net/macros/DialogDemo.txt
	'''
	GD = None

	@classmethod
	def create(cls, title):
		'''
		Creates a modal dialog box with the specified title.
		'''
		cls.GD = GenericDialog(title)
		return cls.GD

	@classmethod
	def createNonBlocking(cls, title):
		'''
		Creates a non-modal dialog box with the specified title.
		'''
		cls.GD = NonBlockingGenericDialog(title)
		return cls.GD

	@classmethod
	def addMessage(cls, string, fontSize=None, fontColor=None):
		'''
		Adds a message to the dialog using a specified font size and color (`example`_). 

		The message can be broken into multiple lines by inserting new line characters ("\\n") into the string. 
		The 'fontSize' and 'fontColor' arguments are optional. Requires 1.52q. 

		.. _`example`: https://imagej.net/macros/examples/DialogMessageDemo.txt
		'''
		if (fontSize is None):
			cls.GD.addMessage(string)
			return cls.GD
		font = Font("SansSerif", Font.PLAIN, int((fontSize*Prefs.getGuiScale())));	
		if (fontColor is None):
			cls.GD.addMessage(string, font)
			return cls.GD
		color = Colors.decode(fontColor, Color.BLACK)
		cls.GD.addMessage(string, font, color)
		return cls.GD

	@classmethod
	def addString(cls, label, initialText, columns=8):
		'''
		Adds a text field to the dialog, where *columns* specifies the field width in characters. 
		'''
		cls.GD.addStringField(label, initialText, columns)
		return cls.GD
	
	@classmethod
	def show(cls):
		'''
		Displays the dialog and waits until the user clicks "OK" or "Cancel". 
		
		In ij the macro terminates if the user clicks "Cancel". This doesn't work in ijmpy.
		This means the variables will be set to the default values even if the user cancels 
		the dialog. To avoid this, use: 

			if  not Dialog.show().wasCanceled():
				name = Dialog.getString();
				...
				
		'''
		cls.GD.showDialog()
		return cls.GD

	@classmethod
	def getString(cls):
		'''
		Returns a string containing the contents of the next text field. 
		'''
		return cls.GD.getNextString();
		
def getPixel(x, y=None):
	'''
	Returns the raw value of the pixel at (x,y). 
	
	Uses bilinear interpolation if 'x' or 'y' are not integers. 
	Use getValue(x,y) to get calibrated pixel values from 8 and 16 bit images and intensity values from RGB images. 
	Note that pixels in RGB images contain red, green and blue components that need to be extracted using shifting and masking. 
	
	See the `Color Picker Tool`_ macro for an example that shows how to do this. 

	.. _`Color Picker Tool`: https://imagej.net/macros/tools/ColorPickerTool.txt
	'''
	imp = IJ.getImage()
	ip = imp.getProcessor()
	if y is not None: 
		if isinstance(x, int) and isinstance(y, int):
			if isinstance(ip, FloatProcessor):
				value = ip.getPixelValue(x,y)
			else:
				value = ip.getPixel(x,y)
		else:
			if isinstance(ip, ColorProcessor):
				ip.getPixelInterpolated(x, y)
			else:
				cal = imp.getCalibration();
				imp.setCalibration(None);
				value = ip.getInterpolatedValue(x, y);
				imp.setCalibration(cal);
	else:
		if isinstance(ip, ColorProcessor):
			value = ip.get(int(x))
		else:
		 	value = ip.getf(int(x))
	return value

def getThreshold():
	'''
	Returns the lower and upper threshold levels. 
	
	Both variables are set to -1 if the active image is not thresholded. 
	
	The function has no parameters and returns a tupel. This is different from the ij-macro function which has two result parameters.

	See also: 
	=========
	setThreshold, resetThreshold
	'''
	image = IJ.getImage()
	processor = image.getProcessor()
	t1 = processor.getMinThreshold()
	t2 = processor.getMaxThreshold()
	return t1, t2

def lengthOf(aListOrString):
	'''
	Returns the length of a string or array. 
	Can be replaced with str.length (1.52t or later) or arr.length in ijm but not in ijmpy.
	Use lengthOf(a) or len(a) instead of a.length. 
	'''
	return len(aListOrString)
	
def newArray(*args):
	'''
	Returns a new array containing size elements. You can also create arrays by listing the elements, for example newArray(1,4,7) or 
	newArray("a","b","c"). For more examples, see the Arrays_ macro.
	
	The ImageJ macro language does not directly support 2D arrays. Use python lists instead.

	ijmpy uses python lists as arrays. The macro code a.length will not work. Use either the ijm-command lengthOf(a) or the python 
	command len(a) instead.

	The newArray-function is here for compability with ij-macros. Consider using python lists directly.
	
	.. _Arrays: https://imagej.net/macros/Arrays.txt
	'''
	if len(args)==1 and isinstance(args[0], int):
		return [0] * args[0]
	return list(args)

def newImage(title, imageType, width, height, depthOrChannels, depth=1, frames=1):
	'''
	Opens a new image or stack using the name title. 
	
	The string type should contain "8-bit", "16-bit", "32-bit" or "RGB". 
	In addition, it can contain "white", "black" or "ramp" (the default is "white"). 
	As an example, use "16-bit ramp" to create a 16-bit image containing a grayscale ramp. 
	Precede with call("ij.gui.ImageWindow.setNextLocation", x, y) to set the location of the new image. 
	Width and height specify the width and height of the image in pixels. Depth specifies the number of stack slices. 
	'''
	if depth==1 and frames ==1:
		image = IJ.createImage(title, imageType, width, height, depthOrChannels)
	else:
		image = IJ.createImage(title, imageType, width, height, depthOrChannels, depth, frames)
	image.show()
	return image

def nImages():
	'''
	Returns number of open images. 
	
	The parentheses "()" are optional in the ij-macro language but *not* in ijmpy. 
	'''
	return WindowManager.getImageCount()
	
def roiManager(command, parameter=""):
	'''
	These function run ROI Manager commands. 
	
	The ROI Manager is opened if it is not already open. 
	Use roiManager("reset") to delete all ROIs on the list. 
	Use setOption("Show All", boolean) to enable/disable "Show All" mode. For examples, refer to the 
	`RoiManagerMacros`_, 
	`ROI Manager Stack Demo`_ and 
	`RoiManagerSpeedTest`_ macros.

	.. _`RoiManagerMacros`: https://imagej.net/macros/RoiManagerMacros.txt
	.. _`ROI Manager Stack Demo`: https://imagej.net/macros/ROI_Manager_Stack_Demo.txt
	.. _`RoiManagerSpeedTest`: https://imagej.net/macros/RoiManagerSpeedTest.txt
	
	roiManager("and")
		Uses the conjunction operator on the selected ROIs, or all ROIs if none are selected, to create a composite selection.

	roiManager("add")
		Adds the current selection to the ROI Manager.
	
	roiManager("add & draw")
		Outlines the current selection and adds it to the ROI Manager.
	
	roiManager("combine")
		Uses the union operator on the selected ROIs to create a composite selection. Combines all ROIs if none are selected.
	
	roiManager("count")
		Returns the number of ROIs in the ROI Manager list.
	
	roiManager("delete")
		Deletes the selected ROIs from the list, or deletes all ROIs if none are selected.
	
	roiManager("deselect")
		Deselects all ROIs in the list. When ROIs are deselected, subsequent ROI Manager commands are applied to all ROIs.
	
	roiManager("draw")
		Draws the selected ROIs, or all ROIs if none are selected, using the equivalent of the Edit>Draw command.
	
	roiManager("fill")
		Fills the selected ROIs, or all ROIs if none are selected, using the equivalent of the Edit>Fill command.
	
	roiManager("index")
		Returns the index of the currently selected ROI on the list, or -1 if the list is empty or no ROIs are selected. 
		Returns the index of the first selected ROI if more than one is selected
	
	roiManager("measure")
		Measures the selected ROIs, or if none is selected, all ROIs on the list.
	
	roiManager("multi measure")
		Measures all the ROIs on all slices in the stack, creating a Results Table with one row per slice.
	
	roiManager("multi-measure append")
		Measures all the ROIs on all slices in the stack, appending the measurements to the Results Table, with one row per slice.
	
	roiManager("multi-measure one")
		Measures all the ROIs on all slices in the stack, creating a Results Table with one row per measurement.
	
	roiManager("multi plot")
		Plots the selected ROIs, or all ROIs if none are selected, on a single graph.
	
	roiManager("open", file-path)
		Opens a .roi file and adds it to the list or opens a ZIP archive (.zip file) and adds all the selections contained in it to the list.
	
	roiManager("remove slice info")
		Removes the information in the ROI names that associates them with particular stack slices.
	
	roiManager("rename", name)
		Renames the selected ROI. You can get the name of an ROI on the list using call("ij.plugin.frame.RoiManager.getName", index).
	
	roiManager("reset")
		Deletes all ROIs on the list.
	
	roiManager("save", file-path)
		Saves all the ROIs on the list in a ZIP archive.
	
	roiManager("save selected", file-path)
		Saves the selected ROI as a .roi file.
	
	roiManager("select", index)
		Selects an item in the ROI Manager list, where index must be greater than or equal zero and less than the value returned by roiManager("count"). 
		Note that macros that use this function sometimes run orders of magnitude faster in batch mode. Use roiManager("deselect") to deselect all 
		items on the list. 
		For an example, refer to the `ROI Manager Stack Demo`_ macro.
	
	roiManager("select", indexes)
		Selects multiple items in the ROI Manager list, where indexes is an array of integers, each of which must be greater than or equal to 0 and 
		less than the value returned by roiManager("count"). The selected ROIs are not highlighted in the ROI Manager list and are no longer selected 
		after the next ROI Manager command is executed.
	
	roiManager("show all")
		Displays all the ROIs as an overlay.
	
	roiManager("show all with labels")
		Displays all the ROIs as an overlay, with labels.
	
	roiManager("show all without labels")
		Displays all the ROIs as an overlay, without labels.
	
	roiManager("show none")
		Removes the ROI Manager overlay.
	
	roiManager("sort")
		Sorts the ROI list in alphanumeric order.
	
	roiManager("split")
		Splits the current selection (it must be a composite selection) into its component parts and adds them to the ROI Manager.
	
	roiManager("update")
		Replaces the selected ROI on the list with the current selection.
	'''
	if (command.lower().strip()=='count'):
		return RoiManager.getRoiManager().getCount()
	if (command.lower().strip()=='index'):
		return RoiManager.getRoiManager().getSelectedIndex()
	if command.lower().strip()=='select' and isinstance(parameter, list):
		RoiManager.getRoiManager().setSelectedIndexes(parameter)
		return
	if parameter=="":
		IJ.runMacro('roiManager("'+command+'")')
	else:
		IJ.runMacro('roiManager("'+command+'",'+str(parameter)+')')
	return None
		
def run(command, parameters=""):
	'''
	Executes an ImageJ menu command. 
	
	The optional second argument contains values that are automatically entered into dialog boxes 
	(must be GenericDialog or OpenDialog). Use the Command Recorder (Plugins>Macros>Record) to generate run() function calls. 
	Use string concatenation to pass a variable as an argument. 
	With ImageJ 1.43 and later, variables can be passed without using string concatenation by adding "&" to the variable name. 
	For examples, see the ArgumentPassingDemo_ macro.
	
	.. _ArgumentPassingDemo: https://imagej.net/macros/ArgumentPassingDemo.txt
	''' 
	if parameters=="":
		IJ.run(command)
	else:
		IJ.run(command, parameters)

def setAutoThreshold(method="Default"):
	'''
	Uses the specified method to set the threshold levels of the current image.
	
	It may select dark or bright areas as thresholded, 
	as was the case with the Image>Adjust>Threshold "Auto" option in ImageJ 1.42o and earlier. 

	Use the getList("threshold.methods") 
	function to get a list of the available methods. Concatenate " dark" to the method name if the image has a dark background. 
	For an example, see the `AutoThresholdingDemo`_ macro.

	.. _`AutoThresholdingDemo`: https://imagej.net/macros/examples/AutoThresholdingDemo.txt

	See also: 
	=========
	setThreshold, `getThreshold`_, resetThreshold

	.. _`getThreshold`: redirect.html#mripy.ijmpy.getThreshold
	'''
	image = IJ.getImage()
	IJ.setAutoThreshold(image, method)

def getWidth():
	'''
	Returns the width in pixels of the current image.
	'''
	image = IJ.getImage()
	return image.getWidth()

def print(text):
	'''
	For now just writes to the ImageJ-log window.
	'''
	IJ.log(text)

def __getNameOfArg(arg):
	'''
	Utility function to get the name of the variable that was passed as an argument 
	to the function.	
	'''
	import inspect
	name = None
	outerFrameLocals = inspect.currentframe().f_back.f_back.f_locals	
	for key in outerFrameLocals.keys():
		if id(outerFrameLocals[key])==id(arg):
			name = key
	return name

def example():
	'''
	An example of how to use the macro commands.
	'''
	run("Blobs (25K)");
	run("Invert");
	setAutoThreshold();
	close();