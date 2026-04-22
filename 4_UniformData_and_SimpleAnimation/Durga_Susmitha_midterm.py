from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from OpenGL.GL import *

import random

"""
CSCI 5337 – Mid-Term Exam
Interactive Triangle with Keyboard Control

This program renders a single triangle that:
• Moves using the arrow keys
• Changes to a random color when the spacebar is pressed

The triangle's position and color are controlled using
uniform variables (translation and baseColor).
Keyboard input is handled through the updated Input class.
"""


class Test(Base):

    def initialize(self):
        print('Initializing keyboard-controlled triangle...')

        # Shader Setup
        # The vertex shader applies a translation offset to the triangle using a uniform variable.
        vsCode = """
        in vec3 position;
        uniform vec3 translation;

        void main()
        {
            vec3 pos = position + translation;
            gl_Position = vec4(pos, 1.0);
        }
        """

        # The fragment shader simply colors the triangle using the uniform baseColor.
        fsCode = """
        uniform vec3 baseColor;
        out vec4 fragColor;

        void main()
        {
            fragColor = vec4(baseColor, 1.0);
        }
        """

        # Compile and link shaders into a program
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        # Set a soft background color so the triangle stands out
        glClearColor(0.6, 0.8, 0.8, 1.0)

        # Geometry Setup (Single VAO)
        # Only one VAO is needed since we are drawing a single triangle.
        self.vaoRef = glGenVertexArrays(1)
        glBindVertexArray(self.vaoRef)

        # Base triangle centered at the origin
        positionData = [
            [0.0,  0.2, 0.0],
            [0.2, -0.2, 0.0],
            [-0.2, -0.2, 0.0]
        ]

        # Send vertex positions to GPU and link to shader
        Attribute('vec3', positionData).associateVariable(self.programRef, 'position')

        # Store number of vertices for rendering
        self.vertexCount = len(positionData)

        # Unbind VAO after setup (good practice)
        glBindVertexArray(0)

        # Uniform Variables
        # Translation controls triangle movement
        self.translation = Uniform('vec3', [0.0, 0.0, 0.0])
        self.translation.locateVariable(self.programRef, 'translation')

        # Base color controls triangle color
        # Start with red so movement is clearly visible
        self.baseColor = Uniform('vec3', [1.0, 0.0, 0.0])
        self.baseColor.locateVariable(self.programRef, 'baseColor')

        # Controls how fast the triangle moves per frame
        self.move_speed = 0.05

    def update(self):
        # Activate shader program
        glUseProgram(self.programRef)

        # Clear screen each frame
        glClear(GL_COLOR_BUFFER_BIT)

        # Keyboard Movement
        # isKeyPressed() stays True while the key is held down,allowing smooth movement.
        if self.input.isKeyPressed('up'):
            self.translation.data[1] += self.move_speed
        if self.input.isKeyPressed('down'):
            self.translation.data[1] -= self.move_speed
        if self.input.isKeyPressed('left'):
            self.translation.data[0] -= self.move_speed
        if self.input.isKeyPressed('right'):
            self.translation.data[0] += self.move_speed

        # Send updated position to GPU
        self.translation.uploadData()

        # Random Color Change
        # isKeyDown() returns True only on the frame the spacebar is first pressed.
        if self.input.isKeyDown('space'):
            self.baseColor.data = [
                random.uniform(0.0, 1.0),
                random.uniform(0.0, 1.0),
                random.uniform(0.0, 1.0)
            ]

        # Upload current color
        self.baseColor.uploadData()

        # Draw Triangle
        glBindVertexArray(self.vaoRef)
        glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)
        glBindVertexArray(0)


# Start the application
Test().run()