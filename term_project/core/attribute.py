import numpy as np
from OpenGL.GL import *

class Attribute( object ):
	"""
	Manages vertex attribute data (e.g., positions, colors, normals) for OpenGL.
	This class handles uploading data to a GPU buffer and associating it with
	a variable in a shader program.
	"""

	def __init__( self, dataType, data ):
		"""
		Initializes an Attribute object.

		Args:
			dataType (str): The type of data (e.g., "int", "float", "vec2", "vec3", "vec4").
			data (list): The raw data to be stored in the buffer (e.g., a list of vertex coordinates).
		"""
		# data type: int, float, vec2, vec3, vec4 (for now)
		self.dataType = dataType

		# data to be stored in the buffer
		self.data = data

		# reference to available GPU buffers (unique ID for this buffer)
		self.bufferRef = glGenBuffers(1)

		# upload data immediately upon initialization
		self.uploadData()

	def uploadData( self ):
		"""
		Uploads the attribute data to the GPU buffer.
		"""
		# convert data to a numpy array with float32 type
		data = np.array( self.data ).astype( np.float32 )

		# bind the buffer to the GL_ARRAY_BUFFER target
		glBindBuffer( GL_ARRAY_BUFFER, self.bufferRef )

		# upload data to the currently bound buffer (flatten data using .ravel() to convert 2D array to 1D array)
		# GL_STATIC_DRAW indicates that the data will not be changed often
		glBufferData( GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)

	def associateVariable( self, programRef, variableName):
		"""
		Associates this buffer's data with a variable in a shader program.

		Args:
			programRef (int): The ID of the shader program.
			variableName (str): The name of the attribute variable in the shader
								(e.g., "position", "vertexColor").
		"""
		# get the reference (memory location) for the program variable with a given name
		variableRef = glGetAttribLocation( programRef, variableName )

		# if the variable does not exist in the shader, do nothing
		if variableRef == -1:
			return 

		# set up the association
		# bind the buffer to the GL_ARRAY_BUFFER target again
		glBindBuffer( GL_ARRAY_BUFFER, self.bufferRef )

		# specify how the data in the currently bound buffer will be read
		# variableRef: index of the generic vertex attribute
		# size: number of components per generic vertex attribute (e.g., 3 for vec3)
		# type: data type of each component (e.g., GL_FLOAT)
		# normalized: whether integer data values should be normalized to [-1, 1] or [0, 1]
		# stride: byte offset between consecutive generic vertex attributes
		# pointer: offset of the first component of the first generic vertex attribute
		if self.dataType == "int":
			glVertexAttribPointer( variableRef, 1, GL_INT, False, 0, None )
		elif self.dataType == "float":
			glVertexAttribPointer( variableRef, 1, GL_FLOAT, False, 0, None )
		elif self.dataType == "vec2":
			glVertexAttribPointer( variableRef, 2, GL_FLOAT, False, 0, None )
		elif self.dataType == "vec3":
			glVertexAttribPointer( variableRef, 3, GL_FLOAT, False, 0, None )
		elif self.dataType == "vec4":
			glVertexAttribPointer( variableRef, 4, GL_FLOAT, False, 0, None )
		else:
			raise Exception("Unknown Attribute Type: " + self.dataType )

		# enable the generic vertex attribute array for the given variable reference
		glEnableVertexAttribArray( variableRef )