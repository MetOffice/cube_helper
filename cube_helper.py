import os
import iris
from cube_dataset import CubeSet
from cube_loader import CubeLoader


class CubeHelper(object):

	def __init__(self, directory, opt_filetype = ".nc", opt_constraints = None,):
		self.directory = directory
		self.opt_filetype = opt_filetype
        self.opt_constraints = opt_constraints
		if type(dir) == str:
			loaded_cubes = CubeLoader.load_from_dir(self.directory)
			self.cube_dataset = CubeSet(loaded_cubes)
		elif type([]):
			loaded_cubes = CubeLoader.load_from_filelist(self.directory)
			self.cube_dataset = CubeSet(loaded_cubes)
		else:
			print("cube input parameters invalid")

	def get_combined_cube(self):
		"""
		Returns the concatenated_cube if cube_list has been concatenated.

		:return iris.cube.Cube: concatenated resultant cube
		"""
		return None


	def concatenate(self):
		return self.cube_dataset.cube_list.concatenate()

	def merge_cube(self):
		return self.cube_dataset.cube_list.merge_cube()

	def merge(self):
		return self.cube_dataset.cube_list.merge()

	def convert_units(self, unit):
		for cube in self.loaded_cubes:
			cube.convert_units(unit)

	def collapse_dimension(self, dimension):
		for index, cube in enumerate(self.loaded_cubes):
			self.loaded_cubes[index] = cube.collapsed(dimension, iris.analysis.MEAN)
		self.cube_list = iris.cube.CubeList(self.loaded_cubes)

	def remove_attributes(self, cubes):
		self.cube_list = CubeEqualiser.remove_attributes(cubes)