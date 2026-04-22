from material.basicMaterial import BasicMaterial
from OpenGL.GL import *

class SurfaceBasicMaterial(BasicMaterial):

	def __init__(self, properties={}):
		super().__init__()

		self.settings["drawStyle"] = GL_TRIANGLES

		self.settings["lineWidth"] = 4

		self.settings["doubleSide"] = True

		self.settings["wireframe"] = False

		self.setProperties(properties)

	def updateRenderSettings(self):

		# glLineWidth(self.settings["lineWidth"])

		if self.settings["doubleSide"]:
			glDisable(GL_CULL_FACE)
		else:
			glEnable(GL_CLL_FACE)

		if self.settings["wireframe"]:
			glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
		else:
			glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
