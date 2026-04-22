import pygame # load image, convert image to the format for GPU
from OpenGL.GL import *

class Texture(object):
	"""
	Represents a 2D texture in OpenGL.
	"""

	def __init__(self, fileName=None, properties={}):
		"""
		Initializes a Texture object.
		
		Args:
			fileName (str, optional): The path to the image file. Defaults to None.
			properties (dict, optional): A dictionary of texture properties to override default values. Defaults to {}.
		"""

		self.surface = None

		# texture reference
		self.textureRef = glGenTextures(1)

		self.properties = {
			"magFilter" : GL_LINEAR,
			"minFilter" : GL_LINEAR_MIPMAP_LINEAR,
			"wrap" 		: GL_REPEAT
		}

		# overwrite default properties values
		self.setProperties( properties ) # define the function later

		# upload image
		if fileName is not None:
			self.loadImage(fileName) # write this function later
			self.uploadData() # write this function later

	def loadImage(self, fileName):
		"""
		Loads an image from the specified file and stores it as a pygame surface.
		
		Args:
			fileName (str): The path to the image file.
		"""
		self.surface = pygame.image.load(fileName)

	def setProperties(self, props):
		"""
		Sets texture properties.
		
		Args:
			props (dict): A dictionary of properties to set. Valid properties are "magFilter", "minFilter", and "wrap".
		
		Raises:
			Exception: If an invalid property name is provided.
		"""
		for name, data in props.items():
			# if the property name exist in the list, update the value
			# otherwise, raise exception
			if name in self.properties.keys():
				self.properties[names] = value
			else:
				raise Exception("No property named:" + name)

	# upload pixel data to GPU
	def uploadData(self):
		"""
		Uploads the pixel data of the loaded image to the GPU as a 2D texture.
		This method also generates mipmaps and sets texture parameters based on the object's properties.
		"""
		width = self.surface.get_width()
		height = self.surface.get_height()

		# convert image to string buffer
		pixelData = pygame.image.tostring(self.surface, "RGBA", 1)

		# bind texture
		glBindTexture(GL_TEXTURE_2D, self.textureRef)

		# send data to texture object
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixelData)

		# generate mipmaps
		glGenerateMipmap(GL_TEXTURE_2D)

		# set texture parameters
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, self.properties["magFilter"])
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, self.properties["minFilter"])

		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, self.properties["wrap"])
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, self.properties["wrap"])
