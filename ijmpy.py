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
'''
from __future__ import print_function					# we will overwrite python's print command
import __builtin__										# to use the python print command: __builtin__.print(<text>)
from ij import IJ, WindowManager
from ij.process import FloatProcessor, ColorProcessor
from ij.plugin.frame import RoiManager

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
	---------
	setThreshold, resetThreshold
	'''
	image = IJ.getImage()
	processor = image.getProcessor()
	t1 = processor.getMinThreshold()
	t2 = processor.getMaxThreshold()
	return t1, t2
	
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
	---------
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
	
def example():
	'''
	An example of how to use the macro commands.
	'''
	run("Blobs (25K)");
	run("Invert");
	setAutoThreshold();
	roiManager("Select", 0);
	close();
