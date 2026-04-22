from core.base import Base
from core.render import Render
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh 

from geometry.sphereGeometry import SphereGeometry
from geometry.ellipsoidGeometry import EllipsoidGeometry
from geometry.boxGeometry import BoxGeometry
from material.surfaceBasicMaterial import SurfaceBasicMaterial

class Test(Base):

	def initialize(self):
		print("Initializing...")

		self.render = Render()
		self.scene = Scene()
		self.camera = Camera()
		self.camera.setPosition(0,0,5)

		# define the geometry
		geometry_e = EllipsoidGeometry(width=5, height=5)
		geometry = SphereGeometry(radius=1)
		material = SurfaceBasicMaterial({"useVertexColors":1})
		self.mesh = Mesh(geometry, material)
		self.mesh_e = Mesh(geometry_e, material)

		# add the geometry to the scene
		self.scene.add(self.mesh)
		self.scene.add(self.mesh_e)		


	def update(self):
		self.mesh.rotateY(1/60.0)
		self.mesh_e.rotateY(1/500.0)

		# display
		self.render.render(self.scene, self.camera)

Test().run()
