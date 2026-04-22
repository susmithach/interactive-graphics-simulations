from material.material import Material
from OpenGL.GL import *

class TextureMaterial(Material):
	"""
	A material that applies a 2D texture to an object.
	"""

	def __init__(self, texture, properties={}):
		"""
		Initializes a TextureMaterial object.
		
		Args:
			texture (Texture): The Texture object to apply.
			properties (dict, optional): A dictionary of material properties to override default values. Defaults to {}.
		"""

		vertexShaderCode = """
		uniform mat4 projectionMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 modelMatrix;

		in vec3 vertexPosition;
		in vec2 vertexUV;

		out vec2 UV;

		void main()
		{
			vec4 position = vec4(vertexPosition, 1.0);
			gl_Position = projectionMatrix * viewMatrix * modelMatrix * position;

			UV = vertexUV;
		}
		"""

		fragmentShaderCode = """
		uniform vec3 baseColor;
		uniform sampler2D textureSampler2D;

		in vec2 UV;
		out vec4 fragColor;

		void main()
		{
			vec4 color = vec4(baseColor, 1.0);
			//fragColor = color * texture2D( textureSampler2D, UV ); // this is for Windows
			fragColor = color * texture( textureSampler2D, UV ); // this is for Mac
		}
		"""

		super().__init__(vertexShaderCode, fragmentShaderCode)

		# add uniforms
		self.addUniform("vec3", "baseColor", [1.0, 1.0, 1.0])
		self.addUniform("sampler2D", "textureSampler2D", [texture.textureRef, 1])
		self.locateUniforms()

		# draw style
		self.settings["drawStyle"] = GL_TRIANGLES
		# render both side?
		self.settings["doubleSide"] = True
		# render wireframe?
		self.settings["wireframe"] = False
		# line thickness
		self.settings["lineWidth"] = 1

		self.setProperties( properties )

	def updateRenderSettings(self):
		"""
		Updates OpenGL render settings based on the material's properties.
		This includes culling, wireframe mode, and line width.
		"""
		if self.settings["doubleSide"] == True:
			glDisable(GL_CULL_FACE)
		else:
			glEnable(GL_CULL_FACE)

		if self.settings["wireframe"] == True:
			glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
		else:
			glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

		glLineWidth(self.settings["lineWidth"])

