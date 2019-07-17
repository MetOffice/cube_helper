import iris
import os
import numpy as np
import unittest
from iris_test import Dataset

class TestIrisCmipWrapper(unittest.TestCase):

    def test_init_method(self):
        dataset = Dataset('data/')
        filelist = ['data/pr_Amon_HadGEM2-ES_rcp26_r1i1p1_200512-203011.nc',
                    'data/pr_Amon_HadGEM2-ES_rcp26_r1i1p1_203012-205511.nc',
                    'data/pr_Amon_HadGEM2-ES_rcp26_r1i1p1_205512-208011.nc',
                    'data/pr_Amon_HadGEM2-ES_rcp26_r1i1p1_208012-209911.nc',
                    'data/pr_Amon_HadGEM2-ES_rcp26_r1i1p1_209912-212411.nc',
                    'data/pr_Amon_HadGEM2-ES_rcp26_r1i1p1_212412-214911.nc',
                    'data/pr_Amon_HadGEM2-ES_rcp26_r1i1p1_214912-217411.nc',
                    'data/pr_Amon_HadGEM2-ES_rcp26_r1i1p1_217412-219911.nc',
                    'data/pr_Amon_HadGEM2-ES_rcp26_r1i1p1_219912-222411.nc',
                    'data/pr_Amon_HadGEM2-ES_rcp26_r1i1p1_222412-224911.nc',
                    'data/pr_Amon_HadGEM2-ES_rcp26_r1i1p1_224912-227411.nc',
                    'data/pr_Amon_HadGEM2-ES_rcp26_r1i1p1_227412-229911.nc',
                    'data/pr_Amon_HadGEM2-ES_rcp26_r1i1p1_229912-229912.nc']


        self.assertEqual(dataset.data_dir, 'data/')

        for file in dataset.data_filelist:
            self.assertIn(file, filelist)

        for file in dataset.data_filelist:
            self.assertTrue(file.endswith('.nc'),)

        self.assertEqual(dataset.unique_attributes, ['tracking_id', 'creation_date'])
        self.assertNotIn('tracking_id', dataset.identical_attributes)
        self.assertNotIn('creation_date', dataset.identical_attributes)

    def test_seperate_attributes(self):
        dataset = Dataset('data/')
        self.assertEqual(dataset.unique_attributes, ['tracking_id', 'creation_date'])
        self.assertNotIn('tracking_id', dataset.identical_attributes)
        self.assertNotIn('creation_date', dataset.identical_attributes)

    def test_cube_load(self):
        dataset = Dataset('data/')
        for filename in dataset.data_filelist:
            self.assertTrue(isinstance(filename, str))
        self.assertTrue(isinstance(dataset.loaded_cubes, list))

        cube_class_test = iris.load_cube('data/pr_Amon_HadGEM2-ES_rcp26_r1i1p1_200512-203011.nc')
        for cube in dataset.loaded_cubes:
            self.assertEqual(type(cube), type(cube_class_test))



if __name__ == '__main__':
    unittest.main()


