from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from OpenGL.GL import *

"""
Assignment2: Drawing Multiple Geometric Shapes with Unique Colors

- 4 distinct shapes
- 4 distinct VAOs
- Each VAO has both attributes:
    * position (vec3)
    * vertexColor (vec3)
- Shaders accept per-vertex color
"""

class Test(Base):

    def initialize(self):
        print("Initializing program for multiple shapes with unique colors...")

        # Vertex shader:
        # Receives position and vertexColor as attributes.
        # Passes the color to the fragment shader.
        vsCode = """
        in vec3 position;
        in vec3 vertexColor;
        out vec3 color;

        void main()
        {
            gl_Position = vec4(position, 1.0);
            color = vertexColor;
        }
        """

        # Fragment shader:
        # Uses the color from the vertex shader.
        fsCode = """
        in vec3 color;
        out vec4 fragColor;

        void main()
        {
            fragColor = vec4(color, 1.0);
        }
        """

        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        # Render settings
        glClearColor(0.06, 0.06, 0.08, 1.0)
        glPointSize(10)
        min_w, max_w = glGetFloatv(GL_ALIASED_LINE_WIDTH_RANGE)
        safe_w = min(max(1.0, float(min_w)), float(max_w))   # always valid
        glLineWidth(safe_w)

        # Shape 1: Triangle
        self.vaoShape1 = glGenVertexArrays(1)
        glBindVertexArray(self.vaoShape1)

        # Triangle vertex positions
        positionData1 = [
            [-0.75,  0.75, 0.0],
            [-0.55,  0.25, 0.0],
            [-0.95,  0.25, 0.0],
        ]
        colorData1 = [[1.0, 0.0, 0.0]] * len(positionData1)

        Attribute("vec3", positionData1).associateVariable(self.programRef, "position")
        Attribute("vec3", colorData1).associateVariable(self.programRef, "vertexColor")
        self.vertexCountShape1 = len(positionData1)

        # Shape 2: Square
        self.vaoShape2 = glGenVertexArrays(1)
        glBindVertexArray(self.vaoShape2)

        positionData2 = [
            [0.25, 0.75, 0.0],
            [0.85, 0.75, 0.0],
            [0.85, 0.25, 0.0],
            [0.25, 0.25, 0.0],
        ]
        colorData2 = [[0.0, 1.0, 0.0]] * len(positionData2)

        Attribute("vec3", positionData2).associateVariable(self.programRef, "position")
        Attribute("vec3", colorData2).associateVariable(self.programRef, "vertexColor")
        self.vertexCountShape2 = len(positionData2)

        # Shape 3: Pentagon
        self.vaoShape3 = glGenVertexArrays(1)
        glBindVertexArray(self.vaoShape3)

        positionData3 = [
            [-0.75, -0.20, 0.0],
            [-0.50, -0.45, 0.0],
            [-0.60, -0.80, 0.0],
            [-0.90, -0.80, 0.0],
            [-0.98, -0.45, 0.0],
        ]
        colorData3 = [[0.0, 0.4, 1.0]] * len(positionData3)

        Attribute("vec3", positionData3).associateVariable(self.programRef, "position")
        Attribute("vec3", colorData3).associateVariable(self.programRef, "vertexColor")
        self.vertexCountShape3 = len(positionData3)

        # Shape 4: Points cluster
        self.vaoShape4 = glGenVertexArrays(1)
        glBindVertexArray(self.vaoShape4)

        positionData4 = [
            [0.45, -0.25, 0.0],
            [0.70, -0.25, 0.0],
            [0.55, -0.45, 0.0],
            [0.82, -0.55, 0.0],
            [0.62, -0.75, 0.0],
            [0.35, -0.60, 0.0],
        ]
        colorData4 = [[1.0, 1.0, 0.0]] * len(positionData4)

        Attribute("vec3", positionData4).associateVariable(self.programRef, "position")
        Attribute("vec3", colorData4).associateVariable(self.programRef, "vertexColor")
        self.vertexCountShape4 = len(positionData4)

        # Unbinding VAO
        glBindVertexArray(0)

    def update(self):
        # Clear the screen each frame
        glClear(GL_COLOR_BUFFER_BIT)

        # Use the shader program once
        glUseProgram(self.programRef)

        # Shape 1: Triangle
        glBindVertexArray(self.vaoShape1)
        glDrawArrays(GL_TRIANGLES, 0, self.vertexCountShape1)

        # Shape 2: Square
        glBindVertexArray(self.vaoShape2)
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.vertexCountShape2)

        # Shape 3: Pentagon
        glBindVertexArray(self.vaoShape3)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCountShape3)

        # Shape 4: Points
        glBindVertexArray(self.vaoShape4)
        glDrawArrays(GL_POINTS, 0, self.vertexCountShape4)

        # Unbind
        glBindVertexArray(0)

# Run the program
Test().run()
