''' 
bialang is a python wrapper to the imagej1 api. It tries to create a simpler
api for imagej1 to allow writing more readable and re-usable bio-image analysis
scripts.

Currently there are 4 ways to write image analysis workflows in ImageJ:

	* as an imagej-macro
	* as a script in one of the scripting languages (python, groovy, javascript, ...)
	* as a plugin in java
	* using operators and imglib2 from the sci-java framework 

A nice feature is that actions can be recorded in different languages, using the macro-recorder.

However there are some problems with the above approaches:

	* the code contains technical details and is not centered on the (bio-)image analysis  
	* the macro-language has little support for code-organization and re-use.
	* execution depends on the global state in imagej (global settings like the "Black background option, ...)
	* operations are applied to the active image or window
	* parameters are passed as strings
	* the sci-java remedies most of the problems, however a high level image analysis api is still missing.

Example:

Here is a simple pre-processing workflow in the ijm::

	run("Duplicate...", " ");
	run("Find Edges");
	run("8-bit");
	run("Smooth");
	setAutoThreshold(thresholdMethod);
	run("Analyze Particles...", "size="+minSize+"-"+maxSize+" circularity=0.00-1.00 show=Masks exclude in_situ");
	run("Create Selection");
	run("Enlarge...", "enlarge=" + numberOfDilates + " pixel");
	roiManager("Add");
	close();
	roiManager("select", 0);
	run("Clear Outside");

In a scripting language it would look something like this::

	imp2 = imp.duplicate();
	IJ.run(imp, "Find Edges", "");
	IJ.run(imp, "8-bit", "");
	IJ.run(imp, "Smooth", "");
	IJ.setAutoThreshold(imp, "Percentile dark");
	IJ.run(imp, "Analyze Particles...", "size=350-20000 show=Masks exclude in_situ");
	IJ.run(imp, "Create Selection", "");
	IJ.run(imp, "Enlarge...", "enlarge=10");
	rm.addRoi(imp.getRoi());
	imp.close();
	rm.select(0);
	IJ.setBackgroundColor(0, 0, 0);
	IJ.run(imp, "Clear Outside", "");

Here is how it looks like in bialang::

	image = duplicate(inputImage)
	findEdges(image)
	to8Bit(image)
	smooth(image)
	toMask(image, 
           percentileThreshold(image), 
           Filter(minSize, maxSize, minCirc, maxCirc, exclude))
	roi = createSelection(image)
	close(image)
	enlarge(roi, numberOfDilates, unit=units.pixel)
	clearOutside(inputImage, roi)

The operations like duplicate, findEdges, ... are objects which instead being immediatly run can also be created and
configured first and then explicitly run.

For example::

	Duplicate = Duplicate()
	Duplicate.selectChannels(1, 3)
	Duplicate.setZSices(1, 3, 5, 7)
	Duplicate.run(image)

written 2020 by `Volker Baecker`_, `Montpellier Ressources Imagerie`_, Biocampus Montpellier, UM, INSERM, CNRS

.. _`Volker Baecker`: https://github.com/volker-baecker
.. _`Montpellier Ressources Imagerie`: http://www.mri.cnrs.fr

Have fun!
'''

from ij import IJ, WindowManager
from ij.plugin.filter import Filters;

class ImageOperation(object):
	'''
	Abstract super-class for image-operations. 
	'''
	def run(self, image=None):
		'''
		Run the operation implemented in the apply-method on the image.

		:param image: the input image
		:return: the value returned by the image-operation
		
		'''
		if image is None:
			inputImage = IJ.getImage()
		else:
			inputImage = image
		return self.apply(inputImage)

	def apply(self, image):
		'''
		Apply the operation to the image.
		
		Return an image or other data calculated from the image.
		Abstract method that must be overridden by subclasses.
		'''
		pass
		
class FindEdges(ImageOperation):
	'''
	Apply an edge-filter to the image. 
	
	Edges will have high values in the resulting image.
	Uses a radius 1 (3x3)-pixel Sobel-filter.
	'''
	def apply(self, inputImage):
		filter = Filters();
		filter.setup('edge', inputImage)
		filter.run(inputImage.getProcessor())
		return inputImage

def findEdges(image=None):
	'''
	Run the `FindEdges`_ operation.

	.. _`FindEdges`: redirect.html#mripy.bialang.FindEdges
	'''
	return FindEdges().run(image)