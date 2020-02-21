from ij.gui import Toolbar
from ij.plugin.tool import PlugInTool
from fiji.tool import ToolToggleListener

class MyActionTool(PlugInTool, ToolToggleListener):

	def getToolName(self):
		self.name = "my_cool_Action_Tool-"
		return self.name

	def getToolIcon(self):
		self.toolicon = "C000T4b12n"
		return self.toolicon

	def runMacroTool(self, name):
		print("runMacroTool exceuted")

	def run(self, args):
		super(type(self), self).run(args)
		print("run exceuted")

	def mousePressed(self, imp, e):
		print("mouse pressed")

	def actionPerformed(self, e):
		print("action performed")

	def toolToggled(self, enabled):
		if (enabled):
			text = "on"
		else:
			text = "off"
		IJ.log(self.getToolName() + " was switched " + text)
	
tool = MyActionTool()
tool.run("")
#Toolbar.addPlugInTool(tool)
