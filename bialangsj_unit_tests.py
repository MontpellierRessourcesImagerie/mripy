#@ OpService ops

from mripy.bialangsj import *
import unittest
import sys
from net.imglib2.type.numeric.integer import UnsignedByteType

class findEdgesTest(unittest.TestCase):

	def testRectangle(self):
		# create a test image with a filled rectangle
		testImg = ops.run("create.img", [256, 256], UnsignedByteType())
		formula = "(p[0]>10 && p[0]<110 && p[1]>10 && p[1]<110)*255"
		ops.image().equation(testImg, formula)
		
		edgesImage = findEdges(testImg);

		ra = edgesImage.randomAccess()

		ra.setPosition([9, 9])
		v1 = ra.get().get()
		ra.setPosition([10, 10])
		v2 = ra.get().get()
		ra.setPosition([11,11])
		v3 = ra.get().get()
		ra.setPosition([12,12])
		v4 = ra.get().get()
	
		self.assertEquals(v1, 0)
		self.assertEquals(v2, 64)
		self.assertEquals(v3, 255)
		self.assertEquals(v4, 0)

def suite():
	suite = unittest.TestSuite()

	suite.addTest(findEdgesTest('testRectangle'))

	return suite

runner = unittest.TextTestRunner(sys.stdout, verbosity=1)
runner.run(suite())