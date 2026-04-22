import pygame
import sys # for system control to terminate the application

from core.input import Input

class Base(object): 

	def __init__(self): # a constructor, a class method

		# initialize all pygame module
		pygame.init()

		# set window size
		screenSize = ( 512, 512 )

		# indicate rendering options for pygame
		displayFlags = pygame.DOUBLEBUF | pygame.OPENGL 

		# initialize buffers to perform anti-aliasing
		pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
		pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)

		# use a core OpenGL profile for cross-platform compatibility (MacOS)
		#	requires pygame >= 2.0.0
		pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, 
										pygame.GL_CONTEXT_PROFILE_CORE)

		# create the window
		self.screen = pygame.display.set_mode( screenSize, displayFlags )

		# determines if the main loop is active
		self.running = True

		# manage time-related data and operations
		self.clock = pygame.time.Clock()

		# manage user's input
		self.input = Input()

	def initialize(self):
		pass # the code will be written by any extendsion of this class

	def update(self):
		pass

	# main 
	def run(self):
		## startup ##
		self.initialize()

		## the main loop ##
		while self.running:

			## check/process input ##
			self.input.update() # this is the Update in the Input class

			if self.input.quit:
				self.running = False

			## update ##
			self.update()

			## render ##

			# display image on screen
			pygame.display.flip()

			# pause if nesseary to achieve 60 FPS
			self.clock.tick(60)


		## shutdown ##
		pygame.quit() # step pygame window
		sys.exit() # complete shutdown the applcation



