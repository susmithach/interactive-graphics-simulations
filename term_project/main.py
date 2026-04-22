from core.base import Base
from core.render import Render
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh

from geometry.boxGeometry import BoxGeometry

from material.surfaceBasicMaterial import SurfaceBasicMaterial


class Test(Base):
    def initialize(self):
        print("Initializing term project scene...")

        self.render = Render()
        self.scene = Scene()
        self.camera = Camera()

        self.camera.setPosition(0, 0, 5)

        geometry = BoxGeometry()
        material = SurfaceBasicMaterial({"useVertexColors": 1})

        self.cube = Mesh(geometry, material)
        self.scene.add(self.cube)

    def update(self):
        self.cube.rotateY(1/120)
        self.cube.rotateX(1/180)
        self.render.render(self.scene, self.camera)


Test().run()