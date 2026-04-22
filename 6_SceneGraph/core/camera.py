from core.object3D import Object3D
from core.matrix import Matrix
from numpy.linalg import inv # for inverse of a matrix

class Camera(Object3D):
    """
    Represents a camera in the 3D scene, inheriting from Object3D.
    It manages the projection matrix and calculates the view matrix based on its world transformation.
    """

    def __init__(self, 
                 angleOfView=60,
                 aspectRatio=1,
                 near=0.1,
                 far=100):
        """
        Initializes the camera with projection parameters.
        Args:
            angleOfView (float): The vertical field of view in degrees.
            aspectRatio (float): The aspect ratio of the viewport (width / height).
            near (float): The distance to the near clipping plane.
            far (float): The distance to the far clipping plane.
        """
        super().__init__()

        # Projection matrix defines the camera's viewing frustum.
        self.projectionMatrix = Matrix.makePerspective(angleOfView, aspectRatio, near, far)

        # View matrix transforms world coordinates to camera coordinates.
        self.viewMatrix = Matrix.makeIdentity()

    def updateViewMatrix(self):
        """
        Calculates and updates the view matrix based on the inverse of the camera's world matrix.
        This effectively transforms objects from world space to camera's local space.
        """
        self.viewMatrix = inv(self.getWorldMatrix())
