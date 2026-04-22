from core.base import Base
from core.render import Render
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh 
from core.texture import Texture

from geometry.boxGeometry import BoxGeometry
from geometry.rectangleGeometry import RectangleGeometry
from geometry.sphereGeometry import SphereGeometry

from material.surfaceBasicMaterial import SurfaceBasicMaterial
from material.textureMaterial import TextureMaterial

from geometry.geometry import Geometry
from material.material import Material

class Test(Base):
	"""
	This class extends the Base class to create a simple application that displays a textured box and a textured sphere.
	"""

	def initialize(self):
		"""
		Initializes the scene, camera, geometry, material, and mesh.
		"""
		print("Initializing...")

		self.render = Render()
		self.scene = Scene()
		self.camera = Camera()
		self.camera.setPosition(0,0,5)

		# define the geometry	
		geometry = BoxGeometry()
		material = SurfaceBasicMaterial({"useVertexColors":1})
		self.mesh = Mesh(geometry, material)
		self.mesh.setPosition(0, 1, 0)
		self.scene.add(self.mesh)		

		earthGeometry = SphereGeometry(radius=90)		
		earthTex = Texture("8_Texture/img/land.png")
		earthMaterial = TextureMaterial(earthTex)
        # earthMaterial = SurfaceBasicMaterial({"useVertexColors":1})

		self.earthMesh = Mesh(earthGeometry, earthMaterial)
		self.scene.add(self.earthMesh)

	def update(self):
		"""
		Updates the scene by rotating the mesh and rendering the scene.
		"""
		self.mesh.rotateX(1/60.0)
		self.mesh.rotateY(1/120.0)
		self.mesh.rotateZ(1/180.0)

		self.earthMesh.rotateY(1/240.0)

		# display
		self.render.render(self.scene, self.camera)

Test().run()
