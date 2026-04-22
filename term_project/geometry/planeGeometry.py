from geometry.parametricGeometry import ParametricGeometry

class PlaneGeometry(ParametricGeometry):

	def __init__(self, width=1, height=1, widthResolution=8, heightResolution=8):

		def S(u,v):
			return [u, v, -1]


		uStart = -width/2
		uEnd = width/2
		uResolution = widthResolution

		vStart = -height/2
		vEnd = height/2
		vResolution = heightResolution

		super().__init__(uStart, uEnd, uResolution,
					     vStart, vEnd, vResolution, S)