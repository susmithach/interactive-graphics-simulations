# Interactive Mini Environment Simulation

## Overview

This project is a real-time interactive graphics simulation built with PyGame and PyOpenGL.

The scene contains:
- a textured globe player
- a floor
- a wall obstacle

The player can be moved with the keyboard. The globe stays inside the floor area and cannot pass through the wall.

## Features

- Real-time rendering using PyOpenGL
- Scene graph structure using `Scene`, `Mesh`, and `Object3D`
- Image-based texture on the globe
- Keyboard movement with `W`, `A`, `S`, and `D`
- Movement handled in the `update()` stage
- Model matrix updates through object position changes
- AABB collision detection with the wall
- Floor boundary limits to keep the player inside the visible area

## Controls

```text
W - move forward
S - move backward
A - move left
D - move right
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

## Implementation Notes

### Texture

The globe uses an image texture through:
- a GLSL `sampler2D` uniform
- the GLSL `texture()` function
- normalized UV coordinates from the sphere geometry

### Movement

Keyboard input is checked every frame in `update()`.
The player position is updated using `setPosition(...)`, which changes the object's model matrix.

### Collision

The project uses Axis-Aligned Bounding Box (AABB) collision detection.

Before moving the player, the program:
1. calculates the proposed next position
2. checks collision with the wall
3. checks that the player stays inside the floor boundary
4. applies movement only if both checks pass

This prevents the globe from crossing the wall or leaving the floor area.

## Manual Test Checklist

1. Run `python main.py`
2. Confirm the globe, floor, and wall are visible
3. Press `W`, `A`, `S`, and `D`
4. Confirm the globe moves correctly
5. Move directly into the wall and confirm it stops
6. Move around the side of the wall and confirm movement is allowed
7. Move toward the floor edges and confirm the globe stays inside the floor
8. Close the window and confirm the program exits cleanly

## Summary

This project demonstrates texture mapping, scene graph rendering, keyboard-controlled movement, model matrix updates, and collision handling in a simple interactive 3D environment.
