import os
import unittest
import iris
from ~/cube_helper import CubeHelper

class TestCubeHelper(unittest.TestCase):

    def test_initilisation(self):
        test_dict = {'opt_constraint': None, 'opt_filetype': '.nc', 'loaded_cubes': [], 'cube_list': None,
         'concatenated_cube': None, 'units': '', 'long_name': '', 'standard_name': '', 'is_unified': False,
         'is_loaded': False, 'is_concatenated': False}

        example_case = CubeHelper()
        self.assertEqual(example_case.__dict__, test_dict)