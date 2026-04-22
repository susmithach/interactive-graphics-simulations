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
from geometry.boxGeometry import BoxGeometry
from math import pi

from material.surfaceBasicMaterial import SurfaceBasicMaterial

def is_colliding(pos_a, size_a, pos_b, size_b):
      return (
          abs(pos_a[0] - pos_b[0]) < (size_a[0] + size_b[0]) / 2 and
          abs(pos_a[1] - pos_b[1]) < (size_a[1] + size_b[1]) / 2 and
          abs(pos_a[2] - pos_b[2]) < (size_a[2] + size_b[2]) / 2
      )

def is_inside_floor(pos, x_limit, z_limit):
      return (
          -x_limit <= pos[0] <= x_limit and
          -z_limit <= pos[2] <= z_limit
      )

class Test(Base):

    def initialize(self):
        print("Initializing term project scene...")

        self.render = Render()
        self.scene = Scene()
        self.camera = Camera()

        self.camera.setPosition(1.8, 2.4, 7)
        self.camera.rotateY(0.18)
        self.camera.rotateX(-0.35)

        base_dir = Path(__file__).resolve().parent

        player_texture_path = base_dir/"img"/"earth_8k.jpg"

        player_geometry = SphereGeometry(radius=0.6)
        player_texture = Texture(str(player_texture_path))
        player_material = TextureMaterial(player_texture)

        self.player = Mesh(player_geometry, player_material)
        self.player.setPosition(0, -0.4, 2)
        self.scene.add(self.player)

        floor_geometry = RectangleGeometry(width=10, height=12)
        floor_material = SurfaceBasicMaterial({"baseColor": [0.45, 0.45, 0.45]})

        self.floor = Mesh(floor_geometry, floor_material)
        self.floor.rotateX(-pi / 2)
        self.floor.setPosition(0, -1, 0)
        self.scene.add(self.floor)

        wall_geometry = BoxGeometry(width=3, height=1.5, depth=0.7)
        wall_material = SurfaceBasicMaterial({"baseColor": [0.8, 0.15, 0.12]})

        self.wall = Mesh(wall_geometry, wall_material)
        self.wall.setPosition(0, -0.25, -3)
        self.scene.add(self.wall)

        self.player_speed = 0.05
        self.player_size = [1.2, 1.2, 1.2]
        self.wall_size = [3, 1.5, 0.7]
        self.floor_x_limit = 4.4
        self.floor_z_limit = 5.4
        

    def update(self):
        dx = 0
        dz = 0

        if self.input.isKeyPressed("w"):
            dz -= self.player_speed
        if self.input.isKeyPressed("s"):
            dz += self.player_speed
        if self.input.isKeyPressed("a"):
            dx -= self.player_speed
        if self.input.isKeyPressed("d"):
            dx += self.player_speed

        current_position = self.player.getPosition()
        proposed_position = [
            current_position[0] + dx,
            current_position[1],
            current_position[2] + dz
        ]

        blocked_by_wall = is_colliding(
            proposed_position,
            self.player_size,
            self.wall.getPosition(),
            self.wall_size
        )

        inside_floor = is_inside_floor(
            proposed_position,
            self.floor_x_limit,
            self.floor_z_limit
        )

        if inside_floor and not blocked_by_wall:
            self.player.setPosition(
                proposed_position[0],
                proposed_position[1],
                proposed_position[2]
            )
    
        self.player.rotateY(1/120)
        self.player.rotateX(1/180)
        self.render.render(self.scene, self.camera)


Test().run()