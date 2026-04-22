from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from OpenGL.GL import *
from math import sin

"""
This script demonstrates how to render multiple instances of a single geometric shape
(a triangle) using only one Vertex Array Object (VAO) and one vertex buffer.
Each instance's position and color are controlled dynamically using uniform variables
sent from the CPU to the GPU before each draw call.
"""

class Test(Base):
	"""
	Main class for the OpenGL application, inheriting from Base.
	Handles initialization (setting up shaders with uniform inputs, VAO, attributes,
	uniform variables) and rendering multiple instances of an object.
	"""

	def initialize(self):
		"""
		Initializes the OpenGL program, including shaders configured for uniform inputs,
		a single Vertex Array Object (VAO) for the base geometry,
		and uniform variables for translation and color.
		"""
		print("Initializing program...")

		# Time variable, typically used for animation (updates every frame).
		self.time = 0

		# Vertex Shader Code: Transforms vertices based on a uniform translation.
		# `position` (vec3): Incoming vertex position from the buffer.
		# `translation` (uniform vec3): A uniform variable passed from the CPU
		#                             to translate the object in x, y, z.
		vsCode = """
		in vec3 position;
		uniform vec3 translation; // used to translate the x,y,z

		void main()
		{
			vec3 pos = position + translation; // get new location of vertices
			gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
		}
		"""

		# Fragment Shader Code: Determines the final color of each pixel based on a uniform color.
		# `baseColor` (uniform vec3): A uniform variable passed from the CPU
		#                           to set the base color of the object.
		# `fragColor` (out vec4): The final color of the fragment (pixel).
		fsCode = """
		uniform vec3 baseColor;
		out vec4 fragColor;
		void main()
		{
			fragColor = vec4(baseColor.r, baseColor.g, baseColor.b, 1.0);
		}
		"""

		# Initialize the GPU program using the vertex and fragment shaders.
		self.programRef = OpenGLUtils.initializeProgram( vsCode, fsCode )

		# Set up a single Vertex Array Object (VAO) to manage the attribute data.
		# We only need one VAO because both triangles share the same underlying geometry (position data).
		vaoRef = glGenVertexArrays(1)
		glBindVertexArray(vaoRef)

		# Set up the position attribute for the base triangle geometry.
		# This defines an equilateral triangle centered at the origin.
		positionData = [[0.0, 0.2, 0.0],
						[0.2, -0.2, 0.0],
						[-0.2, -0.2, 0.0]] 
		
		# Create an Attribute object for position data.
		positionAttribute = Attribute("vec3", positionData) 
		# Associate this attribute with the "position" variable in the shader program.
		positionAttribute.associateVariable( self.programRef, "position")

		# Store the number of vertices; used for drawing.
		self.vertexCount = len(positionData)

		# Set up uniform attributes:
		# Uniforms are global shader variables (set by the CPU) that are constant
		# for all vertices/fragments in a single draw call. They are NOT bound to a VAO.
		# We store them as instance variables and upload data before each draw call.

		# Uniform for the translation of the first triangle.
		self.translation1 = Uniform("vec3", [-0.5, 0.0, 0.0]) # Move to the left.
		# Get the memory location (reference) of the "translation" uniform variable in the shader.
		self.translation1.locateVariable(self.programRef, "translation") 

		# Uniform for the translation of the second triangle.
		self.translation2 = Uniform("vec3", [0.5, 0.0, 0.0]) # Move to the right.
		self.translation2.locateVariable(self.programRef, "translation") 

		# Uniform for the base color of the first triangle.
		self.baseColor1 = Uniform("vec3", [1.0, 0.0, 0.0]) # Red.
		self.baseColor1.locateVariable(self.programRef, "baseColor")

		# Uniform for the base color of the second triangle.
		self.baseColor2 = Uniform("vec3", [0.0, 0.0, 1.0]) # Blue.
		self.baseColor2.locateVariable(self.programRef, "baseColor")

	def update(self):
		"""
		Called once per frame to render the scene. This method draws two triangles
		by updating and uploading uniform variables for each before issuing draw calls.
		"""
		# Update the time variable for potential animation.
		self.time += 1/60

		# Set the active shader program.
		glUseProgram(self.programRef)
		
		# --- Draw the first triangle ---
		# Upload the current values for the translation and color uniforms to the GPU.
		self.translation1.uploadData()
		self.baseColor1.uploadData()
		# Draw the base triangle geometry using GL_TRIANGLES primitive type.
		glDrawArrays( GL_TRIANGLES, 0, self.vertexCount)

		# --- Draw the second triangle ---
		# Upload the current values for the translation and color uniforms for the second triangle.
		self.translation2.uploadData()
		self.baseColor2.uploadData()
		# Draw the base triangle geometry again with the new uniform values.
		glDrawArrays( GL_TRIANGLES, 0, self.vertexCount)

# Create an instance of the Test class and run the application.
Test().run()