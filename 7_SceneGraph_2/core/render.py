from OpenGL.GL import *
from core.mesh import Mesh

class Render(object):
	def __init__(self, clearColor=[0,0,0,1.0]):

		glEnable(GL_DEPTH_TEST)
		glClearColor(clearColor[0], clearColor[1], clearColor[2], clearColor[3])

	def render(self, scene, camera):

		# clear buffers
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		# update camera view matrix
		camera.updateViewMatrix()

		# extract list of Mesh objects
		descendentList = scene.getDescendentList()
		# filter out other things
		meshFilter = lambda x : isinstance(x, Mesh)
		meshList = list(filter(meshFilter, descendentList))

		for mesh in meshList:

			if not mesh.visible:
				continue

			glUseProgram(mesh.material.programRef)
			glBindVertexArray(mesh.vaoRef)

			# update uniform matrices
			mesh.material.uniforms["modelMatrix"].data = mesh.getWorldMatrix()
			mesh.material.uniforms["viewMatrix"].data = camera.viewMatrix
			mesh.material.uniforms["projectionMatrix"].data = camera.projectionMatrix
			
			# upload uniforms
			for variableName, uniformObject in mesh.material.uniforms.items():
				uniformObject.uploadData()

			# update render settings
			mesh.material.updateRenderSettings()

			glDrawArrays(mesh.material.settings["drawStyle"], 0, mesh.geometry.vertexCount)
