import os
import unittest
import iris
from ..cube_helper.cube_helper import CubeHelp

class TestCubeHelper(unittest.TestCase):

    def test_initilisation(self):
        example_case = CubeHelp('data', opt_constraints='air_temperature')
        self.assertEqual(example_case.directory, 'data')
        self.assertEqual(example_case.opt_constraints, 'air_temperature')
        self.assertEqual(type(example_case.cube_dataset.loaded_cubes), list)
        self.assertEqual(type(example_case.cube_dataset.cube_list), iris.cube.CubeList)
        file_list =   ['cube_helper/data/tasmin_Amon_HadGEM3-GC31-LL_piControl_r1i1p1f1_gn_185001-194912.nc',
                        'cube_helper/data/tasmin_Amon_HadGEM3-GC31-LL_piControl_r1i1p1f1_gn_195001-204912.nc',
                        'cube_helper/data/tasmin_Amon_HadGEM3-GC31-LL_piControl_r1i1p1f1_gn_205001-214912.nc',
                        'cube_helper/data/tasmin_Amon_HadGEM3-GC31-LL_piControl_r1i1p1f1_gn_215001-224912.nc',
                        'cube_helper/data/tasmin_Amon_HadGEM3-GC31-LL_piControl_r1i1p1f1_gn_225001-234912.nc']
        example_case = CubeHelp(file_list)
        self.assertEqual(type(example_case.directory), list)

    def test_concatenated_cube(self):
        example_case = CubeHelp('data')
        self.assertEqual(example_case.concatenated_cube(), iris.cube.CubeList)
        test_method = example_case.concatenated_cube()
        self.assertEqual(type(test_method), iris.cube.Cube)
        self.assertEqual(test_method.ndim, 3)




if __name__ == "__main__":
    unittest.main()
    unittest.main()