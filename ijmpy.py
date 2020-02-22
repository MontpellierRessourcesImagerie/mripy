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

acos()
------

Import the function from python's math module instead. 

.. code-block:: python

	from math import acos

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
from __future__ import print_function					# we will overwrite python's print command
import __builtin__										# to use the python print command: __builtin__.print(<text>)
from ij import IJ, WindowManager
from ij.process import FloatProcessor, ColorProcessor
from ij.plugin.frame import RoiManager
from ij.plugin.filter import MaximumFinder
from ij.process import FHT
from ij.util import Tools
from java.lang import Double
from ij.measure import ResultsTable
from ij.plugin.filter import Analyzer
import math

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

		if len(args)==0 or (len(args)==1 and not isinstance(args[0], list)):
			raise Exception('Array show needs at least one array')

		title = "Arrays"
		if len(args)==1:
			title = getNameOfArg(args[0])
			column = "Value"
			rt = ResultsTable()
			for value in args[0]:
				rt.incrementCounter()
				rt.addValue(column, value)
			rt.show(title)
			return rt
		indexes = False
		rowNumbers = False
		if (isinstance(args[0], str)):
			title = args[0]
			if title.find('(indexes)')>=0:
				indexes = True
				title = title.replace('(indexes)', '')
			if title.find('(row numbers)')>=0:
				rowNumbers = True
				title = title.replace('(row numbers)', '')
		if (title.lower=='results'):
			rt = Analyzer.getResultsTable()
		else:
			rt = ResultsTable()
		for array in args:
			if isinstance(array, str):
				continue
			for value in array:
				column = getNameOfArg(array)
				rt.incrementCounter()
				rt.addValue(column, value)
		rt.showRowIndexes(indexes)
		rt.showRowNumbers(rowNumbers)
		rt.show(title)
		return rt
			
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

def getNameOfArg(arg):
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