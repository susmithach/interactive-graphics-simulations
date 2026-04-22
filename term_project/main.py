from core.base import Base
from core.render import Render
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from pathlib import Path
from core.texture import Texture
from material.textureMaterial import TextureMaterial
from geometry.sphereGeometry import SphereGeometry
from geometry.rectangleGeometry import RectangleGeometry
from math import pi

from material.surfaceBasicMaterial import SurfaceBasicMaterial



class Test(Base):
    def initialize(self):
        print("Initializing term project scene...")

        self.render = Render()
        self.scene = Scene()
        self.camera = Camera()

        self.camera.setPosition(0, 2.5, 7)
        self.camera.rotateX(-0.35)

        base_dir = Path(__file__).resolve().parent

        player_texture_path = base_dir/"img"/"earth_8k.jpg"

        player_geometry = SphereGeometry(radius=1)
        player_texture = Texture(str(player_texture_path))
        player_material = TextureMaterial(player_texture)

        self.player = Mesh(player_geometry, player_material)
        self.scene.add(self.player)

        floor_geometry = RectangleGeometry(width=10, height=10)
        floor_material = SurfaceBasicMaterial({"baseColor": [0.45, 0.45, 0.45]})

        self.floor = Mesh(floor_geometry, floor_material)
        self.floor.rotateX(-pi / 2)
        self.floor.setPosition(0, -1, 0)
        self.scene.add(self.floor)

    def update(self):
        self.player.rotateY(1/120)
        self.player.rotateX(1/180)
        self.render.render(self.scene, self.camera)


Test().run()