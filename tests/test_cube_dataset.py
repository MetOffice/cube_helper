import unittest
from cube_helper.cube_loader import load_from_dir
from cube_helper.cube_dataset import CubeSet


class TestCubeDataset(unittest.TestCase):

    def test_initialisation(self):
        