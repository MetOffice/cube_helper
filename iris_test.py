import iris
import os
import numpy as np
import matplotlib.pyplot as plt
import iris.quickplot as qplt
from iris import cube
import cartopy.crs as ccrs
from iris.util import unify_time_units

class Dataset(object):

	def __init__(self, data_dir = None):
		self.data_dir = data_dir
		self.data_filelist = []
		self.cleansed_data_filelist = []
		self.loaded_cubes = []
		self.identical_attributes = []
		self.unique_attributes = []
		self.coordinates = []
		self.units = ''
		self.variable_name = ''
		self.merged_cubes = []

		for filename in os.listdir(self.data_dir):
			if filename.endswith(".nc"):
				self.data_filelist.append(data_dir + filename)



		for filename in self.data_filelist:

			self.loaded_cubes.append(iris.load_cube(filename))

		identical_attributes = list(self.loaded_cubes[0].attributes.keys())
		print(identical_attributes)
		for cube in self.loaded_cubes[1:]:
			cube_keys = list(cube.attributes.keys())
			self.identical_attributes = [
				key for key in identical_attributes
				if (key in cube_keys and
					np.all(cube.attributes[key] == self.loaded_cubes[0].attributes[key]))]

		# Remove all the other attributes.
		for cube in self.loaded_cubes:
			for key in list(cube.attributes.keys()):
				if key not in self.identical_attributes:
					if key not in self.unique_attributes:
						self.unique_attributes.append(key)
					del cube.attributes[key]

		self.coordinates = ', '.join(sorted([coord.name() for coord in cube.coords()]))
		#print(self.loaded_cubes[0].attributes)
		cube_list = iris.cube.CubeList(self.loaded_cubes)
		#complete_cube = iris.load(cube_list,'precipitation_flux')
		#complete_cube = complete_cube.merge_cube()
		#print(cube_list)
		#print(cube_list.concatenate_cube())
		#print(type(cube_list.concatenate()))


dataset = Dataset('data/')
print(dataset.unique_attributes)