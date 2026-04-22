from core.base import Base
from core.render import Render
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh 

from geometry.boxGeometry import BoxGeometry
from geometry.hexagonGeometry import HexagonGeometry
from geometry.polygonGeometry import PolygonGeometry
from material.surfaceBasicMaterial import SurfaceBasicMaterial

class Test(Base):

	def initialize(self):
		print("Initializing...")

		self.render = Render()
		self.scene = Scene()
		self.camera = Camera()

		geometry = HexagonGeometry()
		material = SurfaceBasicMaterial({"useVertexColors":1})
		self.mesh = Mesh(geometry, material)

		self.camera.setPosition(0,0,5)

		self.scene.add(self.mesh)

		self.x=0.0
	def update(self):
		self.mesh.rotateZ(1/60.0)
		self.mesh.translate(self.x+0.01, 0, 0, localCoord=False)

		self.render.render(self.scene, self.camera)

Test().run()
