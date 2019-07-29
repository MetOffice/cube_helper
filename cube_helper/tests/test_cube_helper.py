import sys
sys.path.append('/net/home/h01/jbedwell/Downloads/cube_helper/cube_helper')
import unittest
import iris
from cube_helper import CubeHelp




class TestCubeHelper(unittest.TestCase):

    def test_initilisation(self):
        example_case = CubeHelp('test_data/air_temp', opt_constraints='air_temperature', opt_filetype='.pp')
        self.assertEqual(example_case.directory, 'test_data/air_temp')
        self.assertEqual(example_case.opt_constraints, 'air_temperature')
        self.assertEqual(type(example_case.cube_dataset.loaded_cubes), list)
        self.assertEqual(type(example_case.cube_dataset.cube_list), iris.cube.CubeList)
        filelist = ['test_data/air_temp/air_temp_1.pp','test_data/air_temp/air_temp_2.pp',
                    'test_data/air_temp/air_temp_3.pp','test_data/air_temp/air_temp_4.pp'
                                            'test_data/air_temp/air_temp_5.pp']
        example_case = CubeHelp(filelist, opt_filetype='.pp')
        self.assertEqual(type(example_case.directory), list)
        single_load = iris.load_cube('test_data/air_temp/air_temp_1.pp')
        single_case = CubeHelp(single_load, opt_filetype='.pp')
        self.assertEqual(len(single_case.cube_dataset.loaded_cubes), 1)

    # def test_concatenated_cube(self):
    #     example_case = CubeHelp('test_data/north_sea_ice', opt_filetype='.pp')
    #     self.assertEqual(type(example_case.cube_dataset.cube_list), iris.cube.CubeList)
    #     test_method = example_case.merged_cube()
    #     self.assertEqual(type(test_method), iris.cube.Cube)
    #     self.assertEqual(test_method.ndim, 3)

    def test_concatenated(self):
        example_case = CubeHelp('test_data/north_sea_ice', opt_filetype='.pp')
        test_method = example_case.concatenated()
        self.assertEqual(type(test_method), iris.cube.CubeList)

    def test_merged(self):
        example_case = CubeHelp('test_data/north_sea_ice', opt_filetype='.pp')
        test_method = example_case.merged()
        self.assertEqual(type(test_method), iris.cube.CubeList)

    def test_merged_cube(self):
        example_case = CubeHelp('test_data/north_sea_ice', opt_filetype='.pp')
        test_method = example_case.merged_cube()
        self.assertEqual(type(test_method), iris.cube.Cube)
        self.assertEqual(test_method.ndim, 3)


    def test_convert_units(self):
        example_case = CubeHelp('test_data/air_temp', opt_filetype='.pp')
        example_case.convert_units('celsius')
        for cube in example_case.cube_dataset.loaded_cubes:
            self.assertEqual(cube.units, 'celsius')

if __name__ == "__main__":
    unittest.main()