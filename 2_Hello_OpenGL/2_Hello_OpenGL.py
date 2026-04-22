# Import necessary modules
from core.base import Base
from core.openGLUtils import OpenGLUtils
from OpenGL import GL

# Extend the Base class to create a custom test application
class Test(Base):
    # Method to initialize the game
    def initialize(self):
        print("Initializing...")

        # Define vertex position coordinates
        x = -.5
        y = 0.
        z = 0

        # Define fragment color components
        r = 1.0
        g = 0.5
        b = 0.0

        # Vertex shader code: sets the position of the vertex
        vertexShaderCode = """
        void main() {
            gl_Position = vec4(%.2f, %.2f, %.2f, 1.0);
        }
        """ % (x, y, z)

        # Fragment shader code: sets the color of the fragment
        fragmentShaderCode = """
        out vec4 fragColor;
        void main() {            
            fragColor = vec4(%.2f, %.2f, %.2f, 1.0);
        }
        """ % (r, g, b)

        # Initialize the shader program with vertex and fragment shaders
        self.programRef = OpenGLUtils.initializeProgram(vertexShaderCode, 
                                                        fragmentShaderCode)

        # Generate and bind a Vertex Array Object (VAO)
        vaoRef = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vaoRef)

        # Set the point size for rendering
        GL.glPointSize(100.0)

    # Method to update the game state and render
    def update(self):
        # Use the compiled shader program
        GL.glUseProgram(self.programRef)
        # Draw a single point
        GL.glDrawArrays(GL.GL_POINTS, 0, 1)

# Create an instance of the Test class and run the application
test = Test()
test.run()