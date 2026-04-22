
from core.base import Base
from core.render import Render
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh 

from geometry.planeGeometry import PlaneGeometry
from geometry.boxGeometry import BoxGeometry
from material.surfaceBasicMaterial import SurfaceBasicMaterial

class Test(Base):

	def initialize(self):
		print("Initializing...")

		self.render = Render()
		self.scene = Scene()
		self.camera = Camera()
		self.camera.setPosition(1,2,5)

		# define the geometry		
		geometry = PlaneGeometry(width=2)
		material = SurfaceBasicMaterial({"useVertexColors":1})
		self.mesh = Mesh(geometry, material)

		# add the geometry to the scene
		self.scene.add(self.mesh)	

		geometry_b = BoxGeometry()	
		self.mesh_b = Mesh(geometry_b, material)
		self.scene.add(self.mesh_b)

	def update(self):
		# self.mesh.rotateX(1/60.0)

		# display
		self.render.render(self.scene, self.camera)

Test().run()
