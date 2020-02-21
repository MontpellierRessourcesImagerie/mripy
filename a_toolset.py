from fiji.tool import AbstractTool
from ij.gui import Toolbar
from fiji.tool import ToolToggleListener
from fiji.tool import ToolWithOptions

class My_Tool(AbstractTool, ToolToggleListener):

	def getToolName(self):
		self.name = "my_cool_Action_Tool"
		return self.name

	def getToolIcon(self):
		self.toolicon = "C000T4b12m"
		return self.toolicon
		
	def toolToggled(self, enabled):
		print(self.getToolName() + " was switched " + str(enabled))
		Toolbar.getInstance().restorePreviousTool()

toolID = Toolbar.getInstance().getToolId();
tool = My_Tool()
tool.run("")
Toolbar.getInstance().setTool(toolID);