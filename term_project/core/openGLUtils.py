from OpenGL import GL

# static methods to load/compile OpenGL shaders
# later, link the shaders to create GPU programs

class OpenGLUtils(object):

	@staticmethod
	def initializeShader( shaderCode, shaderType ):

		# specify OpenGL version and additional requirements 
		#	for Window machine
		# extension = "#extension GL_ARB_shading_language_420pack: require \n"
		# shaderCode = "#version 130 \n" + extension + shaderCode

		# specify OpenGL version and additional requirements 
		#	for Mac 
		shaderCode = "#version 330\n" + shaderCode

		# create an empty shader object and return the reference 
		shaderRef = GL.glCreateShader( shaderType )
		# store source code in the shader
		GL.glShaderSource( shaderRef, shaderCode )
		# compile the source code
		GL.glCompileShader( shaderRef )

		##Error Checking##
		# query compilation status
		compileSuccess = GL.glGetShaderiv( shaderRef, GL.GL_COMPILE_STATUS )

		# if we got an error
		if not compileSuccess:
			# retrive error message
			errorMessage = GL.glGetShaderInfoLog( shaderRef ) # returns a byte string
			# free memory
			GL.glDeleteShader( shaderRef )
			# convert byte string to character string
			errorMessage = "\n" + errorMessage.decode("utf-8")
			# raise exception, stop the program, print error message
			raise Exception( errorMessage )

		# if compilation was successful
		return shaderRef

	@staticmethod
	def initializeProgram( vertexShaderCode, fragementShaderCode ):

		# Compile the two shaders and store the references
		vertexShaderRef = OpenGLUtils.initializeShader( vertexShaderCode, 
														GL.GL_VERTEX_SHADER )

		fragmentShaderRef = OpenGLUtils.initializeShader( fragementShaderCode, 
														  GL.GL_FRAGMENT_SHADER )

		# Create the empty program object
		programRef = GL.glCreateProgram()

		# Attach compiled shaders
		GL.glAttachShader( programRef, vertexShaderRef)
		GL.glAttachShader( programRef, fragmentShaderRef)

		# Link the shaders together
		GL.glLinkProgram( programRef )


		# Error checking
		linkSuccess = GL.glGetProgramiv( programRef, GL.GL_LINK_STATUS )

		if not linkSuccess:
			errorMessage = GL.glGetProgramInfoLog( programRef )
			GL.glDeleteProgram( programRef )
			errorMessage = "\n" + errorMessage.decode("utf-8")
			raise Exception( errorMessage )

		return programRef
        
