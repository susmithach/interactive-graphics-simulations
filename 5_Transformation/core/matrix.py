import numpy as np
from math import sin, cos, tan, pi 

class Matrix(object):
	"""
	A utility class providing static methods to generate various 4x4 transformation
	matrices (identity, translation, rotation, scale) and a perspective projection matrix.
	These matrices are fundamental for manipulating objects in 3D space within OpenGL.
	All angles are expected in radians.
	"""

	@staticmethod
	def makeIdentity():
		"""
		Generates a 4x4 identity matrix.
		An identity matrix represents no transformation when multiplied with other matrices.
		Returns:
			np.array: A 4x4 NumPy array representing the identity matrix.
		"""
		return np.array([[1, 0, 0, 0],
						 [0, 1, 0, 0],
						 [0, 0, 1, 0],
						 [0, 0, 0, 1]]).astype(float)

	@staticmethod
	def makeTranslation(x, y, z):
		"""
		Generates a 4x4 translation matrix.
		This matrix moves an object by the specified (x, y, z) offsets.
		Args:
			x (float): Translation along the x-axis.
			y (float): Translation along the y-axis.
			z (float): Translation along the z-axis.
		Returns:
			np.array: A 4x4 NumPy array representing the translation matrix.
		"""
		return np.array([[1, 0, 0, x],
						 [0, 1, 0, y],
						 [0, 0, 1, z],
						 [0, 0, 0, 1]]).astype(float)

	@staticmethod
	def makeRotationX(angle):
		"""
		Generates a 4x4 rotation matrix around the X-axis.
		Args:
			angle (float): Rotation angle in radians.
		Returns:
			np.array: A 4x4 NumPy array representing the X-axis rotation matrix.
		"""
		c = cos(angle)
		s = sin(angle)
		return np.array([[1, 0,  0, 0],
						 [0, c, -s, 0],
						 [0, s,  c, 0],
						 [0, 0,  0, 1]]).astype(float)

	@staticmethod
	def makeRotationY(angle):
		"""
		Generates a 4x4 rotation matrix around the Y-axis.
		Args:
			angle (float): Rotation angle in radians.
		Returns:
			np.array: A 4x4 NumPy array representing the Y-axis rotation matrix.
		"""
		c = cos(angle)
		s = sin(angle)
		return np.array([[ c, 0, s, 0],
						 [ 0, 1, 0, 0],
						 [-s, 0, c, 0],
						 [ 0, 0, 0, 1]]).astype(float)

	@staticmethod
	def makeRotationZ(angle):
		"""
		Generates a 4x4 rotation matrix around the Z-axis.
		Args:
			angle (float): Rotation angle in radians.
		Returns:
			np.array: A 4x4 NumPy array representing the Z-axis rotation matrix.
		"""
		c = cos(angle)
		s = sin(angle)
		return np.array([[c, -s, 0, 0],
						 [s,  c, 0, 0],
						 [0,  0, 1, 0],
						 [0,  0, 0, 1]]).astype(float)

	@staticmethod
	def makeScale(s):
		"""
		Generates a 4x4 uniform scaling matrix.
		This matrix scales an object uniformly by a factor 's' along all axes.
		Args:
			s (float): The scaling factor.
		Returns:
			np.array: A 4x4 NumPy array representing the scaling matrix.
		"""
		return np.array([[s, 0, 0, 0],
						 [0, s, 0, 0],
						 [0, 0, s, 0],
						 [0, 0, 0, 1]]).astype(float)

	@staticmethod
	def makePerspective(angleOfView=60,
						aspectRatio=1,
						near=0.1,
						far=100):
		"""
		Generates a 4x4 perspective projection matrix.
		This matrix transforms 3D view-space coordinates into 2D clip-space coordinates,
		creating the illusion of depth.
		Args:
			angleOfView (float): The vertical field of view in degrees.
			aspectRatio (float): The aspect ratio of the viewport (width / height).
			near (float): The distance to the near clipping plane.
			far (float): The distance to the far clipping plane.
		Returns:
			np.array: A 4x4 NumPy array representing the perspective projection matrix.
		"""
		# Convert angleOfView from degrees to radians.
		a = angleOfView * pi/180

		# Calculate distance to the projection plane.
		d = 1.0 / tan(a/2) 
		r = aspectRatio
		
		# Coefficients for Z-transformation.
		b = (far+near) / (near-far)
		c = 2*far*near / (near-far)

		return np.array([[d/r, 0,  0, 0],
						 [  0, d,  0, 0],
						 [  0, 0,  b, c],
						 [  0, 0, -1, 0]]).astype(float)