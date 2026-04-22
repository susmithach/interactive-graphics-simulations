from geometry.geometry import Geometry

class RectangleGeometry(Geometry):

	def __init__(self, width=1, height=1):

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

		# UV
		T0, T1, T2, T3 = [0,0], [1,0], [0,1], [1, 1]

		positionData = [P0,P1,P3, P0,P3,P2]
		colorData = [C0,C1,C3, C0,C3,C2]

		uvData = [T0, T1, T3, 
				  T0, T3, T2]

		self.addAttribute("vec3", "vertexPosition", positionData)
		self.addAttribute("vec3", "vertexColor", colorData)
		self.addAttribute("vec3", "vertexUV", uvData)
		self.countVertices()


