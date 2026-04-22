from material.basicMaterial import BasicMaterial
from OpenGL.GL import *

class LineBasicMaterial(BasicMaterial):

	def __init__(self, properties={}):
		super().__init__()

		# drawStyle: GL_LINE_STRIP | GL_LINE_LOOP | GL_LINES
		self.settings["drawStyle"] = GL_LINE_STRIP

		self.settings["lineWidth"] = 4

		# line type: "connected" | "loop" | "segments"
		self.settings["lineType"] = "connected"

		self.setProperties(properties)

	def updateRenderSettings(self):

		glLineWidth(self.settings["lineWidth"])

		if self.settings["lineType"] == "connected":
			self.settings["drawStyle"] = GL_LINE_STRIP		
		elif self.settings["lineType"] == "loop":
			self.settings["drawStyle"] = GL_LINE_LOOP
		elif self.settings["lineType"] == "segments":
			self.settings["drawStyle"] = GL_LINES
		else:
			raise Exception("Unknow line style: " + self.settings["lineType"])