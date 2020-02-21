'''
bialangsj is a python wrapper to the imagej2 api. It tries to create a bio-image analyst 
centric api for imagej2.
'''

from net.imagej import ImageJ

ops = ImageJ().op()

class ImageOperation(object):
	'''
	Abstract super-class for image-operations. 
	'''
	def run(self, image):
		'''
		Run the operation implemented in the apply-method on the image.

		:param image: the input image
		:return: the value returned by the image-operation
		
		'''
		return self.apply(image)

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
	Uses a Sobel-filter.
	'''
	def apply(self, inputImage):
		sobel = ops.filter().sobel(inputImage)
		newImage = ops.create().img(sobel)
		ops.image().normalize(newImage, sobel)
		return newImage

def findEdges(image=None):
	'''
	Run the `FindEdges`_ operation.

	.. _`FindEdges`: redirect.html#mripy.bialang.FindEdges
	'''
	return FindEdges().run(image)