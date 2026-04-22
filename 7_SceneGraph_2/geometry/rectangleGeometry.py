from geometry.geometry import Geometry

class RectangleGeometry(Geometry):
	"""
	Represents a 2D rectangle geometry.
	"""

	def __init__(self, width=1, height=1):
		"""
		Initializes a RectangleGeometry object.
		
		Args:
			width (int, optional): The width of the rectangle. Defaults to 1.
			height (int, optional): The height of the rectangle. Defaults to 1.
		"""

		super().__init__()

		# vertices' positions
		P0 = [-width/2, -height/2, 0]
		P1 = [ width/2, -height/2, 0]
		P2 = [-width/2,  height/2, 0]
		P3 = [ width/2,  height/2, 0]

		# vertex colors
		C0 = [1,1,1]
		C1 = [1,0,0]
		C2 = [0,1,0]
		C3 = [0,0,1]

		positionData = [P0,P1,P3, P0,P3,P2]
		colorData = [C0,C1,C3, C0,C3,C2]

		self.addAttribute("vec3", "vertexPosition", positionData)
		self.addAttribute("vec3", "vertexColor", colorData)

		self.countVertices()


