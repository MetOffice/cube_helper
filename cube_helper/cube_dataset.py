import os
import iris
from cube_equaliser import equalise_attributes, unify_time_units

class CubeSet(object):

	def __init__(self, loaded_cubes):
		"""
		initialises class. data_file list
		is a list of cube filepaths or filenames to be manipulated.
		"""
		self.cube_list = iris.cube.CubeList(loaded_cubes)
		self.loaded_cubes = loaded_cubes

	def __repr__(self):
		"""
		prettify the set of cubes (CubeSet)
		:return: formatted CubeList
		"""
		return '{self.cube_list}'.format(self=self)

	def append(self, other):
		self.loaded_cubes.extend(other.loaded_cubes)
		self.cube_list = iris.cube.CubeList(self.loaded_cubes)





