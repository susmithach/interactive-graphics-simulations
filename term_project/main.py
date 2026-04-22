from core.base import Base
from core.render import Render
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from pathlib import Path
from core.texture import Texture
from material.textureMaterial import TextureMaterial
from geometry.sphereGeometry import SphereGeometry



class Test(Base):
    def initialize(self):
        print("Initializing term project scene...")

        self.render = Render()
        self.scene = Scene()
        self.camera = Camera()

        self.camera.setPosition(0, 0, 5)

        base_dir = Path(__file__).resolve().parent
        texture_path = base_dir / "img" / "earth_8k.jpg"

        geometry = SphereGeometry(radius=1)
        texture = Texture(str(texture_path))
        material = TextureMaterial(texture)

        self.player = Mesh(geometry, material)
        self.scene.add(self.player)

    def update(self):
        self.player.rotateY(1/120)
        self.player.rotateX(1/180)
        self.render.render(self.scene, self.camera)


Test().run()