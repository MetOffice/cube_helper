import iris
import os
import numpy as np
import cf_units


class CubeEqualiser(object):


	def equalise_attributes(self,cubes):
		# Work out which attributes are identical across all the cubes.
		common_keys = list(cubes[0].attributes.keys())
		for cube in cubes[1:]:
			cube_keys = list(cube.attributes.keys())
			common_keys = [
				key for key in common_keys
				if (key in cube_keys and
					np.all(cube.attributes[key] == cubes[0].attributes[key]))]

		# Remove all the other attributes.
		for cube in cubes:
			for key in list(cube.attributes.keys()):
				if key not in common_keys:
					del cube.attributes[key]


	def unify_time_units(self, cubes):
		epochs = {}
		for cube in cubes:
			for time_coord in cube.coords():
				if time_coord.units.is_time_reference():
					epoch = epochs.setdefault(time_coord.units.calendar, time_coord.units.origin)
					new_unit = cf_units.Unit(epoch, time_coord.units.calendar)
					time_coord.convert_units(new_unit)


	def remove_attributes(self, cubes):
		attributes_list = list(cubes[0].attributes.keys())
		for index, cube in enumerate(cubes):
			for key in attributes_list:
				cube.attributes[key] = ''
				cubes[index] = cube
		return iris.cube.CubeList(cubes)