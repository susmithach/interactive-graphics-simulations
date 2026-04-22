from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from OpenGL.GL import *

# render a triangle and a square
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

		# render settings
		glPointSize( 20 )

		## Triangle ##
		self.vaoTri = glGenVertexArrays(1)
		glBindVertexArray(self.vaoTri)
		positionDataTri = [[-0.5, 0.8, 0.0],
						   [-0.2, 0.2, 0.0],
						   [-0.8, 0.2, 0.0]]

		positionAttributeTri = Attribute("vec3", positionDataTri)
		positionAttributeTri.associateVariable(self.programRef, "position")
		self.vertexCountTri = len(positionDataTri)

		## Square ##
		self.vaoSq = glGenVertexArrays(1)
		glBindVertexArray(self.vaoSq)
		positionDataSq = [[0.8, 0.8, 0.0],
						  [0.8, 0.2, 0.0],
						  [0.2, 0.2, 0.0],
						  [0.2, 0.8, 0.0]]
		positionAttributeSq = Attribute("vec3", positionDataSq)
		positionAttributeSq.associateVariable(self.programRef, "position")
		self.vertexCountSq = len(positionDataSq)


	def update(self):
		"""
		Called once per frame to render the scene. This method draws multiple objects
		(a triangle and a square) by binding their respective VAOs.
		"""
		# Tell OpenGL to use the compiled shader program for all drawing operations.
		glUseProgram( self.programRef )

		# --- Draw Triangle ---
		# Bind the VAO that contains the triangle's vertex data and attribute configurations.
		glBindVertexArray( self.vaoTri )
		# Draw the triangle's vertices as individual points.
		glDrawArrays( GL_POINTS, 0, self.vertexCountTri)
		# Draw the triangle's vertices as a closed line loop.
		glDrawArrays( GL_LINE_LOOP, 0, self.vertexCountTri)

		# --- Draw Square ---
		# Bind the VAO that contains the square's vertex data and attribute configurations.
		glBindVertexArray( self.vaoSq )
		# Draw the square's vertices as a closed line loop.
		glDrawArrays( GL_LINE_LOOP, 0, self.vertexCountSq)

# Run the program
Test().run()







