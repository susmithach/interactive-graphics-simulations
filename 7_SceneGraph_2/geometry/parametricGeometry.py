from geometry.geometry import Geometry

class ParametricGeometry(Geometry):
	"""
	Generates geometry based on a parametric surface function.
	"""

	def __init__(self, uStart, uEnd, uResolution,
					   vStart, vEnd, vResolution, S):
		"""
		Initializes a ParametricGeometry object.
		
		Args:
			uStart (float): The starting value for the u-parameter.
			uEnd (float): The ending value for the u-parameter.
			uResolution (int): The number of divisions along the u-axis.
			vStart (float): The starting value for the v-parameter.
			vEnd (float): The ending value for the v-parameter.
			vResolution (int): The number of divisions along the v-axis.
			S (function): A parametric function S(u, v) that returns a 3D point [x, y, z].
		"""

		super().__init__()

		# generate a set of points in the 2D world
		deltaU = (uEnd - uStart) / uResolution
		deltaV = (vEnd - vStart) / vResolution

		# positions in the 3D world
		positions =[]

		for uIndex in range(uResolution + 1):
			vArray = []
			u = uStart + deltaU * uIndex

			for vIndex in range(vResolution + 1):
				v = vStart + deltaV * vIndex
				vArray.append( S(u, v) )
			positions.append(vArray)

		# group the points into vertex data
		positionData = []
		colorData = []

		# vertex color (default)
		C1, C2, C3 = [1,0,0], [0,1,0], [0,0,1]
		C4, C5, C6 = [0,1,1], [1,0,1], [1,1,0]

		# group points into triangles
		for xIndex in range(uResolution):
			for yIndex in range(vResolution):
				# position data
				pA = positions[xIndex+0][yIndex+0]
				pB = positions[xIndex+1][yIndex+0]
				pC = positions[xIndex+1][yIndex+1]
				pD = positions[xIndex+0][yIndex+1]

				positionData += [pA, pB, pC,
								 pA, pC, pD]

				colorData += [C1, C2, C3,
							  C4, C5, C6]

		self.addAttribute("vec3", "vertexPosition", positionData)
		self.addAttribute("vec3", "vertexColor", colorData)
		self.countVertices()




