import pygame

class Input(object):

	def __init__(self):

		# has the user quit the applicaiton?
		self.quit = False

		# lists to store key states
		#	down: discrete events (key was just pressed)
		# 	pressed: continouse event (key is currently held)
		self.keyDownList = []
		self.keyPressedList = []

	def update(self):

		# reset discrete key states
		self.keyDownList = []

		# check each pygame event
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quit = True

			# check for keydown and keyup
			if event.type == pygame.KEYDOWN:
				keyName = pygame.key.name( event.key )
				self.keyDownList.append( keyName )
				# Only add to keyPressedList if not already present to avoid duplicates
				if keyName not in self.keyPressedList:
					self.keyPressedList.append( keyName )
			
			if event.type == pygame.KEYUP:
				keyName = pygame.key.name( event.key )
				# Remove from keyPressedList if present
				if keyName in self.keyPressedList:
					self.keyPressedList.remove( keyName)

	def isKeyDown(self, keyName):
		return keyName in self.keyDownList
	def isKeyPressed(self, keyName):
		return keyName in self.keyPressedList