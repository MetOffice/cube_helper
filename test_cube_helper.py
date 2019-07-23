import os
import unittest
import iris
from cube_helper import CubeHelper

class TestCubeHelper(unittest.TestCase):

    def test_initilisation(self):
        example_case = CubeHelper('data', opt_constraints='air_temperature')
        self.assertEqual(example_case.directory, 'data')
        self.assertEqual(example_case.opt_constraints, 'air_temperature')
        self.assertEqual(type(example_case.cube_dataset.loaded_cubes), type([]))

if __name__ == "__main__":
    unittest.main()