import sys
sys.path.append('/net/home/h01/jbedwell/Downloads/cube_helper/cube_helper')
import unittest
from cube_loader import CubeLoader
from cube_equaliser import equalise_attributes,unify_time_units,unify_data_type,remove_attributes

class TestCubeEqualiser(unittest.TestCase):

    def test_equalise_attributes(self):
        filepath = '/project/champ/data/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/piControl/r1i1p1f1/Amon/tasmin/gn/v20190628'
        test_load = CubeLoader.load_from_dir(filepath)
        equalise_attributes(test_load)
        for cubes in test_load:
            self.assertEqual(cubes.attributes, test_load[0].attributes)


if __name__ == "__main__":
    unittest.main()

