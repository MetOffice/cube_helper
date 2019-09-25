import unittest
import iris
from cube_helper.cube_loader import (load_from_dir,
                                     load_from_filelist,
                                     _parse_directory)


class TestCubeLoader(unittest.TestCase):
    def test_load_from_filelist(self):
        filelist = ['test_data/air_temp/air_temp_1.pp',
                    'test_data/air_temp/air_temp_2.pp',
                    'test_data/air_temp/air_temp_3.pp',
                    'test_data/air_temp/air_temp_4.pp',
                    'test_data/air_temp/air_temp_5.pp']
        example_case = load_from_filelist(filelist, '.pp')
        self.assertIsInstance(example_case, list)

    def test_load_from_dir(self):
        example_case = load_from_dir(
            'test_data/air_temp/', '.pp')
        self.assertIsInstance(example_case, list)

    def test_parse_directory(self):
        directory = 'test_data/air_temp/air_temp_1.pp'
        self.assertEqual(_parse_directory(directory),
                         '/test_data/air_temp/air_temp_1.pp/')


if __name__ == "__main__":
    unittest.main()
