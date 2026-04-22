from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from OpenGL.GL import *

"""
This script demonstrates a basic OpenGL application to render a triangle outline.
It sets up vertex data, compiles shaders, and draws the triangle as a line loop.
"""

class Test( Base ):
	"""
	Main class for the OpenGL application, inheriting from Base.
	Handles initialization (setting up shaders, VAOs, attributes) and rendering (update).
	"""

	def initialize( self ):
		"""
		Initializes the OpenGL program, including shaders, vertex array objects (VAOs),
		and vertex attributes.
		"""
		print("Initializing program for drawing triangles...")

		# Vertex Shader Code: Defines how vertices are transformed.
		# `position` is an incoming 3D vector from the buffer.
		# `gl_Position` is a built-in output variable that sets the final vertex position.
		vsCode="""
		in vec3 position; // get incoming data from the buffer

		void main()
		{
			gl_Position = vec4(position.x, position.y, position.z, 1.0);
		}
		"""

		# Fragment Shader Code: Defines the color of each pixel (fragment).
		# `fragColor` is an output variable that sets the final color of the fragment.
		fsCode="""
		out vec4 fragColor; 
		void main()
		{
			fragColor = vec4(0.1, 1.0, 1.0, 1.0); // Cyan color
		}
		"""

		# Initialize the shader program with the vertex and fragment shaders.
		self.programRef = OpenGLUtils.initializeProgram( vsCode, fsCode )

		# Render settings:
		# Set the point size for GL_POINTS primitive type.
		glPointSize( 20 )
		# Set the line width. Core profile only guarantees 1.0; larger values can cause GL_INVALID_VALUE.
		glLineWidth( 1 )

		# Set up Vertex Array Object (VAO):
		# A VAO stores the state of all vertex attribute lists.
		self.vaoRef = glGenVertexArrays(1) # Generate a unique ID for the VAO.
		glBindVertexArray(self.vaoRef)    # Bind the VAO to make it the active one.

		# Set up vertex attribute (position data):
		# Define the 3D coordinates for the vertices of the triangle.
		positionData = [[-0.5, 0.8, 0.0],
						[-0.2, 0.2, 0.0],
						[-0.8, 0.2, 0.0]]

		# Store the number of vertices; used for drawing.
		self.vertexCount = len(positionData)

		# Use the Attribute class to manage and associate the position data.
		# "vec3" specifies that each vertex has 3 components.
		positionAttribute = Attribute("vec3", positionData)
		# Associate this attribute with the "position" variable in the shader program.
		positionAttribute.associateVariable( self.programRef, "position")

	def update( self ):
		"""
		Called once per frame to render the scene.
		"""
		# Tell OpenGL to use the compiled shader program.
		glUseProgram( self.programRef )

		# Bind the VAO that contains the vertex data and attribute configurations.
		# Optional for this example since we only have one VAO and it is already bound.
		glBindVertexArray(self.vaoRef)
		
		# Draw the vertices as a line loop (connects first to last vertex).
		# GL_POINTS would draw individual points.
		# GL_LINE_LOOP connects vertices to form a closed loop.
		glDrawArrays( GL_LINE_LOOP, 0, self.vertexCount)

# Create an instance of the Test class and run the application.
Test().run()
