import os
import iris


class CubeLoader(object):


	@staticmethod
	def load_from_dir(directory, opt_constraint=None, opt_filetype='.nc'):
		"""
		Loads a set of cubes from a given directory, single cubes are loaded and
		appended into an iterable as well as being loaded into a cubelist.

		:param string directory: Directory to load data from
		:return list loaded cubes: List of cubes loaded from the filelist
		"""
		if opt_constraint == None:
			loaded_cubes = []
			for path in os.listdir(directory):
				full_path = os.path.join(directory, path)
				if os.path.isfile(full_path) and full_path.endswith(opt_filetype):
					loaded_cubes.append(iris.load_cube(full_path))
			return iris.cube.CubeList(loaded_cubes)
		else:
			loaded_cubes = []
			for path in os.listdir(directory):
				full_path = os.path.join(directory, path)
				if os.path.isfile(full_path) and full_path.endswith(opt_filetype):
					loaded_cubes.append(iris.load_cube(full_path, opt_constraint))
			return iris.cube.CubeList(loaded_cubes)

	@staticmethod
	def load_from_filelist(data_filelist, opt_constraint=None, opt_filetype='.nc'):
		"""
		Loads a set of cubes from a given directory, single cubes are loaded and
		appended into an iterable as well as being loaded into a cubelist.

		:param list data_filelist: A list of files to load data from
		:return list loaded_cubes: An iterable of cubes loaded from file list
		"""
		loaded_cubes = []
		for filename in data_filelist:
			if filename.endswith(opt_filetype):
				break
			else:
				print('\n\nThe selected filetype is not present in data_filelist\n\n')

		for filename in data_filelist:
			if opt_constraint == None:
				try:
					loaded_cubes.append(iris.load_cube(filename))
				except:
					pass
			else:
				try:
					loaded_cubes.append(iris.load_cube(filename, opt_constraint))
				except:
					pass
		return iris.cube.CubeList(loaded_cubes)