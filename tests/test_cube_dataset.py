import unittest
import iris
from cube_helper.cube_loader import load_from_dir
from cube_helper.cube_dataset import CubeSet


class TestCubeDataset(unittest.TestCase):

    def test_initialisation(self):
        filepath = 'test_data/north_sea_ice'
        cube_list = load_from_dir(filepath, '.pp')
        cube_set = CubeSet(cube_list)
        self.assertIsInstance(cube_list, list)
        self.assertIsInstance(cube_set, iris.cube.CubeList)
                
if __name__ == "__main__":
    unittest.main()

