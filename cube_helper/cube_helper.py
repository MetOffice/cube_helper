import os
import iris
from cube_helper.cube_helper.cube_loader import CubeLoader
from cube_helper.cube_helper.cube_equaliser import remove_attributes, equalise_attributes, unify_time_units


class CubeHelper(object):

    def __init__(self, directory, opt_filetype = ".nc", opt_constraints = None):
        self.directory = directory
        self.opt_filetype = opt_filetype
        self.opt_constraints = opt_constraints
        if type(directory) == str:
            loaded_cubes = CubeLoader.load_from_dir(directory, opt_constraints, opt_filetype)
            self.cube_dataset = CubeSet(loaded_cubes)
        elif type(directory) == type([]):
            loaded_cubes = CubeLoader.load_from_filelist(directory, opt_constraints, opt_filetype)
            self.cube_dataset = CubeSet(loaded_cubes)
        else:
            print("cube input parameters invalid")

    def concatenated(self):
        return self.cube_dataset.cube_list.concatenate()

    def concatenated_cube(self):
        return self.cube_dataset.cube_list.concatenate_cube()

    def merged_cube(self):
        return self.cube_dataset.cube_list.merge_cube()

    def merged(self):
        return self.cube_dataset.cube_list.merge()

    def convert_units(self, unit):
        for cube in self.cube_dataset.loaded_cubes:
            cube.convert_units(unit)

    def collapsed_dimension(self, dimension):
        for index, cube in enumerate(self.cube_dataset.loaded_cubes):
            self.cube_dataset.loaded_cubes[index] = cube.collapsed(dimension, iris.analysis.MEAN)
            return iris.cube.CubeList(self.cube_dataset.loaded_cubes)

    def remove_attributes(self, cubes):
        remove_attributes(cubes)