# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.
import cube_helper as ch
from common import _generate_ocean_cube, _redirect_stdout
import unittest
import cf_units
from glob import glob
import os
import iris
import iris.coords
from iris.tests import stock
import platform
if float(platform.python_version()[0:3]) <= 2.7:
    from io import BytesIO as IO
else:
    from io import StringIO as IO


class TestCubeEqualiser(unittest.TestCase):

    def setUp(self):
        super(TestCubeEqualiser, self).setUp()
        abs_path = os.path.dirname(os.path.abspath(__file__))
        self.tmp_dir = abs_path + '/' + 'tmp_dir/'
        self.tmp_dir_aux = abs_path + '/' + 'tmp_dir_aux/'
        self.tmp_dir_attr = abs_path + '/' + 'tmp_dir_attr/'
        self.tmp_dir_time = abs_path + '/' + 'tmp_dir_time/'
        if not os.path.exists(self.tmp_dir):
            os.mkdir(self.tmp_dir)
        if not os.path.exists(self.tmp_dir_attr):
            os.mkdir(self.tmp_dir_attr)
        if not os.path.exists(self.tmp_dir_aux):
            os.mkdir(self.tmp_dir_aux)
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
        cube_1 = base_cube[0:2]
        cube_2 = base_cube[2:4]
        cube_3 = base_cube[4:]
        self.temp_1 = 'temp_1.nc'
        self.temp_2 = 'temp_2.nc'
        self.temp_3 = 'temp_3.nc'
        iris.save(cube_1, self.tmp_dir + self.temp_1)
        iris.save(cube_2, self.tmp_dir + self.temp_2)
        iris.save(cube_3, self.tmp_dir + self.temp_3)
        cube_1 = base_cube[0:2]
        cube_2 = base_cube[2:4]
        cube_3 = base_cube[4:]
        cube_2.attributes['history'] = 'some differing attributes'
        cube_2.attributes['creation_date'] = 'life day'
        cube_3.attributes['tracking_id'] = 'askbjQODOQwd210934AS'
        self.temp_1_attr = 'temp_1_attr.nc'
        self.temp_2_attr = 'temp_2_attr.nc'
        self.temp_3_attr = 'temp_3_attr.nc'
        iris.save(cube_1, self.tmp_dir_attr + self.temp_1_attr)
        iris.save(cube_2, self.tmp_dir_attr + self.temp_2_attr)
        iris.save(cube_3, self.tmp_dir_attr + self.temp_3_attr)
        cube_1 = base_cube[0:2]
        cube_2 = base_cube[2:4]
        cube_3 = base_cube[4:]
        height_coord = iris.coords.AuxCoord(2,
                                            standard_name='height',
                                            long_name='height',
                                            var_name='height',
                                            units='m')
        cube_2.add_aux_coord(height_coord)
        self.temp_1_aux = 'temp_1_aux.nc'
        self.temp_2_aux = 'temp_2_aux.nc'
        self.temp_3_aux = 'temp_3_aux.nc'
        iris.save(cube_1, self.tmp_dir_aux + self.temp_1_aux)
        iris.save(cube_2, self.tmp_dir_aux + self.temp_2_aux)
        iris.save(cube_3, self.tmp_dir_aux + self.temp_3_aux)

    def test_equalise_attributes(self):
        glob_path = self.tmp_dir_attr + '*.nc'
        print(glob_path)
        filepaths = glob(glob_path)
        test_load = [iris.load_cube(cube) for cube in filepaths]
        test_load = ch.equalise_attributes(test_load)
        for cubes in test_load:
            self.assertEqual(cubes.attributes, test_load[0].attributes)

    def test_equalise_time_units(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepaths = glob(glob_path)
        test_load = [iris.load_cube(cube) for cube in filepaths]
        test_load = ch.equalise_time_units(test_load)
        test_calendar = test_load[0].dim_coords[0].units.calendar
        test_origin = test_load[0].dim_coords[0].units.origin
        for cube in test_load:
            for time_coords in cube.coords():
                if time_coords.units.is_time_reference():
                    self.assertEqual(test_calendar,
                                     time_coords.units.calendar)
                    self.assertEqual(test_origin,
                                     time_coords.units.origin)

    def test_remove_attributes(self):
        glob_path = self.tmp_dir + '*.nc'
        filepaths = glob(glob_path)
        test_load = [iris.load_cube(cube) for cube in filepaths]
        ch.remove_attributes(test_load)
        keys = list(test_load[0].attributes.keys())
        for cube in test_load:
            for key in keys:
                self.assertEqual(cube.attributes[key], '')

    def test_equalise_data_type(self):
        glob_path = self.tmp_dir + '*.nc'
        filepaths = glob(glob_path)
        test_load = [iris.load_cube(cube) for cube in filepaths]
        ch.equalise_data_type(test_load)
        for cube in test_load:
            self.assertEqual(cube.dtype, 'float32')
        ch.equalise_data_type(test_load, 'float64')
        for cube in test_load:
            self.assertEqual(cube.dtype, 'float64')
        ch.equalise_data_type(test_load, 'int32')
        for cube in test_load:
            self.assertEqual(cube.dtype, 'int32')
        ch.equalise_data_type(test_load, 'int64')
        for cube in test_load:
            self.assertEqual(cube.dtype, 'int64')

    def test_equalise_dim_coords(self):
        glob_path = self.tmp_dir + '*.nc'
        filepaths = glob(glob_path)
        test_load = [iris.load_cube(cube) for cube in filepaths]
        test_load = ch.equalise_dim_coords(test_load)
        for cube in test_load:
            self.assertEqual(cube.dim_coords[0].name(), 'time')
            self.assertEqual(cube.dim_coords[1].name(), 'grid_latitude')

    def test_equalise_dim_coords_ocean(self):
        test_load = _generate_ocean_cube()
        test_load[10].coord('time').var_name = 'bananas'
        test_load = ch.equalise_dim_coords(test_load)
        for cube in test_load:
            self.assertEqual(cube.dim_coords[0].name(), 'time')
            self.assertEqual(cube.dim_coords[1].name(),
                             'cell index along first dimension')
            self.assertEqual(cube.dim_coords[2].name(),
                             'cell index along second dimension')

    def test_equalise_aux_coords(self):
        glob_path = self.tmp_dir_aux + '*.nc'
        filepaths = glob(glob_path)
        test_load = [iris.load_cube(cube) for cube in filepaths]
        test_load = ch.equalise_aux_coords(test_load)
        for cube in test_load:
            coords_list = [c.name() for c in cube.coords()]
            self.assertIn('height', coords_list)

    def test_compare_cubes(self):
        glob_path = self.tmp_dir_aux + '*.nc'
        filepaths = glob(glob_path)
        test_load = [iris.load_cube(cube) for cube in filepaths]
        out = IO()
        with _redirect_stdout(out):
            ch.compare_cubes(test_load)
        output = out.getvalue().strip()
        expected_output = "cube aux coordinates differ: " + \
                          "\n\n\theight coords inconsistent"
        self.assertEqual(output, expected_output)

    def test_compare_cubes_incompatible(self):
        test_case_a = stock.simple_2d()
        test_case_b = stock.simple_3d()
        test_cubes = [test_case_a, test_case_b]
        self.assertRaises(OSError,
                          ch.compare_cubes,
                          test_cubes)

    def test_compare_cubes_ocean(self):
        test_load = _generate_ocean_cube()
        out = IO()
        with _redirect_stdout(out):
            ch.compare_cubes(test_load)
        output = out.getvalue().strip()
        expected_output = ""
        self.assertEqual(output, expected_output)

    def test_equalise_all(self):
        glob_path = self.tmp_dir_attr + '*.nc'
        filepaths = glob(glob_path)
        test_cubes = [iris.load_cube(cube) for cube in filepaths]
        test_cubes = ch.equalise_all(test_cubes)
        test_attr = list([cube.attributes.keys() for cube in test_cubes])
        self.assertNotIn('creation_date', test_attr)
        self.assertNotIn('history', test_attr)
        self.assertNotIn('tracking_id', test_attr)

    def tearDown(self):
        super(TestCubeEqualiser, self).tearDown()
        if os.path.exists(self.tmp_dir + self.temp_1):
            os.remove(self.tmp_dir + self.temp_1)
        if os.path.exists(self.tmp_dir_aux + self.temp_1_aux):
            os.remove(self.tmp_dir_aux + self.temp_1_aux)
        if os.path.exists(self.tmp_dir_attr + self.temp_1_attr):
            os.remove(self.tmp_dir_attr + self.temp_1_attr)
        if os.path.exists(self.tmp_dir_time + self.temp_1_time):
            os.remove(self.tmp_dir_time + self.temp_1_time)
        if os.path.exists(self.tmp_dir + self.temp_2):
            os.remove(self.tmp_dir + self.temp_2)
        if os.path.exists(self.tmp_dir_aux + self.temp_2_aux):
            os.remove(self.tmp_dir_aux + self.temp_2_aux)
        if os.path.exists(self.tmp_dir_attr + self.temp_2_attr):
            os.remove(self.tmp_dir_attr + self.temp_2_attr)
        if os.path.exists(self.tmp_dir_time + self.temp_2_time):
            os.remove(self.tmp_dir_time + self.temp_2_time)
        if os.path.exists(self.tmp_dir + self.temp_3):
            os.remove(self.tmp_dir + self.temp_3)
        if os.path.exists(self.tmp_dir_aux + self.temp_3_aux):
            os.remove(self.tmp_dir_aux + self.temp_3_aux)
        if os.path.exists(self.tmp_dir_attr + self.temp_3_attr):
            os.remove(self.tmp_dir_attr + self.temp_3_attr)
        if os.path.exists(self.tmp_dir_time + self.temp_3_time):
            os.remove(self.tmp_dir_time + self.temp_3_time)
        os.removedirs(self.tmp_dir)
        os.removedirs(self.tmp_dir_aux)
        os.removedirs(self.tmp_dir_attr)
        os.removedirs(self.tmp_dir_time)


if __name__ == '__main__':
    unittest.main()
