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

# Checks whether the sphere is above the top face of the wall.
# A small margin is used so the player can stand on the wall without slipping through the edge.
def is_over_wall_top(pos, wall_pos, wall_size):
    x_margin = 0.05
    z_margin = 0.05
    wall_left = wall_pos[0] - wall_size[0] / 2
    wall_right = wall_pos[0] + wall_size[0] / 2
    wall_front = wall_pos[2] - wall_size[2] / 2
    wall_back = wall_pos[2] + wall_size[2] / 2

    return (
        wall_left + x_margin <= pos[0] <= wall_right - x_margin and
        wall_front + z_margin <= pos[2] <= wall_back - z_margin
    )


# Checks whether the player is coming down onto the top of the wall.
def is_landing_on_wall(
    current_pos,
    proposed_pos,
    wall_support_y,
    wall_pos,
    wall_size
):
    falling = proposed_pos[1] <= current_pos[1]
    crossed_support_height = (
        current_pos[1] >= wall_support_y - 0.02 and
        proposed_pos[1] <= wall_support_y + 0.12
    )
    over_top = is_over_wall_top(
        proposed_pos,
        wall_pos,
        wall_size
    )

    return falling and crossed_support_height and over_top

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
        self.camera.setPosition(1.5, 2.2, 6.2)
        self.camera.rotateY(0.16)
        self.camera.rotateX(-0.32)

        # Use the folder containing this file as the base path for loading images.
        # This makes the texture path work when the project is run from term_project.
        base_dir = Path(__file__).resolve().parent

        # Create the player object as a textured sphere.
        # The Earth image is applied using TextureMaterial.
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
        wall_geometry = BoxGeometry(width=3.5, height=1.8, depth=1.4)
        wall_material = SurfaceBasicMaterial({"baseColor": [0.65, 0.2, 0.18]})

        self.wall = Mesh(wall_geometry, wall_material)

        # The wall bottom sits on the floor.
        # Floor Y is -1 and wall height is 1.8, so center Y is -1 + 0.9 = -0.1.
        self.wall.setPosition(0, -0.1, -3)
        self.scene.add(self.wall)

        # Movement speed on the floor and in the air.
        self.player_speed = 0.05
        # Collision sizes for AABB collision.
        # The sphere is approximated by a box around it.
        self.player_size = [1.2, 1.2, 1.2]
        self.wall_size = [3.5, 1.8, 1.4]
        # Floor limits keep the player inside the visible floor area.
        # The floor is 10 by 12, and the sphere radius is 0.6.
        self.floor_x_limit = 4.4
        self.floor_z_limit = 5.4
        # Jump settings. The player starts on the floor and moves up with
        # jump speed, then gravity pulls it back down.
        self.ground_y = -0.4
        self.vertical_velocity = 0.0
        self.jump_speed = 0.22
        self.gravity = 0.012
        self.is_jumping = False

        # These values are used to decide when the player is on top of the wall.
        self.player_radius = 0.6
        self.wall_support_y = (
            self.wall.getPosition()[1] +
            self.wall_size[1] / 2 +
            self.player_radius
        )
        self.support_epsilon = 1e-6

    def update(self):
        # Horizontal movement input for this frame.
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
        current_x = current_position[0]
        current_y = current_position[1]
        current_z = current_position[2]

        # The player can stand either on the floor or on top of the wall.
        on_floor = abs(current_y - self.ground_y) < self.support_epsilon
        on_wall = (
            abs(current_y - self.wall_support_y) < self.support_epsilon and
            is_over_wall_top(
                current_position,
                self.wall.getPosition(),
                self.wall_size
            )
        )

        # Start a jump only when the player is standing on a support surface.
        if self.input.isKeyDown("space") and (on_floor or on_wall):
            self.vertical_velocity = self.jump_speed
            self.is_jumping = True

        # If the player walks off the wall top, start falling.
        horizontal_probe = [current_x + dx, current_y, current_z + dz]
        if on_wall and not self.is_jumping:
            still_over_wall = is_over_wall_top(
                horizontal_probe,
                self.wall.getPosition(),
                self.wall_size
            )
            if not still_over_wall:
                self.is_jumping = True
                self.vertical_velocity = 0.0

        # Update the jump arc.
        new_y = current_y
        if self.is_jumping:
            new_y += self.vertical_velocity
            self.vertical_velocity -= self.gravity

        # Try the next position for this frame before applying it.
        proposed_position = [
            current_x + dx,
            new_y,
            current_z + dz
        ]

        # The player must stay on the visible floor area.
        inside_floor = is_inside_floor(
            proposed_position,
            self.floor_x_limit,
            self.floor_z_limit
        )
        if not inside_floor:
            proposed_position[0] = current_x
            proposed_position[2] = current_z

        # This allows the player to land on top of the wall instead of entering it.
        landing_on_wall = is_landing_on_wall(
            current_position,
            proposed_position,
            self.wall_support_y,
            self.wall.getPosition(),
            self.wall_size
        )

        # The wall body stays solid all the time.
        colliding_with_wall_body = is_colliding(
            proposed_position,
            self.player_size,
            self.wall.getPosition(),
            self.wall_size
        )
        currently_inside_wall = is_colliding(
            current_position,
            self.player_size,
            self.wall.getPosition(),
            self.wall_size
        )

        blocked_by_wall = (
            colliding_with_wall_body and
            proposed_position[1] < self.wall_support_y and
            not landing_on_wall
        )

        final_x = proposed_position[0]
        final_y = proposed_position[1]
        final_z = proposed_position[2]

        if landing_on_wall:
            # Snap the player to the top of the wall and stop the fall.
            final_y = self.wall_support_y
            self.vertical_velocity = 0.0
            self.is_jumping = False

        elif blocked_by_wall:
            # Do not allow the player to move deeper into the wall body.
            final_x = current_x
            final_z = current_z

            if currently_inside_wall:
                # Push the player back to the nearest side if it reaches a wall collision state.
                wall_center_z = self.wall.getPosition()[2]
                clearance = (self.wall_size[2] + self.player_size[2]) / 2
                if current_z <= wall_center_z:
                    final_z = wall_center_z - clearance
                else:
                    final_z = wall_center_z + clearance

            if final_y <= self.ground_y:
                final_y = self.ground_y
                self.vertical_velocity = 0.0
                self.is_jumping = False

        else:
            # Land back on the floor after the jump ends.
            if final_y <= self.ground_y:
                final_y = self.ground_y
                self.vertical_velocity = 0.0
                self.is_jumping = False
            elif on_wall and not self.is_jumping:
                # Keep the player supported while it is standing on top of the wall.
                over_wall_now = is_over_wall_top(
                    [final_x, self.wall_support_y, final_z],
                    self.wall.getPosition(),
                    self.wall_size
                )
                if over_wall_now:
                    final_y = self.wall_support_y

        self.player.setPosition(final_x, final_y, final_z)

        # Rotate the globe while it is moving or jumping.
        if dx != 0 or dz != 0 or self.is_jumping:
            self.player.rotateY(1 / 120)
            self.player.rotateX(1 / 180)

        # Draw the updated scene for this frame.
        self.render.render(self.scene, self.camera)

Test().run()
