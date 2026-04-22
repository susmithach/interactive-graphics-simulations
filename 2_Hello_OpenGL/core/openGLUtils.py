from OpenGL import GL 

class OpenGLUtils:
    # Static method to initialize and compile a shader
    @staticmethod
    def initializeShader(shaderCode, shaderType):
        # Add OpenGL version directive to the shader code
        shaderCode = "#version 330\n" + shaderCode

        # Create a new shader object
        shaderRef = GL.glCreateShader(shaderType)
        # Set the shader source code
        GL.glShaderSource(shaderRef, shaderCode)
        # Compile the shader
        GL.glCompileShader(shaderRef)

        # Return the shader reference
        return shaderRef

    # Static method to initialize and link a shader program
    @staticmethod
    def initializeProgram(vertexShaderCode, fragmentShaderCode):
        # Compile vertex shader
        vertexShaderRef = OpenGLUtils.initializeShader(vertexShaderCode,
                                                        GL.GL_VERTEX_SHADER)
        # Compile fragment shader
        fragmentShaderRef = OpenGLUtils.initializeShader(fragmentShaderCode,
                                                        GL.GL_FRAGMENT_SHADER)

        # Create a new shader program object
        programRef = GL.glCreateProgram()
        # Attach vertex and fragment shaders to the program
        GL.glAttachShader(programRef, vertexShaderRef)
        GL.glAttachShader(programRef, fragmentShaderRef)
        # Link the shader program
        GL.glLinkProgram(programRef)

        # Return the program reference
        return programRef