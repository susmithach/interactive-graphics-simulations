from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from OpenGL.GL import *

"""
This script demonstrates how to pass per-vertex color data from the application
 to the shaders and use it to render a hexagon with a gradient of colors.
It highlights the use of an additional vertex attribute for color.
"""

class Test( Base ):
	"""
	Main class for the OpenGL application, inheriting from Base.
	Handles initialization (setting up shaders with color input, VAO, attributes)
	and rendering.
	"""

	def initialize( self ):
		"""
		Initializes the OpenGL program, including shaders configured for color input,
		vertex array object (VAO), and position and color attributes.
		"""
		print("Initializing program...")

		# Vertex Shader Code: Transforms vertices and passes color to the fragment shader.
		# `position` (vec3): Incoming vertex position from buffer.
		# `vertexColor` (vec3): Incoming per-vertex color from buffer.
		# `color` (vec3): Output to fragment shader, interpolated across the primitive.
		vsCode="""
		in vec3 position;
		in vec3 vertexColor;
		out vec3 color;

		void main()
		{
			gl_Position = vec4(position.x, position.y, position.z, 1.0);
			color = vertexColor;
		}
		"""

		# Fragment Shader Code: Determines the final color of each pixel.
		# `color` (vec3): Incoming interpolated color from the vertex shader.
		# `fragColor` (vec4): Output, the final color of the fragment (pixel).
		fsCode="""
		in vec3 color;
		out vec4 fragColor; 

		void main()
		{
			fragColor = vec4(color.r, color.g, color.b, 1.0);
		}
		"""

		# Initialize the shader program with the vertex and fragment shaders.
		self.programRef = OpenGLUtils.initializeProgram( vsCode, fsCode )

		# Render settings: Set the point size for GL_POINTS primitive type.
		glPointSize( 20 )

		# Set up Vertex Array Object (VAO):
		# A VAO stores the state of all vertex attribute lists. It encapsulates
		# the configuration of vertex data for a single object.
		vaoRef = glGenVertexArrays(1) # Generate a unique ID for the VAO.
		glBindVertexArray(vaoRef)    # Bind the VAO to make it the active one.

		# Set up position attribute:
		# Define the 3D coordinates for the vertices of the hexagon.
		positionData = [[0.8, 0.0, 0.0],
						[0.4, 0.6, 0.0],
						[-0.4, 0.6, 0.0],
						[-0.8, 0.0, 0.0],
						[-0.4, -0.6, 0.0],
						[0.4, -0.6, 0.0]]

		# Store the number of vertices; used for drawing.
		self.vertexCount = len(positionData)

		# Use the Attribute class to manage and associate the position data.
		# "vec3" specifies that each vertex has 3 components.
		positionAttribute = Attribute("vec3", positionData)
		# Associate this attribute with the "position" variable in the shader program.
		positionAttribute.associateVariable( self.programRef, "position")

		# Set up color attribute:
		# Define a unique 3D color vector [R, G, B] for each vertex.
		colorData = [[1.0, 0.0, 0.0], # Red
					 [1.0, 0.5, 0.0], # Orange
					 [1.0, 1.0, 0.0], # Yellow
					 [0.0, 1.0, 0.0], # Green
					 [0.0, 0.0, 1.0], # Blue
					 [0.5, 0.0, 1.0]] # Indigo
		# Use the Attribute class to manage and associate the color data.
		colorAttribute = Attribute("vec3", colorData)
		# Associate this attribute with the "vertexColor" variable in the shader program.
		colorAttribute.associateVariable( self.programRef, "vertexColor" )

	def update( self ):
		"""
		Called once per frame to render the scene. This method draws the hexagon
		with per-vertex colors.
		"""
		# Tell OpenGL to use the compiled shader program.
		glUseProgram( self.programRef )

		# Draw the vertices using the specified primitive type.
		# Uncomment different glDrawArrays calls to experiment with different rendering modes:
		# GL_POINTS: Draws individual points at each vertex.
		# glDrawArrays( GL_POINTS, 0, self.vertexCount)
		# GL_LINE_LOOP: Draws a connected sequence of line segments, closing the loop.
		# glDrawArrays( GL_LINE_LOOP, 0, self.vertexCount)
		# GL_LINES: Draws independent pairs of line segments.
		# glDrawArrays( GL_LINES, 0, self.vertexCount)
		# GL_TRIANGLES: Draws independent triangles; each three vertices form a triangle.
		# glDrawArrays( GL_TRIANGLES, 0, self.vertexCount )
		# GL_TRIANGLE_FAN: Draws a connected fan of triangles; first vertex is common to all.
		glDrawArrays( GL_TRIANGLE_FAN, 0, self.vertexCount )
		
# Create an instance of the Test class and run the application.
Test().run()
