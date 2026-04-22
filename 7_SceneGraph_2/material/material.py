from core.openGLUtils import OpenGLUtils
from core.uniform import Uniform

class Material(object):

	def __init__(self, vertexShaderCode, fragementShaderCode):

		# compile shader code
		self.programRef = OpenGLUtils.initializeProgram(vertexShaderCode, 
														fragementShaderCode)
		# store uniform objects
		self.uniforms = {}

		self.uniforms["modelMatrix"] = Uniform("mat4", None)
		self.uniforms["viewMatrix"] = Uniform("mat4", None)
		self.uniforms["projectionMatrix"] = Uniform("mat4", None)

		# store OpenGL render settings
		self.settings = {}
		self.settings["drawStyle"] = None

	def locateUniforms(self):
		for variableName, uniformObject in self.uniforms.items():
			uniformObject.locateVariable(self.programRef, variableName)

	def updateRenderSettings(self):
		pass

	def setProperties(self, properties={}):
		for name, data in properties.items():
			if name in self.uniforms.keys():
				self.uniforms[name].data = data
			elif name in self.settings.keys():
				self.settings[name].data = data
			else:
				raise Exception("Material has not property: " + name)


	def addUniform(self, dataType, variableName, data):
		self.uniforms[variableName] = Uniform(dataType, data)





