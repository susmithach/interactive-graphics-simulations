import numpy as np 
from OpenGL.GL import * 

class Attribute(object):
    def __init__(self, dataType, data):
        self.dataType = dataType # int, vec2, vec3, vec4
        self.data = data # data to be stored in the buffer

        # create the buffer
        self.bufferRef = glGenBuffers(1)

        # upload data
        self.uploadData() 
    
    def uploadData(self):
        data = np.array( self.data ).astype(np.float32)

        # bind buffer to target
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)
        # upload
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)

    def associateVariable(self, programRef, variableName):
        variableRef = glGetAttribLocation(programRef, variableName)

        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)

        if self.dataType == "int":
            glVertexAttribPointer(variableRef, 1, GL_INT, False, 0, None)
        elif self.dataType == "vec2":
            glVertexAttribPointer(variableRef, 2, GL_FLOAT, False, 0, None)
        elif self.dataType == "vec3":
            glVertexAttribPointer(variableRef, 3, GL_FLOAT, False, 0, None)
        elif self.dataType == "vec4":
            glVertexAttribPointer(variableRef, 4, GL_FLOAT, False, 0, None)
        elif self.dataType == "float":
            glVertexAttribPointer(variableRef, 1, GL_FLOAT, False, 0, None)
        
        glEnableVertexAttribArray(variableRef)
