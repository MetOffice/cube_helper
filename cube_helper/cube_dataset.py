import iris

class CubeSet(iris.cube.CubeList):

	def __init__(self, loaded_cubes):
		"""
		initialises class. inherits from CubeList.
		"""
		self.cube_list = iris.cube.CubeList(loaded_cubes)

	def __repr__(self):
		"""
		prettify the set of cubes (CubeSet)
		:return: formatted CubeList
		"""
		return '{self.cube_list}'.format(self=self)






