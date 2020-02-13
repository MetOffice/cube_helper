# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

import unittest
from iris.tests import stock
import iris
import cube_helper as ch
from glob import glob
import os
import cf_units

class TestCubeHelp(unittest.TestCase):

    def setUp(self):
        super(TestCubeHelp, self).setUp()
        abs_path = os.path.dirname(os.path.abspath(__file__))
        self.tmp_dir_time = abs_path + '/' + 'tmp_dir_time/'
        if not os.path.exists(self.tmp_dir_time):
            os.mkdir(self.tmp_dir_time)
        base_cube = stock.realistic_3d()
        cube_1 = base_cube[0:2]
        cube_2 = base_cube[2:4]
        cube_3 = base_cube[4:]
        new_time = cf_units.Unit('hours since 1980-01-01 00:00:00',
                                 'gregorian')
        cube_2.dim_coords[0].convert_units(new_time)
        new_time = cf_units.Unit('hours since 1990-01-01 00:00:00',
                                 'gregorian')
        cube_3.dim_coords[0].convert_units(new_time)
        self.temp_1_time = 'temp_1_time.nc'
        self.temp_2_time = 'temp_2_time.nc'
        self.temp_3_time = 'temp_3_time.nc'
        iris.save(cube_1, self.tmp_dir_time + self.temp_1_time)
        iris.save(cube_2, self.tmp_dir_time + self.temp_2_time)
        iris.save(cube_3, self.tmp_dir_time + self.temp_3_time)


    def test_concatenate(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepaths = glob(glob_path)
        test_load = [iris.load_cube(cube) for cube in filepaths]
        test_case_a = ch.concatenate(test_load)
        test_load = iris.cube.CubeList(test_load)
        test_case_b = ch.concatenate(test_load)
        self.assertIsInstance(test_case_a, iris.cube.Cube)
        self.assertIsInstance(test_case_b, iris.cube.Cube)



    def test_load(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepaths = glob(glob_path)
        directory = self.tmp_dir_time
        test_case_a = ch.load(filepaths)
        self.assertIsInstance(test_case_a, iris.cube.Cube)
        self.assertEqual(test_case_a.dim_coords[0].units.origin,
                         "hours since 1970-01-01 00:00:00")
        self.assertEqual(test_case_a.dim_coords[0].units.calendar,
                         "gregorian")
        test_case_b = ch.load(directory)
        self.assertEqual(test_case_b.dim_coords[0].units.origin,
                         "hours since 1970-01-01 00:00:00")
        self.assertEqual(test_case_b.dim_coords[0].units.calendar,
                         "gregorian")


    def test_add_categorical(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepaths = glob(glob_path)
        test_case_a = ch.load(filepaths)
        test_case_b = [iris.load_cube(cube) for cube in filepaths]
        test_categoricals = ["season_year", "season_number",
                              "season_membership", "season",
                              "year", "month_number",
                              "month_fullname", "month",
                              "day_of_month", "day_of_year",
                              "weekday_number", "weekday_fullname",
                              "weekday", "hour"]
        for categorical in test_categoricals:
            test_case_a = ch.add_categorical(test_case_a, categorical)
            self.assertTrue(test_case_a.coord(categorical))
            test_case_a.remove_coord(categorical)

        for categorical in test_categoricals:
            for cube in test_case_b:
                cube = ch.add_categorical(cube, categorical)
                self.assertTrue(cube.coord(categorical))
                cube.remove_coord(categorical)
        test_case_a = ch.load(filepaths)
        test_case_a = ch.add_categorical(test_case_a,
                                         ["clim_season",
                                          "season_year"])
        self.assertTrue(test_case_a.coord("clim_season"))
        self.assertTrue(test_case_a.coord("season_year"))


    def test_aggregate_categorical(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepaths = glob(glob_path)
        test_cube_a = ch.load(filepaths)
        test_cube_b = ch.load(filepaths)
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               ["clim_season", 'season_year'])
        self.assertIsInstance(test_cube_a, iris.cube.Cube)
        iris.coord_categorisation.add_season(test_cube_b, 'time', name='clim_season')
        iris.coord_categorisation.add_season_year(test_cube_b, 'time', name='season_year')
        test_cube_b = test_cube_b.aggregated_by(["season_year",
                                                 'clim_season'],
                                                iris.analysis.MEAN)
        self.assertTrue((test_cube_a == test_cube_b).all())

    def tearDown(self):
        super(TestCubeHelp, self).tearDown()
        if os.path.exists(self.tmp_dir_time + self.temp_1_time):
            os.remove(self.tmp_dir_time + self.temp_1_time)
        if os.path.exists(self.tmp_dir_time + self.temp_2_time):
            os.remove(self.tmp_dir_time + self.temp_2_time)
        if os.path.exists(self.tmp_dir_time + self.temp_3_time):
            os.remove(self.tmp_dir_time + self.temp_3_time)
        os.removedirs(self.tmp_dir_time)

if __name__ == '__main__':
    unittest.main()
