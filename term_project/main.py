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


# Checks whether two axis-aligned bounding boxes are overlapping.
# Each object is represented by its center position and its width, height, and depth.
def is_colliding(pos_a, size_a, pos_b, size_b):
      return (
          abs(pos_a[0] - pos_b[0]) < (size_a[0] + size_b[0]) / 2 and
          abs(pos_a[1] - pos_b[1]) < (size_a[1] + size_b[1]) / 2 and
          abs(pos_a[2] - pos_b[2]) < (size_a[2] + size_b[2]) / 2
      )

# Checks whether the player is still inside the visible floor area.
# This prevents the sphere from moving off the floor into the empty background.
def is_inside_floor(pos, x_limit, z_limit):
      return (
          -x_limit <= pos[0] <= x_limit and
          -z_limit <= pos[2] <= z_limit
      )

class Test(Base):

    def initialize(self):
        print("Initializing term project scene...")

        # Create the renderer, scene graph, and camera.
        # The renderer draws the scene from the camera's point of view.
        self.render = Render()
        self.scene = Scene()
        self.camera = Camera()
        # Position the camera above and behind the scene so the floor,
        # player, and obstacle are visible.
        self.camera.setPosition(1.8, 2.4, 7)
        self.camera.rotateY(0.18)
        self.camera.rotateX(-0.35)

        # Use the folder containing this file as the base path for loading images.
        # This makes the texture path work when the project is run
        base_dir = Path(__file__).resolve().parent

        # Create the player object as a textured sphere.
        # The Earth image is applied using TextureMaterial
        player_texture_path = base_dir/"img"/"earth_8k.jpg"

        player_geometry = SphereGeometry(radius=0.6)
        player_texture = Texture(str(player_texture_path))
        player_material = TextureMaterial(player_texture)

        self.player = Mesh(player_geometry, player_material)

        # The floor is at Y = -1. Since the sphere radius is 0.6,
        # the center is placed at -0.4 so the sphere sits on the floor.
        self.player.setPosition(0, -0.4, 2)
        self.scene.add(self.player)

        # Create a flat rectangular floor.
        # RectangleGeometry starts vertical in the XY plane, so it is rotated
        # around the X axis to lie flat on the XZ plane.
        floor_geometry = RectangleGeometry(width=10, height=12)
        floor_material = SurfaceBasicMaterial({"baseColor": [0.45, 0.45, 0.45]})

        self.floor = Mesh(floor_geometry, floor_material)
        self.floor.rotateX(-pi / 2)
        self.floor.setPosition(0, -1, 0)
        self.scene.add(self.floor)

        # Create a red wall obstacle.
        # The wall is a 3D box and will be used for collision detection.
        wall_geometry = BoxGeometry(width=3, height=1.5, depth=0.7)
        wall_material = SurfaceBasicMaterial({"baseColor": [0.8, 0.15, 0.12]})

        self.wall = Mesh(wall_geometry, wall_material)

        # The wall bottom sits on the floor.
         # Floor Y is -1 and wall height is 1.5, so center Y is -1 + 0.75 = -0.25.
        self.wall.setPosition(0, -0.25, -3)
        self.scene.add(self.wall)

        # Movement speed is measured in scene units per frame.
        self.player_speed = 0.05
        # Collision sizes for AABB collision.
        # The sphere is approximated by a box around it.
        self.player_size = [1.2, 1.2, 1.2]
        self.wall_size = [3, 1.5, 0.7]
        # Floor limits keep the player inside the visible floor area.
        # The floor is 10 by 12, and the sphere radius is 0.6.
        self.floor_x_limit = 4.4
        self.floor_z_limit = 5.4
        

    def update(self):
        # Start each frame with no movement.
        # Keyboard input will change dx and dz.
        dx = 0
        dz = 0


        # w/s move along the z axis.
        # a/d move along the x axis.
        if self.input.isKeyPressed("w"):
            dz -= self.player_speed
        if self.input.isKeyPressed("s"):
            dz += self.player_speed
        if self.input.isKeyPressed("a"):
            dx -= self.player_speed
        if self.input.isKeyPressed("d"):
            dx += self.player_speed

        # Calculate where the player wants to move before actually moving it.
        # This proposed position is checked against collision and floor boundaries.
        current_position = self.player.getPosition()
        proposed_position = [
            current_position[0] + dx,
            current_position[1],
            current_position[2] + dz
        ]

        # Check whether the proposed movement would hit the wall.
        blocked_by_wall = is_colliding(
            proposed_position,
            self.player_size,
            self.wall.getPosition(),
            self.wall_size
        )
        # Check whether the proposed movement stays on the floor.
        inside_floor = is_inside_floor(
            proposed_position,
            self.floor_x_limit,
            self.floor_z_limit
        )

        # Apply movement only when the player stays on the floor
        # and does not collide with the wall.
        if inside_floor and not blocked_by_wall:
            self.player.setPosition(
                proposed_position[0],
                proposed_position[1],
                proposed_position[2]
            )
        # Rotate the globe slightly each frame so the texture is visible in motion.
        self.player.rotateY(1/120)
        self.player.rotateX(1/180)
         # Render the updated scene.
        self.render.render(self.scene, self.camera)


Test().run()