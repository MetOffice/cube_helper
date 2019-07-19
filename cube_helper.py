import iris
import os
import sys
from libs.utils import equalise_attributes, unify_time_units


class CubeHelper(object):
	"""
	initialises class, where constraints and filetypes can be specified. data_file list
	is a list of cube filepaths or filenames to be manipulated.
	"""
	def __init__(self, opt_constraint = None, opt_filetype = ".nc"):
		self.opt_constraint = opt_constraint
		self.opt_filetype = opt_filetype
		self.data_filelist = []
		self.loaded_cubes = []
		self.cube_list = None
		self.combined_cube = None
		self.units = ''
		self.long_name = ''
		self.standard_name = ''
		self.is_unified = False
		self.is_loaded = False
		self.is_concatenated = False

	"""
	returns a string representation, will only work when load_cube(), unify_cube()
	and concatenate have been called
	"""

	def reset_helper(self, opt_constraint = None, opt_filetype = ".nc"):
		self.__init__(opt_constraint, opt_filetype)


	def __repr__(self):
		if self.is_concatenated == False:
			return 'Cube has not been combined'.format(self=self)
		else:
			return '{self.combined_cube}'.format(self=self)

	#loads from a given directory, this method will load all specified file type
	def load_from_dir(self, dir):
		if self.is_loaded == True:
			print('\n\nCubes already loaded\n\n')

		if  dir == '':
			print('\n\nNo directory given\n\n')

		for path in os.listdir(dir):
			full_path = os.path.join(dir, path)
			if os.path.isfile(full_path):
				self.loaded_cubes.append(iris.load_cube(full_path))
		self.cube_list = iris.cube.CubeList(self.loaded_cubes)
		self.is_loaded = True


	#takes a custom list as an argument
	def load_from_filelist(self, data_filelist):
		if self.is_loaded == True:
			print('\n\nCubes already loaded\n\n')
		self.data_filelist = data_filelist
		for filename in self.data_filelist:
			if filename.endswith(self.opt_filetype):
				break
			else:
				print('\n\nThe selected filetype is not present in data_filelist\n\n')

		for filename in self.data_filelist:
			if self.opt_constraint == None:
				try:
					self.loaded_cubes.append(iris.load_cube(filename))
				except:
					pass
			else:
				try:
					self.loaded_cubes.append(iris.load_cube(filename,self.opt_constraint))
				except:
					pass

		#make sure multiple loading parameters aren't called
		self.is_loaded = True
		if not self.loaded_cubes:
			print('\n\nThe selected cubes have not loaded correctly\n\n')
		self.cube_list = iris.cube.CubeList(self.loaded_cubes)

	def unify_cube(self):
		if self.is_loaded:
			unify_time_units(self.loaded_cubes)
			equalise_attributes(self.loaded_cubes)
			self.is_unified = True
		else:
			print('\n\nCubes must be loaded before unification\n\n')


	#get the resultant cube of a merger
	def get_combined_cube(self):
		return self.combined_cube

	#get the list of loaded cubes as a CubeList
	def get_cubelist(self):
		return self.cube_list

	#get units of resultant cube
	def get_units(self):
		return self.units

	def concatenate_cube(self):
		if self.is_loaded and self.is_unified:
			self.combined_cube = self.cube_list.concatenate_cube()
			self.units = self.combined_cube.units
			self.long_name = self.combined_cube.long_name
			self.standard_name = self.combined_cube.standard_name
			self.is_concatenated = True
		else:
			print('\n\nCubes must be loaded and unified (in that order) before concatenation\n\n')

	def concatenate(self):
		if self.is_loaded and self.is_unified:
			self.cube_list = iris.cube.CubeList(self.loaded_cubes)
			self.combined_cube = self.cube_list.concatenate()
		else:
			print('\n\nCubes must be loaded and unified (in that order) before concatenation\n\n')


	def merge_cube(self):
		if self.is_loaded and self.is_unified:
			self.cube_list = iris.cube.CubeList(self.loaded_cubes)
			self.combined_cube = self.cube_list.merge_cube()

		else:
			print('\n\nCubes must be loaded and unified (in that order) before merger\n\n')


	def merge(self):
		if self.is_loaded and self.is_unified:
			self.cube_list = iris.cube.CubeList(self.loaded_cubes)
			self.combined_cube = self.cube_list.merge()
		else:
			print('\n\nCubes must be loaded and unified (in that order) before merger\n\n')

	def convert_units(self, unit):
		for cube in self.loaded_cubes:
			cube.convert_units(unit)

	def collapse_dimension(self, dimension):
		for index, cube in enumerate(self.loaded_cubes):
			self.loaded_cubes[index] = cube.collapsed(dimension, iris.analysis.MEAN)


