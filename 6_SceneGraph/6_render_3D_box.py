from core.base import Base
from core.render import Render
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh 

from geometry.boxGeometry import BoxGeometry
from material.surfaceBasicMaterial import SurfaceBasicMaterial

class Test(Base):

	def initialize(self):
		print("Initializing...")

		self.render = Render()
		self.scene = Scene()
		self.camera = Camera()

		geometry = BoxGeometry()
		material = SurfaceBasicMaterial({"useVertexColors":1})
		self.mesh = Mesh(geometry, material)

		self.scene.add(self.mesh)

		self.camera.setPosition(0,0,5)

		# add a backdrop
		backGeometry = BoxGeometry(width=2, height=2, depth=0.01)
		backMaterial = SurfaceBasicMaterial({"baseColor":[1,1,1]})
		backdrop = Mesh(backGeometry,backMaterial)
		self.scene.add(backdrop)


	def update(self):
		self.mesh.rotateX(1/60.0)
		self.mesh.rotateY(1/60.0)

		self.render.render(self.scene, self.camera)

Test().run()
