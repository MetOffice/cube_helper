import os
import iris
from cube_equaliser import CubeEqualiser

class CubeSet(object):

	def __init__(self, loaded_cubes):
		"""
		initialises class. data_file list
		is a list of cube filepaths or filenames to be manipulated.
		"""
		self.loaded_cubes = loaded_cubes
		self.cube_list = iris.cube.CubeList(loaded_cubes)
		CubeEqualiser.equalise_attributes(self.loaded_cubes)
		CubeEqualiser.unify_time_units(self.loaded_cubes)


	def __repr__(self):
		return '{self.cube_list}'.format(self=self)




