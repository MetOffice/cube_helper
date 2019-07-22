import iris
import os
import sys
from libs.utils import equalise_attributes, unify_time_units


class CubeHelper(object):

	def __init__(self, opt_constraint = None, opt_filetype = ".nc"):
		"""
		initialises class, where constraints and filetypes can be specified. data_file list
		is a list of cube filepaths or filenames to be manipulated.
		"""
		self.opt_constraint = opt_constraint
		self.opt_filetype = opt_filetype
		self.loaded_cubes = []
		self.cube_list = None
		self.concatenated_cube = None
		self.units = ''
		self.long_name = ''
		self.standard_name = ''
		self.is_unified = False
		self.is_loaded = False
		self.is_concatenated = False

	def reset_helper(self, opt_constraint = None, opt_filetype = ".nc"):
		"""
		resets the objects by recalling the init method
		"""
		self.__init__(opt_constraint, opt_filetype)


	def __repr__(self):
		if self.is_concatenated == False:
			return 'Cube has not been combined'.format(self=self)
		else:
			return '{self.concatenated_cube}'.format(self=self)


	def load_from_dir(self, dir):
		"""
		Loads a set of cubes from a given directory, single cubes are loaded and
		appended into an iterable as well as being loaded into a cubelist.

		:param string dir: directory to load data from
		:return iris.cube.CubleList: CubeList loaded form directory
		:return list loaded cubes: List of loaded cubes (needed to manipulate metadata etc)
		"""
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



	def load_from_filelist(self, data_filelist):
		"""
		Loads a set of cubes from a given directory, single cubes are loaded and
		appended into an iterable as well as being loaded into a cubelist.

		:param list data_filelist: directory to load data from
		:return iris.cube.CubleList: CubeList loaded from file list
		:return list loaded_cubes: List of loaded cubes (needed to manipulate metadata etc)
		"""
		if self.is_loaded == True:
			print('\n\nCubes already loaded\n\n')

		for filename in data_filelist:
			if filename.endswith(self.opt_filetype):
				break
			else:
				print('\n\nThe selected filetype is not present in data_filelist\n\n')

		for filename in data_filelist:
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

		self.is_loaded = True
		if not self.loaded_cubes:
			print('\n\nThe selected cubes have not loaded correctly\n\n')
		self.cube_list = iris.cube.CubeList(self.loaded_cubes)



	def unify_cube(self):
		"""
		Equalises the attributes and time units for appropriate merger or concatonation.

		:return list loaded_cubes: Cubes with equalised attributes reloaded into loaded_list
		"""
		if self.is_loaded:
			unify_time_units(self.loaded_cubes)
			equalise_attributes(self.loaded_cubes)
			self.is_unified = True
		else:
			print('\n\nCubes must be loaded before unification\n\n')



	def get_combined_cube(self):
		"""
		Returns the concatenated_cube if cube_list has been concatenated.

		:return iris.cube.Cube: concatenated resultant cube
		"""
		return self.concatenated_cube

	#get the list of loaded cubes as a CubeList
	def get_cubelist(self):
		return self.cube_list

	def get_loaded_cubes(self):
		return self.loaded_cubes

	#get units of resultant cube
	def get_units(self):
		if not self.is_loaded:
			print('\n\nCubes musted be loaded first.')
		if self.is_concatenated:
			return self.units
		else:
			return self.loaded_cubes[0].units

	def concatenate_cube(self):
		if self.is_loaded and self.is_unified:
			self.concatenated_cube = self.cube_list.concatenate_cube()
			self.units = self.concatenated_cube.units
			self.long_name = self.concatenated_cube.long_name
			self.standard_name = self.concatenated_cube.standard_name
			self.is_concatenated = True
		else:
			print('\n\nCubes must be loaded and unified (in that order) before concatenation\n\n')

	def concatenate(self):
		if self.is_loaded and self.is_unified:
			self.cube_list = iris.cube.CubeList(self.loaded_cubes)
			self.concatenated_cube = self.cube_list.concatenate()
		else:
			print('\n\nCubes must be loaded and unified (in that order) before concatenation\n\n')


	def merge_cube(self):
		if self.is_loaded and self.is_unified:
			self.cube_list = iris.cube.CubeList(self.loaded_cubes)
			self.concatenated_cube = self.cube_list.merge_cube()

		else:
			print('\n\nCubes must be loaded and unified (in that order) before merger\n\n')


	def merge(self):
		if self.is_loaded and self.is_unified:
			self.cube_list = iris.cube.CubeList(self.loaded_cubes)
			self.concatenated_cube = self.cube_list.merge()
		else:
			print('\n\nCubes must be loaded and unified (in that order) before merger\n\n')

	def convert_units(self, unit):
		for cube in self.loaded_cubes:
			cube.convert_units(unit)

	def collapse_dimension(self, dimension):
		for index, cube in enumerate(self.loaded_cubes):
			self.loaded_cubes[index] = cube.collapsed(dimension, iris.analysis.MEAN)
		self.cube_list = iris.cube.CubeList(self.loaded_cubes)

	def remove_attributes(self):
		attributes = ['further_info_url', 'initialization_index', 'mo_runid',
					  'table_info', 'variant_label', 'CDO', 'parent_activity_id',
					  'parent_simulation_id', 'original_name', 'contact',
					  'branch_method', 'variant_info', 'CDI', 'references',
					  'parent_mip_era', 'data_specs_version', 'grid', 'institution',
					  'institution_id', 'nominal_resolution', 'source', 'source_id',
					  'title', 'license', 'cmor_version', 'branch_time_in_parent',
					  'branch_time_in_child', 'parent_time_units', 'member_id',
					  'parent_source_id', 'parent_variant_label', 'grid_label',
					  'source_type', 'run_variant', 'branch_time', 'creation_date',
					  'history', 'tracking_id', 'realm', 'nco_openmp_thread_number',
					  'parent_experiment_id', 'name', 'EXPID', 'realization_index',
					  'physics_index', 'forcing_index']
		for index, cube in enumerate(self.loaded_cubes):
			for key in attributes:
				cube.attributes[key] = ''
				self.loaded_cubes[index] = cube
		self.cube_list = iris.cube.CubeList(self.loaded_cubes)
