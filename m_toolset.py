from ij.plugin.tool import MacroToolRunner
from ij.plugin import MacroInstaller
from ij.gui import GenericDialog


class MyActionToolOptions(MacroToolRunner):
	minSize = 6
	name = "my options Action Tool"
	icon = "C000T4b12o"

	def getToolName(self):
		return self.name

	def getToolIcon(self):
		return self.icon

	def runMacroTool(self, name):
		self.showOptionsDialog()
		
	def showOptionsDialog(self):
		gd = GenericDialog("my cool tool options")
		gd.addNumericField("min. size: ", self.minSize)
		gd.showDialog()
		if gd.wasCanceled():
			return None
		self.minSize = gd.getNextNumber()

def myAction():
	print("myAction exceuted")
	
class MyActionTool(MacroToolRunner):

	minSize = 6
	name = "my cool Action Tool"
	icon = "C000T4b12a"
	
	def getToolName(self):
		return self.name

	def getToolIcon(self):
		return self.icon

	def runMacroTool(self, name):
		myAction()
		
	def showOptionsDialog(self):
		gd = GenericDialog("my cool tool options")
		gd.addNumericField("min. size: ", self.minSize)
		gd.showDialog()
		if gd.wasCanceled():
			return None
		self.minSize = gd.getNextNumber()

macroInstaller = MacroInstaller()
options = MyActionToolOptions(macroInstaller)
options.run("")
tool = MyActionTool(macroInstaller)
tool.run("")