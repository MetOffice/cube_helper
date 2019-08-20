import unittest
import iris
from cube_helper.cube_loader import load_from_dir, load_from_filelist





class TestCubeLoader(unittest.TestCase):
    def test_load_from_filelist(self):
        filelist = ['test_data/air_temp/air_temp_1.pp', 'test_data/air_temp/air_temp_2.pp',
                    'test_data/air_temp/air_temp_3.pp', 'test_data/air_temp/air_temp_4.pp',
                                                        'test_data/air_temp/air_temp_5.pp']
        example_case = load_from_filelist(filelist, filetype='.pp')
        self.assertEqual(type(example_case), iris.cube.CubeList)

    def test_load_from_dir(self):
        example_case = load_from_dir('test_data/air_temp', filetype='.pp')
        self.assertEqual(type(example_case), iris.cube.CubeList)


if __name__ == "__main__":
    unittest.main()
