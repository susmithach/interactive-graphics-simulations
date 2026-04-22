from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from OpenGL.GL import *

import random # For random colors
import pygame # No longer directly using pygame.K_, but still needed for window events

"""
This script demonstrates an interactive OpenGL application that renders a single triangle.
Its movement is controlled by keyboard arrow keys, and its color can be changed randomly by pressing the spacebar.
It utilizes uniform variables for dynamic translation and color updates, along with an enhanced
Input class for keyboard state management.
"""

class Test(Base):
	"""
	Main class for the OpenGL application, inheriting from Base.
	Handles initialization (shaders, VAO, attributes, uniforms) and renders
	an interactive triangle based on user input.
	"""

	def initialize(self):
		"""
		Initializes the OpenGL program, including shaders configured for uniform inputs,
		a single Vertex Array Object (VAO) for the base geometry,
		and uniform variables for translation and color. It also sets up input handling.
		"""
		print("Initializing program...")

		# Shaders
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
		# We only need one VAO for the single triangle.
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

		# Uniform for the translation of the triangle (initial position).
		self.translation = Uniform("vec3", [0.0, 0.0, 0.0]) # Start at the origin.
		# Get the memory location (reference) of the "translation" uniform variable in the shader.
		self.translation.locateVariable(self.programRef, "translation") 

		# Uniform for the base color of the triangle (initial color - white).
		self.baseColor = Uniform("vec3", [1.0, 1.0, 1.0]) 
		self.baseColor.locateVariable(self.programRef, "baseColor")

	def update(self):
		"""
		Called once per frame to render the scene and handle user input.
		This method clears the screen, processes keyboard input for movement and color changes,
		updates uniform values, and draws the triangle.
		"""
		# Set the active shader program.
		glUseProgram(self.programRef)

		# Clear the color buffer with the background color defined in initialize.
		glClear( GL_COLOR_BUFFER_BIT )

		# --- Keyboard Input Handling ---
		move_speed = 0.05 # Adjust for desired movement speed

		# Continuous movement using isKeyPressed
		if self.input.isKeyPressed("up"):
			self.translation.data[1] += move_speed
		if self.input.isKeyPressed("down"):
			self.translation.data[1] -= move_speed
		if self.input.isKeyPressed("left"):
			self.translation.data[0] -= move_speed
		if self.input.isKeyPressed("right"):
			self.translation.data[0] += move_speed

		# One-time color change on spacebar press using isKeyDown
		if self.input.isKeyDown("space"):
			# Generate random RGB values between 0.0 and 1.0
			r = random.uniform(0, 1)
			g = random.uniform(0, 1)
			b = random.uniform(0, 1)
			self.baseColor.data = [r, g, b] # Update the color uniform's data

		# --- Draw the triangle ---
		# Upload the current values for the translation uniform to the GPU.
		self.translation.uploadData()
		# Upload the current values for the color uniform to the GPU.
		self.baseColor.uploadData()
		# Draw the base triangle geometry with the current uniform values.
		glDrawArrays( GL_TRIANGLES, 0, self.vertexCount)

# Create an instance of the Test class and run the application.
Test().run()
