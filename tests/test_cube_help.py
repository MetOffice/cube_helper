import unittest
import iris
import cube_helper
from cube_helper import CubeHelp


class TestCubeHelper(unittest.TestCase):

    def test_initilisation(self):
        example_case = CubeHelp('test_data/air_temp', filetype='.pp',
                                constraints='air_temperature')
        self.assertEqual(example_case.directory, 'test_data/air_temp')
        self.assertEqual(example_case.filetype, '.pp')
        self.assertEqual(example_case.constraints, 'air_temperature')
        self.assertIsInstance(example_case.cube_dataset, cube_helper.cube_dataset.CubeSet)
        filelist = ['test_data/air_temp/air_temp_1.pp',
                    'test_data/air_temp/air_temp_2.pp',
                    'test_data/air_temp/air_temp_3.pp',
                    'test_data/air_temp/air_temp_4.pp',
                    'test_data/air_temp/air_temp_5.pp']
        example_case = CubeHelp(filelist, filetype='.pp')
        self.assertIsInstance(example_case.directory, list)

    def test_get_concatenated_cube(self):
        filepath = '/project/champ/data/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/' \
                   'piControl/r1i1p1f1/Amon/tasmin/gn/v20190628'
        example_case = CubeHelp(filepath)
        example_case.equalise()
        test_method = example_case.get_concatenated_cube()
        self.assertIsInstance(test_method, iris.cube.Cube)
        self.assertEqual(test_method.ndim, 3)

    def test_concatenate_cube(self):
        filepath = '/project/champ/data/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/' \
                   'piControl/r1i1p1f1/Amon/tasmin/gn/v20190628'
        example_case = CubeHelp(filepath)
        example_case.equalise()
        example_case.concatenate_cube()
        self.assertIsInstance(example_case.cube_dataset, iris.cube.Cube)
        self.assertEqual(example_case.cube_dataset.ndim, 3)

    def test_get_concatenated(self):
        example_case = CubeHelp('test_data/north_sea_ice', filetype='.pp')
        test_method = example_case.get_concatenated()
        self.assertIsInstance(test_method, iris.cube.CubeList)

    def test_concatenate(self):
        example_case = CubeHelp('test_data/north_sea_ice', filetype='.pp')
        test_method = example_case.concatenate()
        self.assertIsInstance(example_case.cube_dataset, iris.cube.CubeList)

    def test_get_merged(self):
        example_case = CubeHelp('test_data/north_sea_ice', filetype='.pp')
        test_method = example_case.get_merged()
        self.assertIsInstance(test_method, iris.cube.CubeList)

    def test_get_merged_cube(self):
        example_case = CubeHelp('test_data/north_sea_ice', filetype='.pp')
        test_method = example_case.get_merged_cube()
        self.assertIsInstance(test_method, iris.cube.Cube)
        self.assertEqual(test_method.ndim, 3)

    def test_convert_units(self):
        example_case = CubeHelp('test_data/air_temp', filetype='.pp')
        example_case.convert_units('celsius')
        for cube in example_case.cube_dataset:
            self.assertEqual(cube.units, 'celsius')

    def test_collapsed_dimension(self):
        example_case = CubeHelp('test_data/north_sea_ice', filetype='.pp')
        example_case.collapsed_dimension('longitude')
        for cube in example_case.cube_dataset:
            self.assertEqual(cube.ndim, 1)

    def test_get_cube(self):
        example_case = CubeHelp('test_data/north_sea_ice', filetype='.pp')
        test = example_case.get_cube(0)
        self.assertIsInstance(test, iris.cube.Cube)

    def test_reset(self):
        example_case = CubeHelp('test_data/north_sea_ice', filetype='.pp')
        case_1 = example_case.cube_dataset
        example_case.reset()
        self.assertEqual(case_1, example_case.cube_dataset)


if __name__ == "__main__":
    unittest.main()
