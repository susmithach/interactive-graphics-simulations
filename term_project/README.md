# Interactive Mini Environment Simulation

## Overview

This project is a real-time interactive graphics simulation built with PyGame and PyOpenGL.

The scene contains:
- a textured globe player
- a floor
- a wall obstacle

The player can be moved with the keyboard and can also jump. The globe stays inside the floor area and cannot pass through the wall body.

## Features

- Real-time rendering using PyOpenGL
- Scene graph structure using `Scene`, `Mesh`, and `Object3D`
- Image-based texture on the globe
- Keyboard movement with `W`, `A`, `S`, and `D`
- Jump with the `Space` key
- Movement handled in the `update()` stage
- Model matrix updates through object position changes
- AABB collision detection with the wall
- Wall-top landing during jumps
- Floor boundary limits to keep the player inside the visible area

## Controls

```text
W - move forward
S - move backward
A - move left
D - move right
Space - jump
```

## How to Run

From the repository root:

```bash
cd term_project
python main.py
```

Make sure your virtual environment is activated and the required packages are installed.

## Project Structure

```text
term_project/
├── main.py
├── core/
├── geometry/
├── material/
└── img/
```

## Scene Objects

- **Player:** textured sphere using `earth_8k.jpg`
- **Floor:** flat rectangular ground surface
- **Wall:** 3D obstacle that blocks player movement
- **Wall Top:** support surface where the player can land after a jump

## Implementation Notes

### Texture

The globe uses an image texture through:
- a GLSL `sampler2D` uniform
- the GLSL `texture()` function
- normalized UV coordinates from the sphere geometry

### Movement

Keyboard input is checked every frame in `update()`.
The player position is updated using `setPosition(...)`, which changes the object's model matrix. Horizontal movement uses `W`, `A`, `S`, and `D`, and `Space` starts a jump when the player is standing on the floor or on top of the wall.

### Collision

The project uses Axis-Aligned Bounding Box (AABB) collision detection.

Before moving the player, the program:
1. calculates the proposed next position
2. checks collision with the wall
3. checks whether the player should land on top of the wall
4. checks that the player stays inside the floor boundary
5. applies movement only when the result is valid

This prevents the globe from crossing the wall body or leaving the floor area. During a jump, the player can land on top of the wall or move across it, but it should not remain inside the wall.

## Manual Test Checklist

1. Run `python main.py`
2. Confirm the globe, floor, and wall are visible
3. Press `W`, `A`, `S`, and `D`
4. Confirm the globe moves correctly
5. Move directly into the wall and confirm it stops
6. Press `Space` and confirm the globe jumps and lands back on the floor
7. Use `Space` with `W` or `S` near the wall and confirm the globe lands on top of the wall or clears it
8. Move around the side of the wall and confirm movement is allowed
9. Move toward the floor edges and confirm the globe stays inside the floor
10. Close the window and confirm the program exits cleanly

## Summary

This project demonstrates texture mapping, scene graph rendering, keyboard-controlled movement, jumping, model matrix updates, and collision handling in a simple interactive 3D environment.
