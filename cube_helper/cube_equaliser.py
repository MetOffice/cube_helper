import iris
import os
import numpy as np
import cf_units




def equalise_attributes(cubes):
	"""
	:param cubes: Cubes to be equalised
	"""
	uncommon_keys = []
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
				uncommon_keys.append(cube.attributes[key])
				del cube.attributes[key]
	uncommon_keys = list(set(uncommon_keys))
	return uncommon_keys

def unify_time_units(cubes):
	"""
	:param cubes: Cubes to be unified
	"""
	epochs = {}
	for cube in cubes:
		for time_coord in cube.coords():
			if time_coord.units.is_time_reference():
				epoch = epochs.setdefault(time_coord.units.calendar, time_coord.units.origin)
				new_unit = cf_units.Unit(epoch, time_coord.units.calendar)
				time_coord.convert_units(new_unit)
	return cubes


def remove_attributes(cubes):
	"""
	strips cubes of ALL attributes and metadata. Aux coords should
	be unaffected.
	:param cubes: Cubes to be stripped of attributes
	:return: cubes: after attributes have been removed
	"""
	attributes_list = list(cubes[0].attributes.keys())
	for index, cube in enumerate(cubes):
		for key in attributes_list:
			cube.attributes[key] = ''
			cubes[index] = cube
	return cubes


def unify_data_type(cubes):
	"""
	Casts datatypes in iris numpy array to be of the same datatype
	:param cubes: To be unified in datatypes
	:return cubes: uniformly cast cubes
	"""
	for cube in cubes:
		cube.data = np.float32(cube.data)
	return cubes

