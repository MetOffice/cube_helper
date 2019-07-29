import os
import sys
import iris
from cube_loader import CubeLoader
from cube_equaliser import remove_attributes
from cube_dataset import CubeSet


class CubeHelp(object):
	"""
	A wrapper class to implement methods provided by cube_equaliliser
	"""


	def __init__(self, directory, opt_filetype = ".nc", opt_constraints = None):
		"""
		:param directory: The directory or list containing the set of cubes
		:param opt_filetype: The filetype of the cubes (usually .nc or .pp)
		:param opt_constraints: Any constraints to be applied when loading the cube
		"""
		self.directory = directory
		self.opt_filetype = opt_filetype
		self.opt_constraints = opt_constraints
		if type(directory) == str:
			loaded_cubes = CubeLoader.load_from_dir(directory, opt_constraints, opt_filetype)
			if not loaded_cubes:
				print("No cubes found")
			else:
				self.cube_dataset = CubeSet(loaded_cubes)
		elif type(directory) == type([]):
			loaded_cubes = CubeLoader.load_from_filelist(directory, opt_constraints, opt_filetype)
			if not loaded_cubes:
				print("No cubes found")
			else:
				self.cube_dataset = CubeSet(loaded_cubes)

	def concatenated(self):
		"""
		:return self.cube_dataset.cube_list.concatenate(): The concatenated cubes of the cube_dataset
		"""
		return self.cube_dataset.cube_list.concatenate()

	def concatenated_cube(self):
		"""
		:return self.cube_dataset.cube_list.concatenate_cube(): The concatenated cube of the cube_dataset:
		"""
		return self.cube_dataset.cube_list.concatenate_cube()

	def merged_cube(self):
		"""
		:return self.cube_dataset.cube_list.merge_cube(): The merged cube of the cube_dataset
		"""
		return self.cube_dataset.cube_list.merge_cube()

	def merged(self):
		"""
		:return self.cube_dataset.cube_list.merge(): The merged cubes of the cube_dataset
		"""
		return self.cube_dataset.cube_list.merge()

	def convert_units(self, unit):
		"""
		:param unit: The approved unit to convert to.
		"""
		for cube in self.cube_dataset.loaded_cubes:
			cube.convert_units(unit)

	def collapsed_dimension(self, dimension):
		"""
		:param dimension: the dimension of the cube to collapse
		"""
		for index, cube in enumerate(self.cube_dataset.loaded_cubes):
			self.cube_dataset.loaded_cubes[index] = cube.collapsed(dimension, iris.analysis.MEAN)

		self.cube_dataset.cube_list = iris.cube.CubeList(self.cube_dataset.loaded_cubes)


	def remove_attributes(self):
		remove_attributes(self.cube_dataset.loaded_cubes)