import iris
import os
import numpy as np
import matplotlib.pyplot as plt
import iris.quickplot as qplt
from iris import cube



class Dataset(object):

	def __init__(self, data_dir = None):
		self.data_dir = data_dir
		self.data_filelist = []
		self.loaded_cubes = []
		self.attributes = []
		self.identical_attributes = []
		self.unique_attributes = []
		self.coordinates = []

		for filename in os.listdir(self.data_dir):
			if filename.endswith(".nc"):
				self.data_filelist.append(data_dir + filename)



		for filename in self.data_filelist:
			cube = iris.load_cube(filename)
			self.loaded_cubes.append(cube)

		identical_attributes = list(self.loaded_cubes[0].attributes.keys())
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
					self.unique_attributes.append(key)
					del cube.attributes[key]

		self.unique_attributes = list(dict.fromkeys(self.unique_attributes))


		for file in self.data_filelist:
			print(type(file))




dataset = Dataset('data/')