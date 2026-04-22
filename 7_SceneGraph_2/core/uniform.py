from OpenGL.GL import *

class Uniform(object):

	def __init__(self, dataType, data):
		# The constructor takes two parameters:
		#	dataType is used to select which OpenGL function we are going to use
		# 	data is the data we want to upload to GPU

		# type of data
		#	ini | bool | float | vec2 | vec3 | vec4 
		self.dataType = dataType

		# data to be sent to uniform variable
		self.data = data

		# reference for variable location in program
		#	we will upload the data again and again to the same reference, so it is
		#	userful store the reference, and we don't need to retrive it everytime
		self.variableRef = None # since we don't know the variable, yet, we can set
								# it as None for now. Later we can change the value

	# function to locate the variable in program 
	# 	(the function to assign value to self.variableRef)
	#	get and store reference to uniform variable
	def locateVariable(self, programRef, variableName):
		self.variableRef = glGetUniformLocation(programRef, variableName)

	# function to upload data
	#	store data in the uniform variable
	def uploadData(self):

		# make sure the variable exists
		# 	if variable does not exist, then exit
		if self.variableRef == -1:
			return

		# a big if-else block to cover all the cases 
		#	(i.e., upload data for different data types)
		if self.dataType == "int": # 1 integer number
			glUniform1i(self.variableRef, self.data)
		elif self.dataType == "bool":
			glUniform1i(self.variableRef, self.data)  # boolean will be converted to 0/1
													  # it will be handled as same as int
		elif self.dataType == "float": # 1 float number
			glUniform1f(self.variableRef, self.data)	

		# when we have more than one element, we need to seperate the elements	
		elif self.dataType == "vec2": # 2 float number
			glUniform2f(self.variableRef, self.data[0], self.data[1])
		elif self.dataType == "vec3": # 3 float number
			glUniform3f(self.variableRef, self.data[0], self.data[1], 
						self.data[2])
		elif self.dataType == "vec4": # 4 float number
			glUniform4f(self.variableRef, self.data[0], self.data[1], 
						self.data[2], self.data[3])		
		elif self.dataType == "mat4":
			glUniformMatrix4fv(self.variableRef, 1, GL_TRUE, self.data)		
		
		else:
			raise Exception("Unknown Uniform data type: "+self.dataType)