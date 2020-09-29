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

getArgument()
-------------

Not implemented, because it exists when called from a macro. Use:

	if 'getArgument' in globals():
		args = getArgument()

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
import math, sys, importlib, java, types, inspect, keyword, tokenize, os, subprocess, shutil, struct, urllib2
from collections import deque 
from java.lang import Double, String, Thread
from java.util import Calendar
from java.awt import Font, Color
from ij import IJ, WindowManager, Prefs
from ij.io import SaveDialog, OpenDialog
from ij.process import FloatProcessor, ColorProcessor, ImageProcessor, FloodFiller
from ij.plugin import Colors, Macro_Runner
from ij.plugin.frame import RoiManager, Fitter
from ij.plugin.filter import MaximumFinder, Analyzer
from ij.process import FHT
from ij.util import Tools
from ij.measure import ResultsTable, CurveFitter
from ij.gui import Roi, GenericDialog, NonBlockingGenericDialog, Toolbar, YesNoCancelDialog

NaN = Double.NaN
PI = math.pi
true = 1
false = 0

py_open = open
	
class Settings(object):
	AUTO_UPDATE = True
	UPDATE_NEEDED = False
	FONT = None
	JUSTIFICATION = ImageProcessor.LEFT_JUSTIFY
	ANTIALIASED_TEXT = False
	GLOBAL_COLOR = None
	FILE = None

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
	If boolean is true, the display is refreshed each time lineTo(), `drawLine()`_, `drawString()`_, etc. are called.
	
	Otherwise, the display is refreshed only when updateDisplay() is called or when the macro terminates. 

	.. _`drawLine()`: redirect.html#mripy.ijmpy.drawLine
	.. _`drawString()`: redirect.html#mripy.ijmpy.drawString
	'''
	Settings.AUTO_UPDATE = aBoolean
	
def isAutoUpdate():
	'''
	Returns true if auto-update is active and false otherwise.
	'''
	return Settings.AUTO_UPDATE

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

class Dialog(object):
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
	def addNumber(cls, label, default, decimalPlaces=None, columns=6, units=""):
		'''
		Adds a numeric field, using the specified label and default value. 
		
		DecimalPlaces specifies the number of digits to right of decimal point, columns specifies 
		the field width in characters and units is a string that is displayed to the right of the field. 
		'''
		if decimalPlaces is None:
			if isinstance(default, int):
				decimalPlaces = 0
			else:
				decimalPlaces = 3
		cls.GD.addNumericField(label, default, decimalPlaces, columns, units)
		return cls.GD

	@classmethod
	def addSlider(cls, label, minimum, maximum, default):
		'''
		Adds a slider controlled numeric field to the dialog, using the specified label, and min, max and default values (`example`_).
		
		Values with decimal points are used when (max-min)<=5 and min, max or default are non-integer.
		
		.. _`example`: https://imagej.net/macros/examples/SliderDemo.txt
		'''
		stepSize = 0.0
		if ((maximum - minimum) <= 5) and (isinstance(minimum, float) or isinstance(maximum, float) or isinstance(default, float)):
			stepSize = (maximum - minimum) / 100.0
		if stepSize is 0.0:
			cls.GD.addSlider(label, minimum, maximum, default)
		else:
			cls.GD.addSlider(label, minimum, maximum, default, stepSize)
		return cls.GD

	@classmethod
	def addCheckbox(cls, label, default):
		'''
		Adds a checkbox to the dialog, using the specified label and default state (true or false).
		'''
		if default:
			default = True
		else:
			default = False
		cls.GD.addCheckbox(label, default)
		return cls.GD

	@classmethod
	def addCheckboxGroup(cls, rows, columns, labels, defaults):
		'''
		Adds a rowsxcolumns grid of checkboxes to the dialog, using the specified labels and default states (`example`_). 

		.. _`example`: https://imagej.net/macros/AddCheckboxGroupDemo.txt
		
		if not len(labels) is len(defaults):
			raise Exception('labels.length!=states.length')
		
		cls.GD.addCheckboxGroup(rows, columns, labels, defaults)
		return cls.GD
		'''
		if not len(labels) is len(defaults):
			raise Exception('labels.length!=states.length')
		states = [aBool and True for aBool in defaults]
		cls.GD.addCheckboxGroup(rows, columns, labels, states)
		return cls.GD

	@classmethod
	def addRadioButtonGroup(cls, label, items, rows, columns, default):
		'''
		Adds a group of radio buttons to the dialog.
		
		'label' is the group label, 'items' is an array containing the button labels, 
		'rows' and 'columns' specify the grid size, and 'default' is the label of the default button. (`example`_).

		.. _`example`: https://imagej.net/macros/examples/RadioButtonDemo.txt 
		'''

		cls.GD.addRadioButtonGroup(label, items, rows, columns, default)
		return cls.GD

	@classmethod
	def addChoice(cls, label, items, default=None):
		'''
		Adds a popup menu.
		
		items is a string array containing the choices and default is the default choice. 
		'''

		if default==None:
			default = items[0]
		cls.GD.addChoice(label, items, default)
		return cls.GD

	@classmethod
	def addHelp(cls, urlOrHTML):
		'''
		Adds a "Help" button that opens the specified URL in the default browser. 
		 
		This can be used to supply a help page for this dialog or macro. With v1.46b or later, 
		displays an HTML formatted message if 'url' starts with "<html>" (`example`_). 

		.. _`example`: https://imagej.net/macros/examples/DialogWithHelp.txt
		'''
		cls.GD.addHelp(urlOrHTML)
		return cls.GD

	@classmethod
	def addToSameRow(cls):
		'''
		Makes the next item added appear on the same row as the previous item. 
		
		May be used for addNumericField, addSlider, addChoice, addCheckbox, addString, addMessage, 
		and before the showDialog() method. In the latter case, the buttons appear to the right of 
		the previous item. 
		
		Note that addMessage (and addString if a width of more than 8 is specified) use the remaining width, 
		so it must be the last item of a row. Requires 1.51r. 
		'''	
		cls.GD.addToSameRow()
		return cls.GD

	@classmethod
	def setInsets(cls, top, left, bottom):
		'''
		Overrides the default insets (margins) used for the next component added to the dialog.

		Default insets:
		
			addMessage: 0,20,0 (empty string) or 10,20,0
			addCheckbox: 15,20,0 (first checkbox) or 0,20,0
			addCheckboxGroup: 10,0,0
			addNumericField: 5,0,3 (first field) or 0,0,3
			addStringField: 5,0,5 (first field) or 0,0,5
			addChoice: 5,0,5 (first field) or 0,0,5
			
		'''
		cls.GD.setInsets(top, left, bottom)
		return cls.GD

	@classmethod
	def setLocation(cls, x, y):
		'''
		Sets the screen location where this dialog will be displayed.
		'''
		cls.GD.setLocation(x, y)
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
		return cls.GD.getNextString()

	@classmethod
	def getNumber(cls):
		'''
		Returns the contents of the next numeric field. 
		'''
		return cls.GD.getNextNumber()
		
	@classmethod
	def getCheckbox(cls):
		'''
		Returns the state (true or false) of the next checkbox. 
		'''
		if cls.GD.getNextBoolean():
			return true
		else:
			return false

	@classmethod
	def getRadioButton(cls):
		'''
		Returns the selected item (a string) from the next radio button group. 
		'''
		return cls.GD.getNextRadioButton()

	@classmethod
	def getChoice(cls):
		'''
		 Returns the selected item (a string) from the next popup menu. 
		'''
		return cls.GD.getNextChoice()

def doCommand(command):
	'''
	Runs an ImageJ menu command in a separate thread and returns immediately. 
	
	As an example, doCommand("Start Animation") starts animating the current stack in a separate thread 
	and the macro continues to execute. Use run("Start Animation") and the macro hangs until the user stops the animation. 
	'''
	if command == "Start Animation":
		command = "Start Animation [\\]"
	IJ.doCommand(command)

def doWand(x, y, tolerance=0, mode=None):
	'''
	Equivalent to clicking on the current image at (x,y) with the wand tool. 
	
	Note that some objects, especially one pixel wide lines, may not be reliably traced unless they have been 
	thresholded (highlighted in red) using setThreshold. 
	Traces the boundary of the area with pixel values within `tolerance` of the value of the pixel at (x,y). 
	`mode` can be "4-connected", "8-connected" or "Legacy". "Legacy" is for compatibility with previous versions of ImageJ; 
	it is ignored if "tolerance > 0". If `mode` contains "smooth", the contour is smoothed by interpolation (`example`_). 

	.. _`example`: https://imagej.net/macros/examples/SmoothLetters.txt
	'''
	IJ.doWand(x, y, tolerance, mode)
	return IJ.getImage().getRoi()

def drawLine(x1, y1, x2, y2):
	'''
	Draws a line between (x1, y1) and (x2, y2). 
	
	Use setColor() to specify the color of the line and setLineWidth() to vary the line width. 
	
	See also:
	=========
	Overlay.drawLine
	''' 
	imp = IJ.getImage()
	imp.getProcessor().drawLine(x1, y1, x2, y2)
	__updateAndDraw()
	return imp

def drawOval(x, y, width, height):
	'''
	Draws the outline of an oval using the current color and line width. 
	
	See also: 
	=========
	`fillOval`_, setColor, setLineWidth, `autoUpdate`_ and Overlay.drawEllipse. 

	.. _`fillOval`: redirect.html#mripy.ijmpy.fillOval
	.. _`autoUpdate`: redirect.html#mripy.ijmpy.autoUpdate
	'''
	imp = IJ.getImage()
	imp.getProcessor().drawOval(x, y, width, height)
	__updateAndDraw()
	return imp

def drawRect(x, y, width, height):
	'''
	Draws the outline of a rectangle using the current color and line width. 
	
	See also: 
	=========
	`fillRect`_, setColor, setLineWidth, `autoUpdate`_ and Overlay.drawRect 

	.. _`fillRect`: redirect.html#mripy.ijmpy.fillRect
	.. _`autoUpdate`: redirect.html#mripy.ijmpy.autoUpdate
	'''
	imp = IJ.getImage()
	imp.getProcessor().drawRect(x, y, width, height)
	__updateAndDraw()
	return imp

def drawString(aText, x, y, background=None):
	'''
	Draws text at the specified location with a filled background. 

	The first character is drawn obove and to the right of (x,y). Call setFont() to specify the font. 
	Call setJustification() to have the text centered or right justified. Call getStringWidth() to get 
	the width of the text in pixels. Refer to the TextDemo macro for examples and to DrawTextWithBackground 
	to see how to draw text with a background. 
	'''
	ip = IJ.getImage().getProcessor()
	if not Settings.FONT is None:
		ip.setFont(Settings.FONT)
	ip.setJustification(Settings.JUSTIFICATION);
	ip.setAntialiasedText(Settings.ANTIALIASED_TEXT)
	if not background is None:
		aColor = __getColor(background)
		ip.drawString(aText, x, y, aColor)
	else:
		if not Settings.GLOBAL_COLOR is None:
			ip.setColor(Settings.GLOBAL_COLOR)
		else:
			ip.setColor(Toolbar.getForegroundColor())
		ip.drawString(aText, x, y)
	__updateAndDraw()

def dump():
	'''
	Writes the contents of the symbol table, the tokenized script code and the variable stack to the "Log" window. 
	
	In ijmpy you need to save the script before creating a dump.
	'''
	bfuncs = [name for name, function in sorted(vars(__builtin__).items()) if inspect.isbuiltin(function) or inspect.isfunction(function)]
	locs = inspect.currentframe().f_back.f_globals
	keys = locs.keys()
	wantedKeys = []
	for key in keys:
		if type(locs[key]) in [types.TypeType, types.FunctionType]:
			wantedKeys.append(key)
	all = keyword.kwlist + bfuncs +wantedKeys
	all.sort()
	index = 0
	print("\nSymbol Table")
	for name in all:
		print(str(index) + " " +name)
		index = index + 1

	globs = inspect.currentframe().f_back.f_globals
	i = 1
	keys = globs.keys()
	wantedKeys = []
	for key in keys:
		if key in ['__builtin__', '__builtins__', 'java'] or type(globs[key]) in [java.lang.Class, type, types.FunctionType, types.InstanceType, types.ModuleType]:
			continue
		else:
			wantedKeys.append(key)
	wantedKeys.reverse()

	print ("\nTokenized Program")
	tokens = []
	def cons(*args):
		name = args[1]
		if name=='\n':
			name = '\\n'
		tokens.append(str(args[2][0]) +', '+ str(args[2][1]) + ' - ' + str(args[3][0]) + ', ' + str(args[3][1]) + " " + "'" +name + "'")
		
	filename = globs['javax.script.filename']
	result = 'You need to save the script to get the tokens.'
	if os.path.isfile(filename): 
		with py_open(filename, 'r') as myfile:
			tokenize.tokenize(myfile.readline, cons)
	
		for token in tokens:
			print(token)
			
	if len(tokens)==0:
		print(result)
	
	print('\nStack')
	for key in wantedKeys:
		print(len(wantedKeys)-i, key + ' = ' + str(globs[key]))
		i = i + 1

def endsWith(string, suffix):
	'''
	Returns True if string ends with suffix. 
	
	See also: 
	=========
	startsWith, indexOf, substring, matches. 
	'''
	return string.endswith(suffix)

def eval(macroOrLang, argsOrScript=None):
	'''
	Evaluates (runs) one or more lines of macro code. 
	
	An optional second argument can be used to pass a string to the macro being evaluated. 
	
	eval("script", javascript)
		Evaluates the JavaScript code contained in the string javascript and returns, as a string, 
		the value of the last statement executed. 
		For example eval("script","IJ.getInstance().setAlwaysOnTop(true);"). 
		See also: runMacro(path,arg).
	
	eval("js", script)
		Evaluates the JavaScript code contained in the string script and returns, as a string, 
		the value of the last statement executed. For example eval("js","Prefs.blackBackground") 
		returns either "true" or "false".
	
	eval("bsh", script)
		Evaluates the BeanShell code contained in the string script.
	
	eval("python", script)
		Evaluates the Python code contained in the string script. 

	See also: 
	=========
	`EvalDemo`_ macro and runMacro function.

	.. _`EvalDemo`: https://imagej.net/macros/EvalDemo.txt

	'''
	if macroOrLang == "script" or macroOrLang == "js":
		return Macro_Runner().runJavaScript(argsOrScript, "")

	if macroOrLang == "bsh":
		return Macro_Runner.runBeanShell(argsOrScript, "")

	if macroOrLang == "python":
		return Macro_Runner.runPython(argsOrScript, "")

	return IJ.runMacro(macroOrLang, argsOrScript);

def Exec(*args):
	'''
	Executes a native command and returns the output of that command as a
	string. 
	
	Also opens Web pages in the default browser and documents in
	other applications (e.g., Excel). With commands with multiple arguments,
	each argument should be passed as a separate string. For example
	exec("open", "/Users/wayne/test.jpg", "-a", "/Applications/Gimp.app");
	Refer to the `ExecExamples`_ macro for examples.

	It doesn't seem to be possible to override the python keyword echo, although it
	seemed to have worked for eval. For now use "Exec", but this is likely to change.
	
	.. _`ExecExamples`: <@TODO>
	'''
	out = subprocess.check_output(list(args))
	return out

def exit(message=None, **kargs):
	'''
	Terminates execution of the script and displays an error message.

	In ijmpy you can specify an exit status, for example:

		exit(status=0)
		
	'''
	if not message == None:
		IJ.showMessage('Script', message)
	# raise SystemExit
	if 'status' in kargs:
		sys.exit(kargs['status'])
	else:
		sys.exit()

def exp(n):
	'''
	Returns the exponential number e (i.e., 2.718...) raised to the power of n.
	'''
	return math.exp(n)

class ExtMeta(type):
	'''
	Handle a priori unknown calls to Ext.
	'''
	def __getattr__(self, name):
		return lambda *args: self.handleCall(name, *args) 	

	def handleCall(self, method, *args):
		if method == 'install':
			parts = args[0].split('.')
			module = '.'.join(parts[0:len(parts)-1])
			pluginName = parts[-1]
			print(module, pluginName)
			cls = getattr(importlib.import_module(module), pluginName)
			self.plugin = cls()
			if not self.plugin:
				raise Exception('Plugin not found')
		else:
			descriptorList = self.plugin.getExtensionFunctions()
			functions = [desc.name for desc in descriptorList]
			if not method in functions:
				raise Exception('Unrecognized Ext function') 
			res = self.plugin.handleExtension(method, list(args))
			return res

class Ext(object):
	'''
	Implements the (Macro Extension) Functions handling.
	
	These are functions that have been added to the macro language by
	plugins using the MacroExtension interface. The Image5D_Extensions
	plugin, for example, adds functions that work with Image5D. The Serial
	Macro Extensions plugin adds functions, such as Ext.open("COM8",9600,"")
	and Ext.write("a"), that talk to serial devices.
	'''
	__metaclass__ = ExtMeta

class FileMeta(type):

	@property
	def directory(self):
		'''
		The directory path of the last file opened using a file open dialog, a file save dialog, drag and drop, open(path) or runMacro(path).
		'''
		lastDir = OpenDialog.getLastDirectory()
		result = lastDir if lastDir else "" 
		return result

	@property
	def name(self):
		'''
		The name of the last file opened using a file open dialog, a file save dialog, drag and drop, or the open(path) function.
		'''
		lastName = OpenDialog.getLastName()
		result = lastName if lastName else "" 
		return result

	@property
	def nameWithoutExtension(self):
		'''
		The name of the last file opened with the extension removed.		
		'''
		lastName = OpenDialog.getLastName()
		result = lastName if lastName else "" 
		parts = result.split('.')
		result = '.'.join(parts[0:len(parts)-1])
		return result

	@property
	def separator(cls):
		'''
		Returns the file name separator character ("/" or "\").
		'''
		return os.path.sep
		
class File(object):
	'''
	These functions allow you to get information about a file, read or write a text file, create a directory, 
	or to delete, rename or move a file or directory. 
	
	Note that these functions return a string, with the exception of File.length, File.exists, File.isDirectory, 
	File.rename and File.delete when used in an assignment statement, 	for example "length=File.length(path)". 
	The `FileDemo`_ macro demonstrates how to use these functions. 
	
	See also:
	=========
	getDirectory and getFileList. 

	.. _`FileDemo`: https://imagej.net/macros/FileDemo.txt
	'''
	__metaclass__ = FileMeta
	@classmethod
	def append(cls, string, path):
		'''
		Appends string to the end of the specified file. 
		'''
		if os.path.exists(path) and not os.path.isfile(path):
			raise Exception(path + ' is a directory.')
		if not os.path.exists(os.path.dirname(path)):
			raise Exception('path not found: ' + os.path.dirname(path))
		with open(path, "a") as aFile:
			aFile.write(string)

	@classmethod
	def open(cls, path='', defaultName=None):
		'''
		Creates a new text file and returns a file variable that refers to it. 
		
		To write to the file, pass the file variable to the print function. 
		Displays a file save dialog box if path is an empty string. The file is closed 
		when the macro exits. Currently, only one file can be open at a time. For an example, 
		refer to the `SaveTextFileDemo`_ macro.

		.. _`SaveTextFileDemo`: https://imagej.net/macros/SaveTextFileDemo.txt
		'''
		if path=='' or not defaultName is None:
			title = path if defaultName else "openFile"
			defaultName = defaultName if defaultName else "log.txt"
			sd = SaveDialog(title, defaultName, ".txt")
			if not sd.getFileName():
				return ""
			path = sd.getDirectory()+sd.getFileName()
		file_extension = '.'+path.split('.')[-1]
		if os.path.exists(path) and not file_extension in ['.txt', '.java', '.xls', '.ijm', '.html', '.htm']:
			raise Exception("File exists and suffix is not '.txt', '.java', etc.")
		try:
			Settings.FILE = py_open(path, 'w')
		except IOError, e:
			raise Exception('File open error \n"'+str(e)+'"')
		return Settings.FILE

	@classmethod
	def close(cls, aFile):
		'''
		Closes the specified file, which must have been opened using File.open().
		'''
		aFile.close()

	@classmethod
	def copy(cls, path1, path2):
		'''
		Copies a file. 
		'''
		shutil.copy2(path1, path2)

	@classmethod
	def dateLastModified(cls, path):
		'''
		Returns the date and time the specified file was last modified.
		'''
		return time.ctime(os.path.getmtime(path))

	@classmethod
	def delete(cls, path):
		'''
		Deletes the specified file or directory. 
		
		With v1.41e or later, returns True if the file or directory was successfully deleted. 
		If the file is a directory, it must be empty. 
		'''
		if os.path.isfile(path):
			os.remove(path)
			return True
		if os.path.isdir(path):
			os.rmdir(path)
			return True
		return False

	@classmethod
	def exists(cls, path):
		'''
		Returns True if the specified file exists.
		'''
		return os.path.isfile(path) or os.path.isdir(path)

	@classmethod
	def getName(cls, path):
		'''
		Returns the file name (e.g., "blobs.tif") from path.
		'''
		return os.path.basename(path)

	@classmethod
	def getNameWithoutExtension(cls, path):
		'''
		Returns the name (e.g., "blobs") from path without the extension.
		'''
		return os.path.basename(path).split('.')[0]

	@classmethod
	def getDirectory(cls, path):
		'''
		Returns the name (e.g., "blobs") from path without the extension.
		'''
		path, filename = os.path.split(path)
		return path

	@classmethod
	def getDefaultDir(cls):
		'''
		 Returns the current working directory.
		'''
		return os.getcwd()

	@classmethod
	def setDefaultDir(cls, directoryPath):
		'''
		Set the default working directory.
		'''
		os.chdir(directoryPath)
	
	@classmethod
	def getParent(cls, path):
		'''
		Returns the parent of the file specified by path.
		'''
		parts = path.split('/')
		firstParts = parts[0:len(parts)-1]
		
		return '/'.join(firstParts)

	@classmethod
	def isDirectory(cls, path):
		'''
		Returns True if the specified file is a directory.
		'''
		return os.path.isdir(path)

	@classmethod
	def lastModified(cls, path):
		'''
		Returns the time the specified file was last modified as the number of milliseconds since January 1, 1970.
		'''
		return os.path.getmtime(path)

	@classmethod
	def length(cls, path):
		'''
		Returns the length in bytes of the specified file.
		
		For example: 
			length=File.length(path). 
			
		'''
		return os.path.getsize(path)

	@classmethod
	def makeDirectory(cls, path):
		'''
		Creates a directory.
		'''
		os.mkdir(path)

	@classmethod
	def openAsString(cls, path):
		'''
		Opens a text file and returns the contents as a string. 
				
		Displays a file open dialog box if path is an empty string. 
		Use lines=split(str,"\\n") to convert the string to an array of lines.		
		'''
		return IJ.openAsString(path)

	@classmethod
	def openAsRawString(cls, path, count=None):
		'''
		Opens a file and returns up to the first 5,000 bytes as a string. 
		
		Returns all the bytes in the file if the name ends with ".txt". 
		Refer to the `First10Bytes`_ and `ZapGremlins`_ macros for examples. 

		.. _`First10Bytes`: https://imagej.net/macros/First10Bytes.txt
		.. _`ZapGremlins`: https://imagej.net/macros/ZapGremlins.txt
		'''
		if path=='':
			od = OpenDialog("Open As String", "")
			directory = od.getDirectory()
			name = od.getFileName()
			if (name==None):
				return ""
			path = directory + name
		maxLength = count
		if (not count):
			maxLength = 5000
		length = os.path.getsize(path)
		if maxLength>length or (path.endswith('.txt') and not count):
			maxLength = length
		f = py_open(path, 'rb')
		chars = struct.unpack(str(maxLength) + "c", f.read(maxLength))
		out = ''.join(chars)
		return out

	@classmethod
	def openUrlAsString(cls, url):
		'''
		Opens a URL and returns the contents as a string. 
		
		Returns an emptly string if the host or file cannot be found. 
		With v1.41i and later, returns "<Error: message>" if there any error, including host or file not found. 
		'''
		try:
			contents = urllib2.urlopen(url).read()
		except (urllib2.URLError, ValueError), e:
			contents = ('<Error: ' + str(e) + '>')
		return contents

	@classmethod
	def openDialog(cls, title):
		'''
		 Displays a file open dialog and returns the path to the file chosen by the user (`example`_). 
		 
		 The macro exits if the user cancels the dialog. 

		 .. _`example`: https://imagej.net/macros/OpenDialogDemo.txt
		'''
		od = OpenDialog(title, "")
		directory = od.getDirectory()
		name = od.getFileName()
		if (name==None):
			sys.exit(0)
		path = directory + name
		return path

	@classmethod 
	def rename(cls, pathSrc, pathDest):
		'''
		 Renames, or moves, a file or directory. 
		 
		 Returns True if successful. 
		'''
		os.rename(pathSrc, pathDest)
		res = not os.path.exists(pathSrc) and os.path.exists(pathDest)
		return res

	@classmethod
	def saveString(cls, string, path):
		'''
		Saves string as a file.
		'''
		with py_open(path, "w") as txtFile:
			n = txtFile.write(string)
		return n

def fill(imp=None):
	'''
	Fills the image or selection with the current drawing color. 
	'''
	if (not imp):
		imp = IJ.getImage()
	IJ.runMacro('fill()')
	return imp

def fillOval(x, y, width, height, imp=None):
	'''
	Fills an oval bounded by the specified rectangle with the current drawing color. 
	
	See also:
	=========
	`drawOval`_, setColor, `autoUpdate`_.

	.. _`drawOval`: redirect.html#mripy.ijmpy.drawOval
	.. _`autoUpdate`: redirect.html#mripy.ijmpy.autoUpdate
	'''
	if (not imp):
		imp = IJ.getImage()
	imp.getProcessor().fillOval(x, y, width, height)
	return imp

def fillRect(x, y, width, height, imp=None):
	'''
	Fills the specified rectangle with the current drawing color. 
	
	See also:
	=========
	`drawRect`_, setColor, `autoUpdate`_.

	.. _`drawRect`: redirect.html#mripy.ijmpy.drawRect
	.. _`autoUpdate`: redirect.html#mripy.ijmpy.autoUpdate
	'''
	if (not imp):
		imp = IJ.getImage()
	imp.getProcessor().fillRect(x, y, width, height)
	return imp

class FitMeta(type):
	'''
	Meta class of the class Fit.
	'''
	@property
	def rSquared(self):
		'''
		Returns R^2=1-SSE/SSD, where SSE is the sum of the squares of the errors
		and SSD is the sum of the squares of the deviations about the mean. 
		'''
		return Fit.fitter.getRSquared()

	@property
	def nParams(self):
		'''
		Returns the number of parameters.
		'''
		return Fit.fitter.getNumParams()

	@property
	def nEquations(self):
		'''
		Returns the number of equations.
		'''
		return len(CurveFitter.fitList)

	@property
	def plot(self):
		'''
		Plots the current curve fit.
		'''
		Fitter.plot(Fit.fitter);

	@property
	def logResults(self):
		'''
		Causes doFit() to write a description of the curve fitting results to the Log window. 
		'''
		Fit.logFitResults = True

	@property
	def showDialog(self):
		'''
		Causes doFit() to display the simplex settings dialog.
		'''
		Fit.showFitDialog = True
		
class Fit(object):
	'''
	Fit Functions. These functions do curve fitting. 
	
	The `CurveFittingDemo`_ macro demonstrates how to use them. 

	.. _`CurveFittingDemo`: https://imagej.net/macros/examples/CurveFittingDemo.txt
	'''
	__metaclass__ = FitMeta
	fitter = None
	logFitResults = False
	showFitDialog = False
	
	@classmethod
	def doFit(cls, equation, xpoints, ypoints, initialGuesses=None):
		'''
		Fits the specified equation to the points defined by xpoints, ypoints. 
		
		Equation can be either the equation name or an index. The equation names are shown 
		in the drop down menu in the Analyze>Tools>Curve Fitting window. With ImageJ 1.42f 
		or later, equation can be a string containing a user-defined equation (example). 
		If initialGuesses is not None, initialGuesses must be an array equal in length to the 
		number of parameters in equation (example). 
		'''	
		equation = equation.lower()
		fitList = [f.lower() for f in CurveFitter.fitList]
		try:
			index = fitList.index(equation)
		except ValueError:
			index = -1
		isCustom = equation.find("y=")!=-1 or equation.find("y =")!=-1
		if index<0 and not isCustom:
			raise Exception('Unrecognized fit')
		if not len(xpoints)==len(ypoints):
			raise Exception('Arrays not same length')
		if len(xpoints)==0:
			raise Exception('Zero length array')	
		cls.fitter = CurveFitter(xpoints, ypoints)
		cls.fitter.setStatusAndEsc(None, True)
		if index==-1 and isCustom:		
			cls.fitter.doCustomFit(equation, initialGuesses, cls.showFitDialog)
		else:
			cls.fitter.doFit(index, cls.showFitDialog)
		if cls.logFitResults:
			IJ.log(cls.fitter.getResultString())
			cls.logFitResults = False
		cls.showFitDialog = False
		return float('nan')	

	@classmethod
	def p(cls, index):
		'''
		Returns the value of the specified parameter. 
		'''
		if index<0 or index > cls.fitter.getNumParams()-1:
			raise Exception("Index ("+str(index)+") is outside of the 0-"+str(cls.fitter.getNumParams()-1)+" range")
		p = cls.fitter.getParams()
		res = p[index] if index<len(p) else float('nan')
		return res

	@classmethod
	def f(cls, x):
		'''
		Returns the y value at x (`example`_). 

		.. _`example`: https://imagej.net/macros/examples/PlotSigmoidDerivatives.txt
		'''
		return cls.fitter.f(cls.fitter.getParams(), x)

	@classmethod
	def getEquation(cls, index):
		'''
		Returns the name and formula of the specified equation. 
		'''
		if index<0 or index>len(CurveFitter.fitList)-1:
			raise Exception("Index ("+str(index)+") is outside of the 0-"+str(CurveFitter.fitList.length-1)+" range") 
		name = CurveFitter.fitList[index]
		formula = CurveFitter.fList[index]
		return name, formula

def floodFill(x, y, connectivity = '4-connected', imp = None):
	'''
	Fills, with the foreground color, pixels that are connected to, and have the same color as, the pixel at (x, y). 
	
	Does 8-connected filling if there is an optional string argument 
	containing "8", for example floodFill(x, y, "8-connected"). 
	This function is used to implement the `flood fill (paint bucket)`_ macro tool. 

	.. _`flood fill (paint bucket)`: https://imagej.net/macros/tools/FloodFillTool.txt
	'''
	if not imp:
		imp = IJ.getImage()
	ip = imp.getProcessor()
	floodFiller = FloodFiller(ip)
	if connectivity.find('8')>= 0:
		floodFiller.fill8(x, y)
	else:
		floodFiller.fill(x, y)
	__updateAndDraw()
	return imp

def floor(n):
	'''
	Returns the largest value that is not greater than n and is equal to an integer. 
	
	See also: 
	=========
	round
	'''
	return math.floor(n)

def fromCharCode(*args):
	'''
	This function takes one or more Unicode values and returns a string. 
	'''
	return ''.join(map(unichr, args))

def getBoolean(message, yesLabel="  Yes  ", noLabel="  No  "):
	'''
	Displays a dialog box containing the specified message and "Yes", "No" and "Cancel" buttons. 
	
	Returns True if the user clicks "Yes", returns False if the user clicks "No" and exits the script if the user clicks "Cancel". 
	'''
	title = ''
	d = YesNoCancelDialog(IJ.getInstance(), title, message, yesLabel, noLabel)
	if d.cancelPressed():
		sys.exit(0)
	if d.yesPressed():
		return True
	return False

def getBoundingRect(img=None):
	'''
	Replace by `getSelectionBounds`_. 

	.. _`getSelectionBounds`: redirect.html#mripy.ijmpy.getSelectionBounds
	'''
	return getSelectionBounds(img)
	
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

def getSelectionBounds(img=None):
	'''
	Returns the smallest rectangle that can completely contain the current selection
	as a tupel x, y, width, height. 

	
	x and y are the pixel coordinates of the upper left corner of the rectangle. 
	width and height are the width and height of the rectangle in pixels. 
	If there is no selection, returns (0, 0, ImageWidth, ImageHeight). 
	
	See also: 
	=========
	selectionType and setSelectionLocation. 
	'''
	if not img:
		img = IJ.getImage()
	roi = img.getRoi()
	if roi:
		r = roi.getFloatBounds()
		return r.x, r.y, r.width, r.height
	else:
		return 0, 0, img.getWidth(), img.getHeight()

def getCursorLoc(img = None):
	'''
	Returns the cursor location in pixels and the mouse event modifier flags 
	(x, y, z, flags). 
	
	The z coordinate is zero for 2D images. For stacks, it is one less than the slice number. 
	Use toScaled(x,y) to scale the coordinates. For examples, see the `GetCursorLocDemo`_ and the 
	`GetCursorLocDemoTool`_ macros.

	.. _`GetCursorLocDemo`: https://imagej.net/macros//GetCursorLocDemo.txt
	.. _`GetCursorLocDemoTool`: https://imagej.net/macros/tools/GetCursorLocDemoTool.txt
	'''
	if not img:
		img = IJ.getImage()
	ic = img.getCanvas()
	if not ic:
		return None
	p = ic.getCursorLoc()
	z = img.getCurrentSlice()-1
	roi = img.getRoi()
	flags = ic.getModifiers() 
	insideRoi = 32 if (roi and roi.contains(p.x,p.y)) else 0
	flags = flags + insideRoi
	return p.x, p.y, z, flags

def getDateAndTime():
	'''
	Returns the current date and time:
		(year, month, dayOfWeek, dayOfMonth, hour, minute, second, millisecond) 
	
	Note that 'month' and 'dayOfWeek' are zero-based indexes. 
	For an example, refer to the GetDateAndTime macro. 
	
	See also: 
	=========
	getTime
	'''
	date = Calendar.getInstance()
	return date.get(Calendar.YEAR),\
		   date.get(Calendar.MONTH),\
		   date.get(Calendar.DAY_OF_WEEK)-1,\
		   date.get(Calendar.DAY_OF_MONTH),\
		   date.get(Calendar.HOUR_OF_DAY),\
		   date.get(Calendar.MINUTE),\
		   date.get(Calendar.SECOND),\
		   date.get(Calendar.MILLISECOND)

def getDimensions(img=None):
	'''
	Returns the dimensions width, height, channels, slices and frames of the current image.
	'''
	if not img:
		img = IJ.getImage()
	dim = img.getDimensions()
	return tupel(dim)

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

def nResults():
	'''
	Returns the current measurement counter value. The parentheses "()" are optional in the ij-macro language but *not* in ijmpy. 
	
	See also: 
	=========
	getValue("results.count"). 
	'''
	return Analyzer.getResultsTable().getCounter();
	
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
		
def run(command, parameters=None):
	'''
	Executes an ImageJ menu command. 
	
	The optional second argument contains values that are automatically entered into dialog boxes 
	(must be GenericDialog or OpenDialog). Use the Command Recorder (Plugins>Macros>Record) to generate run() function calls. 
	Use string concatenation to pass a variable as an argument. 
	With ImageJ 1.43 and later, variables can be passed without using string concatenation by adding "&" to the variable name. 
	For examples, see the ArgumentPassingDemo_ macro.
	
	.. _ArgumentPassingDemo: https://imagej.net/macros/ArgumentPassingDemo.txt
	''' 
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

def print(*args):
	'''
	For now just writes to the ImageJ-log window.
	'''
	if Settings.FILE and args[0]==Settings.FILE:
		Settings.FILE.write(args[1])
		return
	stringList = [str(item) for item in list(args)]
	message = ', '.join(stringList)
	IJ.log(message)

def __getNameOfArg(arg):
	'''
	Utility function to get the name of the variable that was passed as an argument 
	to the function.	
	'''
	name = None
	outerFrameLocals = inspect.currentframe().f_back.f_back.f_locals	
	for key in outerFrameLocals.keys():
		if id(outerFrameLocals[key])==id(arg):
			name = key
	return name

def __updateAndDraw():
	if Settings.AUTO_UPDATE:
		imp = IJ.getImage()
		imp.updateChannelAndDraw()
		imp.changes = True
	else:
		Settings.UPDATE_NEEDED = True

def __getColor(aColor):
	aColor = aColor.lower()
	if aColor.startswith('#'):
		return Colors.decode(aColor, Color.black)
	colors = {
	 'black': Color.black, 'white': Color.white, 'red': Color.red, 'green': Color.green, 'blue': Color.blue,
	 'cyan': Color.cyan, 'magenta': Color.magenta, 'yellow': Color.yellow,
	 'darkgray': Color.darkGray, 'gray': Color.gray, 'lightgray': Color.lightGray,
	 'orange': Color.orange, 'pink': Color.pink
	}
	if not aColor in colors:
		raise Exception("'red', 'green', or '#0000ff' etc. expected")
	return colors[aColor]

def example():
	'''
	An example of how to use the macro commands.
	'''
	run("Blobs (25K)");
	run("Invert");
	setAutoThreshold();
	close();