from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from OpenGL.GL import *

from math import sin

"""
This script demonstrates animating two triangles using a single vertex buffer
and uniform variables. Each triangle has its own translation and color uniform,
which are updated dynamically in the `update` method to create movement and color changes.
"""

class Test(Base):
	"""
	Main class for the OpenGL application, inheriting from Base.
	Handles initialization (shaders, VAO, attributes, uniforms) and rendering
	and animation logic for multiple instances of an object.
	"""

	def initialize(self):
		"""
		Initializes the OpenGL program, including shaders configured for uniform inputs,
		a single Vertex Array Object (VAO) for the base geometry,
		and uniform variables for translation and color.
		"""
		print("Initializing program...")

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

		# Render settings:
		# Set the clear color for the framebuffer (background color).
		glClearColor(0.6, 0.8, 0.8, 1.0) # Light blue-gray background

		# Set up a single Vertex Array Object (VAO) to manage the attribute data.
		# We only need one VAO because both triangles share the same underlying geometry.
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

		# Uniform for the translation of the first triangle (initial position).
		self.translation1 = Uniform("vec3", [-0.5, 0.0, 0.0]) # Initially moved to the left.
		# Get the memory location (reference) of the "translation" uniform variable in the shader.
		self.translation1.locateVariable(self.programRef, "translation") 

		# Uniform for the translation of the second triangle (initial position).
		self.translation2 = Uniform("vec3", [0.5, 0.0, 0.0]) # Initially moved to the right.
		self.translation2.locateVariable(self.programRef, "translation") 

		# Uniform for the base color of the first triangle (red).
		self.baseColor1 = Uniform("vec3", [1.0, 0.0, 0.0]) 
		self.baseColor1.locateVariable(self.programRef, "baseColor")

		# Uniform for the base color of the second triangle (blue).
		self.baseColor2 = Uniform("vec3", [0.0, 0.0, 1.0]) 
		self.baseColor2.locateVariable(self.programRef, "baseColor")

		# Tracking elapsed time for animation.
		self.time = 0 # Re-initialize to ensure it starts from 0 each run.

	def update(self):
		"""
		Called once per frame to render the scene and update animation.
		This method clears the screen, updates uniform values for animation,
		and draws two triangles with their dynamic properties.
		"""
		# Set the active shader program.
		glUseProgram(self.programRef)

		# Clear the color buffer with the background color defined in initialize.
		glClear( GL_COLOR_BUFFER_BIT )
		# Increment time for animation, assuming ~30 frames per second.
		self.time += 1/30
		
		# --- Draw the first triangle (animated translation) ---
		# Check if the triangle has moved off the top of the screen (y > 1.2).
		if self.translation1.data[1] >= 1.2:
			self.translation1.data[1] = -1.2 # Reset its vertical position to the bottom.
		# Increment the vertical (y) component of its translation.
		self.translation1.data[1] += .01
		# Upload the updated translation uniform value to the GPU.
		self.translation1.uploadData()
		# Upload the (static) base color uniform value to the GPU.
		self.baseColor1.uploadData()
		# Draw the base triangle geometry with the current uniform values.
		glDrawArrays( GL_TRIANGLES, 0, self.vertexCount)

		# --- Draw the second triangle (animated color) ---
		# Animate the blue component of the second triangle's color using a sine wave.
		# (sin(self.time) + 1) / 2 ensures the value stays between 0.0 and 1.0.
		self.baseColor2.data[2] = (sin(self.time) + 1) / 2
		# Upload the (static) translation uniform value to the GPU.
		self.translation2.uploadData()
		# Upload the updated (animated) base color uniform value to the GPU.
		self.baseColor2.uploadData()
		# Draw the base triangle geometry with the current uniform values.
		glDrawArrays( GL_TRIANGLES, 0, self.vertexCount)

# Create an instance of the Test class and run the application.
Test().run()