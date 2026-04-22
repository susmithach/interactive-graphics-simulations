from core.object3D import Object3D
from OpenGL.GL import glGenVertexArrays, glBindVertexArray, GL_TRIANGLES

class Mesh(Object3D):
    """
    Represents a renderable 3D object in the scene.
    A Mesh combines a Geometry object (vertex data) and a Material object (shader program and rendering settings).
    It manages the Vertex Array Object (VAO) and associates geometry attributes with shader variables.
    """
    def __init__(self, geometry, material):
        """
        Initializes a Mesh object.
        Args:
            geometry (Geometry): The geometry (vertex data) for this mesh.
            material (Material): The material (shader and rendering settings) for this mesh.
        """
        super().__init__()

        self.geometry = geometry
        self.material = material

        # Should this object be rendered?
        self.visible = True

        # Set up associations between attributes in geometry and 
        # shader variables in material
        self.vaoRef = glGenVertexArrays(1)
        glBindVertexArray(self.vaoRef)

        for variableName, attributionObject in geometry.attributes.items():
            attributionObject.associateVariable(material.programRef, variableName)

        # Unbind the VAO
        glBindVertexArray(0)
