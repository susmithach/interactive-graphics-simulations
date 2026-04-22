from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from OpenGL.GL import *

# render six points in a hexagon arrangment
class Test( Base ):

	def initialize( self ):
		print("Initializing program for drawing triangles...")

		# shader code
		vsCode="""
		in vec3 position; // get incoming data from the buffer

		void main()
		{
			gl_Position = vec4(position.x, position.y, position.z, 1.0);
		}
		"""

		fsCode="""
		out vec4 fragColor; 
		void main()
		{
			fragColor = vec4(0.1, 1.0, 1.0, 1.0);
		}
		"""

		self.programRef = OpenGLUtils.initializeProgram( vsCode, fsCode )

		glPointSize( 20 )


		# set up vertex array object
		vaoRef = glGenVertexArrays(1)
		glBindVertexArray(vaoRef)

		# set up vertex attribute
		positionData = [[0.8, 0.0, 0.0],
						[0.4, 0.6, 0.0],
						[-0.4, 0.6, 0.0],
						[-0.8, 0.0, 0.0],
						[-0.4, -0.6, 0.0],
						[0.4, -0.6, 0.0]]

		self.vertexCount = len(positionData)

		# use attribute class
		positionAttribute = Attribute("vec3", positionData)
		positionAttribute.associateVariable( self.programRef, "position")

	def update( self ):
		"""
		Called once per frame to render the scene. This method draws the hexagon
		using various OpenGL primitive types (currently GL_POINTS).
		"""
		# Tell OpenGL to use the compiled shader program.
		glUseProgram( self.programRef )

		# Draw the vertices using the specified primitive type.
		# Uncomment different glDrawArrays calls to experiment with different rendering modes:
		
		# GL_POINTS: Draws individual points at each vertex.
		glDrawArrays( GL_POINTS, 0, self.vertexCount)
		# GL_LINE_LOOP: Draws a connected sequence of line segments, closing the loop.
		# glDrawArrays( GL_LINE_LOOP, 0, self.vertexCount)
		# GL_LINES: Draws independent pairs of line segments.
		# glDrawArrays( GL_LINES, 0, self.vertexCount)
		# GL_TRIANGLES: Draws independent triangles; each three vertices form a triangle.
		# glDrawArrays( GL_TRIANGLES, 0, self.vertexCount )
		# GL_TRIANGLE_FAN: Draws a connected fan of triangles; first vertex is common to all.
		# glDrawArrays( GL_TRIANGLE_FAN, 0, self.vertexCount )
# Create test instance
Test().run()

