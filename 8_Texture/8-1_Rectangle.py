from core.base import Base
from core.render import Render
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh 
from core.texture import Texture

from geometry.rectangleGeometry import RectangleGeometry
from material.surfaceBasicMaterial import SurfaceBasicMaterial
from material.textureMaterial import TextureMaterial

from geometry.geometry import Geometry
from material.material import Material

class Test(Base):
	"""
	This class extends the Base class to create a simple application that displays a textured rectangle.
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
		geometry = RectangleGeometry()		
		
		# material = SurfaceBasicMaterial({"useVertexColors":1})
		
		tex = Texture("8_Texture/img/img.jpeg")
		material = TextureMaterial( tex )
		
		self.mesh = Mesh(geometry, material)
		# add the geometry to the scene
		self.scene.add(self.mesh)		

	def update(self):
		"""
		Updates the scene by rotating the mesh and rendering the scene.
		"""
		self.mesh.rotateX(1/60.0)

		# display
		self.render.render(self.scene, self.camera)

Test().run()
