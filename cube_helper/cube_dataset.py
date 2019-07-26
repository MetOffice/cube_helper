import os
import iris
from cube_helper.cube_helper.cube_equaliser import equalise_attributes, unify_time_units

class CubeSet(object):

	def __init__(self, loaded_cubes):
		"""
		initialises class. data_file list
		is a list of cube filepaths or filenames to be manipulated.
		"""
		#self.loaded_cubes = loaded_cubes
		self.cube_list = iris.cube.CubeList(loaded_cubes)
		equalise_attributes(loaded_cubes)
		unify_time_units(loaded_cubes)
		self.loaded_cubes = loaded_cubes


	def __repr__(self):
		return '{self.cube_list}'.format(self=self)



