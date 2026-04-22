from geometry.geometry import Geometry
from math import sin, cos, pi

class PolygonGeometry(Geometry):
	"""
	Represents a 2D polygon geometry.
	"""

	def __init__(self, sides=3, radius=1):
		"""
		Initializes a PolygonGeometry object.
		
		Args:
			sides (int, optional): The number of sides of the polygon. Defaults to 3.
			radius (int, optional): The radius of the polygon. Defaults to 1.
		"""
		super().__init__()

		# define the equation
		A = 2*pi/sides
		# X = radius*cos(A*n)
		# Y = radius*sin(A*n)

		positionData = []
		colorData = []

		uvData = []

		for n in range(sides):
			# vertices positions
			positionData.append([0,0,0])
			positionData.append( [radius*cos(n*A),
								  radius*sin(n*A),
								  0])
			positionData.append( [radius*cos((n+1)*A),
								  radius*sin((n+1)*A),
								  0])

			# vertex colors 
			colorData.append([1,1,1])
			colorData.append([1,0,0])
			colorData.append([0,0,1])

			# texture
			uvData.append([0.5, 0.5])
			uvData.append( [cos(n*A)*0.5+0.5, sin(n*A)*0.5+0.5])
			uvData.append( [cos((n+1)*A)*0.5+0.5, sin((n+1)*A)*0.5+0.5])


		self.addAttribute("vec3", "vertexPosition", positionData)
		self.addAttribute("vec3", "vertexColor", colorData)
		self.countVertices()
