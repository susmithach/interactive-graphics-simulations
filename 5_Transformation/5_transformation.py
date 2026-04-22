from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from core.matrix import Matrix
from OpenGL.GL import *
from math import pi

"""
This script demonstrates various transformations (translation, rotation) and perspective projection
in OpenGL. It shows how to manipulate an object's position and orientation in 3D space
using model and projection matrices, which are updated via uniform variables.
It also includes concepts of global vs. local transformations and depth testing.
"""

class Test(Base):
	"""
	Main class for the OpenGL application, inheriting from Base.
	Handles initialization (shaders with matrix uniforms, VAO, attributes, matrices)
	 and rendering with interactive transformations.
	"""

	def initialize(self):
		"""
		Initializes the OpenGL program, including shaders, a single Vertex Array Object (VAO),
		position attributes, and uniform matrices for model and projection transformations.
		"""
		print("Initializing...")

		# Vertex Shader Code:
		# `position` (vec3): Incoming vertex position from the buffer.
		# `projectionMatrix` (uniform mat4): Matrix to project 3D coordinates onto the 2D screen.
		# `modelMatrix` (uniform mat4): Matrix to transform the object's local coordinates
		#                              into world coordinates (translation, rotation, scale).
		# `gl_Position`: Final vertex position after transformations.
		vsCode = """
		in vec3 position;
		uniform mat4 projectionMatrix;
		uniform mat4 modelMatrix;

		void main()
		{
			gl_Position = projectionMatrix * modelMatrix * vec4(position, 1.0);
		}
		"""

		# Fragment Shader Code:
		# `fragColor`: Output, the final color of the fragment (pixel).
		fsCode = """
		out vec4 fragColor;

		void main()
		{
			fragColor = vec4(1.0, 1.0, 0.0, 1.0); // Simple yellow color for the triangle
		}
		"""

		# Initialize the GPU program using the vertex and fragment shaders.
		self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

		# Render settings:
		# Set the clear color for the framebuffer (background color).
		glClearColor(0.0, 0.0, 0.0, 1.0) # Black background
		
		# Enable depth testing. This ensures that fragments closer to the viewer
		# obscure fragments farther away, correctly rendering 3D objects.
		glEnable(GL_DEPTH_TEST)

		# Set up a single Vertex Array Object (VAO) to manage the attribute data.
		# This VAO will store the configuration for the triangle's position data.
		vaoRef = glGenVertexArrays(1)
		glBindVertexArray(vaoRef)

		# Position attributes:
		# Define the 3D coordinates for the vertices of a small triangle.
		positionData = [[ 0.0,  0.2, 0.0],
						[ 0.1, -0.2, 0.0],
						[-0.1, -0.2, 0.0]]

		# Store the number of vertices; used for drawing.
		self.vertexCount = len(positionData)

		# Create an Attribute object for position data.
		positionAttribute = Attribute("vec3", positionData)
		# Associate this attribute with the "position" variable in the shader program.
		positionAttribute.associateVariable(self.programRef, "position")

		# Uniforms for matrices:
		# Model Matrix: Represents the object's position, rotation, and scale in the world.
		# Initially, translate the object slightly back along the Z-axis so it's visible
		# when perspective projection is applied.
		mMatrix = Matrix.makeTranslation(0, 0, -1)
		self.modelMatrix = Uniform("mat4", mMatrix)
		self.modelMatrix.locateVariable(self.programRef, "modelMatrix")

		# Projection Matrix: Transforms 3D view space coordinates into 2D screen coordinates.
		# makePerspective(fov=60, aspect=1, near=0.1, far=2)
		# The 'far' plane is set to 2 units for this example.
		pMatrix = Matrix.makePerspective(far=2)
		self.projectionMatrix = Uniform("mat4", pMatrix)
		self.projectionMatrix.locateVariable(self.programRef, "projectionMatrix")		

	def update(self):
		"""
		Called once per frame to render the scene and handle interactive transformations.
		This method updates the model matrix based on user input for global/local transformations
		and Z-axis movement, then renders the triangle.
		"""
		# Constants for movement and rotation speed.
		moveAmount = 0.005
		turnAmount = 0.01

		# --- Global Transformations (applied relative to the world coordinate system) ---
		# New transformations are pre-multiplied (matrix @ current_model_matrix).

		# Global Translation (W: Up, S: Down, A: Left, D: Right)
		if self.input.isKeyPressed("w"):
			# Move up (positive along y-axis in world space)
			m = Matrix.makeTranslation(0, moveAmount, 0)
			self.modelMatrix.data = m @ self.modelMatrix.data # Matrix multiplication using @ operator
															  
		if self.input.isKeyPressed("s"):
			# Move down (negative along y-axis in world space)
			m = Matrix.makeTranslation(0, -moveAmount, 0)
			self.modelMatrix.data = m @ self.modelMatrix.data

		if self.input.isKeyPressed("a"):
			# Move left (negative along x-axis in world space)
			m = Matrix.makeTranslation(-moveAmount, 0, 0)
			self.modelMatrix.data = m @ self.modelMatrix.data

		if self.input.isKeyPressed("d"):
			# Move right (positive along x-axis in world space)
			m = Matrix.makeTranslation(moveAmount, 0, 0)
			self.modelMatrix.data = m @ self.modelMatrix.data

		# Global Rotation (Q: Rotate Z-axis positive, E: Rotate Z-axis negative)
		if self.input.isKeyPressed("q"): 
			# Rotate around the world's Z-axis (counter-clockwise)
			m = Matrix.makeRotationZ(turnAmount)
			self.modelMatrix.data = m @ self.modelMatrix.data

		if self.input.isKeyPressed("e"): 
			# Rotate around the world's Z-axis (clockwise)
			m = Matrix.makeRotationZ(-turnAmount)
			self.modelMatrix.data = m @ self.modelMatrix.data

		# --- Local Transformations (applied relative to the object's current local coordinate system) ---
		# New transformations are post-multiplied (current_model_matrix @ new_transform).

		# Local Translation (I: Up, K: Down, J: Left, L: Right)
		if self.input.isKeyPressed("i"):
			# Move up along the object's local y-axis
			m = Matrix.makeTranslation(0, moveAmount, 0)
			self.modelMatrix.data = self.modelMatrix.data @ m 
															  
		if self.input.isKeyPressed("k"):
			# Move down along the object's local y-axis
			m = Matrix.makeTranslation(0, -moveAmount, 0)
			self.modelMatrix.data = self.modelMatrix.data @ m

		if self.input.isKeyPressed("j"):
			# Move left along the object's local x-axis
			m = Matrix.makeTranslation(-moveAmount, 0, 0)
			self.modelMatrix.data = self.modelMatrix.data @ m

		if self.input.isKeyPressed("l"):
			# Move right along the object's local x-axis
			m = Matrix.makeTranslation(moveAmount, 0, 0)
			self.modelMatrix.data = self.modelMatrix.data @ m

		# Local Rotation (U: Rotate Z-axis positive, O: Rotate Z-axis negative)
		if self.input.isKeyPressed("u"): 
			# Rotate around the object's local Z-axis (counter-clockwise)
			m = Matrix.makeRotationZ(turnAmount)
			self.modelMatrix.data = self.modelMatrix.data @ m

		if self.input.isKeyPressed("o"): 
			# Rotate around the object's local Z-axis (clockwise)
			m = Matrix.makeRotationZ(-turnAmount)
			self.modelMatrix.data = self.modelMatrix.data @ m

		# --- Projection (Movement along the Z-axis) ---
		# Moving along the Z-axis (depth) affects perspective. "Global" multiplication order is used here.
		# Z: Move further away (negative Z), X: Move closer (positive Z)
		if self.input.isKeyPressed("z"):
			# Move further away from the viewer along the world's Z-axis
			m = Matrix.makeTranslation(0, 0, -moveAmount)
			self.modelMatrix.data = m @ self.modelMatrix.data

		if self.input.isKeyPressed("x"):
			# Move closer to the viewer along the world's Z-axis
			m = Matrix.makeTranslation(0, 0, moveAmount)
			self.modelMatrix.data = m @ self.modelMatrix.data

		# --- Rendering ---
		# Clear the color buffer (background) and the depth buffer (for 3D ordering).
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		# Activate the shader program for drawing.
		glUseProgram(self.programRef)

		# Upload the updated projection and model matrices to their uniform locations in the shader.
		self.projectionMatrix.uploadData()
		self.modelMatrix.uploadData()

		# Draw the triangle using GL_TRIANGLES primitive type.
		glDrawArrays( GL_TRIANGLES, 0, self.vertexCount)

# Create an instance of the Test class and run the application.
Test().run()