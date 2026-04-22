from core.matrix import Matrix

class Object3D(object):
    """
    Base class for all objects in the 3D scene.
    Manages hierarchical transformations, parent-child relationships,
    and provides methods for common transformations like translation, rotation, and scaling.
    """

    def __init__(self):
        # The local transformation matrix for this object relative to its parent.
        self.transform = Matrix.makeIdentity()
        # Reference to the parent object in the scene graph.
        self.parent = None
        # List of child objects attached to this object.
        self.children = [] 

    ## add child/parent ##
    def add(self, child):
        """
        Adds a child object to this object.
        The child's parent is set to this object.
        Args:
            child (Object3D): The child object to add.
        """
        self.children.append(child)
        child.parent = self

    def remove(self, child):
        """
        Removes a child object from this object.
        The child's parent is set to None.
        Args:
            child (Object3D): The child object to remove.
        """
        self.children.remove(child)
        child.parent = None

    def getWorldMatrix(self):
        """
        Calculates the world matrix for this object by concatenating
        its local transform with the world matrix of its parent (recursively).
        Returns:
            np.array: The 4x4 world transformation matrix.
        """
        if self.parent == None:
            return self.transform
        else:
            return self.parent.getWorldMatrix() @ self.transform

    def getDescendentList(self):
        """
        Returns a list of all descendents of this object, including itself,
        in a breadth-first manner.
        Returns:
            list: A list of Object3D instances.
        """
        descendents = []

        nodesToProcess = [self]
        while len(nodesToProcess)>0:
            node = nodesToProcess.pop(0)
            descendents.append(node)
            nodesToProcess = node.children + nodesToProcess

        return descendents


    def applyMatrix(self, matrix, localCoord=True):
        """
        Applies a given matrix to the object's transformation.
        Args:
            matrix (np.array): The 4x4 matrix to apply.
            localCoord (bool): If True, apply the matrix in local coordinates (post-multiplication).
                               If False, apply in world coordinates (pre-multiplication).
        """
        if localCoord:
            self.transform = self.transform @ matrix
        else:
            self.transform = matrix @ self.transform

    def translate(self, x, y, z, localCoord=True):
        """
        Translates the object by the specified offsets.
        Args:
            x (float): Translation along the x-axis.
            y (float): Translation along the y-axis.
            z (float): Translation along the z-axis.
            localCoord (bool): If True, apply in local coordinates.
        """
        m = Matrix.makeTranslation(x, y, z)
        self.applyMatrix(m, localCoord)

    def rotateX(self, angle, localCoord=True):
        """
        Rotates the object around the X-axis.
        Args:
            angle (float): Rotation angle in radians.
            localCoord (bool): If True, apply in local coordinates.
        """
        m = Matrix.makeRotationX(angle)
        self.applyMatrix(m, localCoord)

    def rotateY(self, angle, localCoord=True):
        """
        Rotates the object around the Y-axis.
        Args:
            angle (float): Rotation angle in radians.
            localCoord (bool): If True, apply in local coordinates.
        """
        m = Matrix.makeRotationY(angle)
        self.applyMatrix(m, localCoord)

    def rotateZ(self, angle, localCoord=True):
        """
        Rotates the object around the Z-axis.
        Args:
            angle (float): Rotation angle in radians.
            localCoord (bool): If True, apply in local coordinates.
        """
        m = Matrix.makeRotationZ(angle)
        self.applyMatrix(m, localCoord)        

    def scale(self, s, localCoord=True):
        """
        Scales the object uniformly by a factor 's'.
        Args:
            s (float): The scaling factor.
            localCoord (bool): If True, apply in local coordinates.
        """
        m = Matrix.makeScale(s)
        self.applyMatrix(m, localCoord)    


    def getPosition(self):
        """
        Returns the current position (translation) of the object from its transform matrix.
        Returns:
            list: A list [x, y, z] representing the object's position.
        """
        return [ self.transform.item((0,3)),
                 self.transform.item((1,3)),
                 self.transform.item((2,3)) ]

    def setPosition(self, x, y, z):
        """
        Sets the position (translation) of the object in its transform matrix.
        Args:
            x (float): New x-coordinate.
            y (float): New y-coordinate.
            z (float): New z-coordinate.
        """
        self.transform[0, 3] = x
        self.transform[1, 3] = y
        self.transform[2, 3] = z

