import iris
import os
import numpy as np
import matplotlib.pyplot as plt
import iris.quickplot as qplt
from iris import cube

data_dir = 'data/'


class Dataset(object):

    def __init__(self, data_dir = None, attribute = ''):
        self.data_dir = data_dir
        self.data_filelist = []
        self.attribute = attribute
        self.loaded_data = []
        self.equalised_cubes = []
        self.attributes = []
        self.identical_attributes = []
        self.unique_attributes = []
        self.coordinates = []

        for filename in os.listdir(data_dir):
            if filename.endswith(".nc"):
                self.data_filelist.append(filename)

        for data_set in self.data_filelist:
            new_cube = iris.load_cube(self.data_dir + data_set, 'precipitation_flux')
            self.loaded_data.append(new_cube)

        identical_attributes = list(self.loaded_data[0].attributes.keys())
        for cube in self.loaded_data[1:]:
            cube_keys = list(cube.attributes.keys())
            self.identical_attributes = [
            key for key in identical_attributes
                if (key in cube_keys and
                    np.all(cube.attributes[key] == self.loaded_data[0].attributes[key]))]

        for cube in self.loaded_data:
            for key in list(cube.attributes):
                if key not in self.identical_attributes:
                    self.unique_attributes.append(cube.attributes[key])


    def display_data_filelist(self):
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".nc"):
                print(filename)


    def equalise_cubes(self):
        equalise_attributes(self.loaded_data)
        equalised_cubes = iris.cube.CubeList(self.loaded_data)
        self.equalised_cubes = equalised_cubes.merge()


    def get_unique_attributes(self):
        print(self.unique_attributes)

    def get_cordinates(self):
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".nc"):
                cube = iris.load_cube(data_dir + filename)
                for coord in cube.coords():
                    print(coord.name())





first_dataset = Dataset(data_dir, 'precipitation_flux')
first_dataset.display_data_filelist()
first_dataset.equalise_cubes()
first_dataset.get_unique_attributes()
#print(first_dataset)
#print(first_dataset.__dict__)