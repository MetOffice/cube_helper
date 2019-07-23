import os
import iris
from cube_dataset import CubeSet
from cube_loader import CubeLoader


class CubeHelper(object):

    def __init__(self, directory, opt_filetype = ".nc", opt_constraints = None,):
        self.directory = directory
        if type(directory) == str:
            loaded_cubes = CubeLoader.load_from_dir(directory, opt_constraints, opt_filetype)
            self.cube_dataset = CubeSet(loaded_cubes)
        elif type(directory) == type([]):
            loaded_cubes = CubeLoader.load_from_filelist(directory, opt_constraints, opt_filetype)
            self.cube_dataset = CubeSet(loaded_cubes)
        else:
            print("cube input parameters invalid")

    def concatenate(self):
        return self.cube_dataset.cube_list.concatenate()

    def concatenate_cube(self):
        return self.cube_dataset.cube_list.concatenate_cube()

    def merge_cube(self):
        return self.cube_dataset.cube_list.merge_cube()

    def merge(self):
        return self.cube_dataset.cube_list.merge()

    def convert_units(self, unit):
        for cube in self.cube_dataset.loaded_cubes:
            cube.convert_units(unit)

    # def collapse_dimension(self, dimension):
    # 	for index, cube in enumerate(self.cube_dataset.loaded_cubes):
    #
    # 	self.cube_dataset.loaded_cubes[index] = cube.collapsed(dimension, iris.analysis.MEAN)
    # 	self.cube_list = iris.cube.CubeList(self.cube_dataset.loaded_cubes)
    #
    # def remove_attributes(self, cubes):
    # 	self.cube_list = CubeEqualiser.remove_attributes(cubes)