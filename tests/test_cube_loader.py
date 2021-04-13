# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.
import copy
import unittest
import os
import iris
from iris.tests import stock
import cf_units
from glob import glob
from cube_helper.cube_loader import (latest_version,
                                     _get_drs_version_string,
                                     load_from_dir,
                                     load_from_filelist,
                                     _parse_directory,
                                     _sort_by_date,
                                     file_sort_by_earliest_date,
                                     sort_by_earliest_date,
                                     _constraint_compatible,
                                     _fix_partial_datetime)


class TestCubeLoader(unittest.TestCase):

    def setUp(self):
        super(TestCubeLoader, self).setUp()
        abs_path = os.path.dirname(os.path.abspath(__file__))
        self.tmp_dir_time = abs_path + '/' + 'tmp_dir_time/'
        self.tmp_dir = abs_path + '/' + 'tmp_dir/'
        if not os.path.exists(self.tmp_dir_time):
            os.mkdir(self.tmp_dir_time)
        if not os.path.exists(self.tmp_dir):
            os.mkdir(self.tmp_dir)
        base_cube = stock.realistic_3d()
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

    def test_load_from_filelist(self):
        filelist = [self.tmp_dir + self.temp_1,
                    self.tmp_dir + self.temp_2,
                    self.tmp_dir + self.temp_1]
        test_load, test_names = load_from_filelist(filelist,
                                                   '.nc')
        self.assertIsInstance(test_load, list)
        self.assertIsInstance(test_names, list)
        for cube in test_load:
            self.assertIsInstance(cube, iris.cube.Cube)
        for name in test_names:
            self.assertIsInstance(name, str)
            self.assertTrue(os.path.exists(name))

    def test_load_from_dir(self):
        test_load, test_names = load_from_dir(self.tmp_dir, '.nc')
        self.assertIsInstance(test_load, list)
        self.assertIsInstance(test_names, list)
        for cube in test_load:
            self.assertIsInstance(cube, iris.cube.Cube)
        for name in test_names:
            self.assertIsInstance(name, str)
            self.assertTrue(os.path.exists(name))

    def test_parse_directory(self):
        directory = 'test_data/realistic_3d/realistic_3d_0.nc'
        self.assertEqual(_parse_directory(directory),
                         '/test_data/realistic_3d/realistic_3d_0.nc/')

    def test_sort_by_earliest_date(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepaths = glob(glob_path)
        test_load = [iris.load_cube(cube) for cube in filepaths]
        test_load = iris.cube.CubeList(test_load)
        test_load.sort(key=sort_by_earliest_date)
        self.assertEqual(test_load[0].dim_coords[0].units.origin,
                         "hours since 1970-01-01 00:00:00")
        self.assertEqual(test_load[1].dim_coords[0].units.origin,
                         "hours since 1980-01-01 00:00:00")
        self.assertEqual(test_load[2].dim_coords[0].units.origin,
                         "hours since 1990-01-01 00:00:00")

    def test_file_sort_by_earliest_date(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepaths = glob(glob_path)
        filepaths.sort(key=file_sort_by_earliest_date)
        test_load = [iris.load_cube(cube) for cube in filepaths]
        self.assertEqual(test_load[0].dim_coords[0].units.origin,
                         "hours since 1970-01-01 00:00:00")
        self.assertEqual(test_load[1].dim_coords[0].units.origin,
                         "hours since 1980-01-01 00:00:00")
        self.assertEqual(test_load[2].dim_coords[0].units.origin,
                         "hours since 1990-01-01 00:00:00")

    def test_constraint_compatible(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepath = glob(glob_path)[0]
        test_cube = iris.load_cube(filepath)
        test_cube_bounds = test_cube.copy()
        test_cube_bounds.coord('time').guess_bounds()
        test_constr_point = iris.Constraint(
            time=lambda cell: cell.point.month == 2)
        test_constr_pdt = iris.Constraint(
            time=iris.time.PartialDateTime(month=2))
        self.assertTrue(_constraint_compatible(test_cube,
                                               test_constr_point))
        self.assertTrue(_constraint_compatible(test_cube,
                                               test_constr_pdt))
        self.assertTrue(_constraint_compatible(test_cube_bounds,
                                               test_constr_point))
        self.assertFalse(_constraint_compatible(test_cube_bounds,
                                                test_constr_pdt))

    def test_fix_partial_datetime(self):
        test_cube = stock.realistic_3d()
        test_cube.coord('time').guess_bounds()
        test_constr_point = iris.Constraint(
            time=lambda cell: cell.point.day == 22)
        test_constr_pdt = iris.Constraint(
            time=iris.time.PartialDateTime(day=22))
        test_constr_full_pdt = iris.Constraint(
            time=iris.time.PartialDateTime(2014, 12, 22))
        test_constr_full_point = iris.Constraint(
            time=lambda cell:
            cell.point.year == 2014 and
            cell.point.month == 12 and
            cell.point.day == 22)
        fixed_constr_point = _fix_partial_datetime(test_constr_point)
        fixed_constr_pdt = _fix_partial_datetime(test_constr_pdt)
        fixed_constr_full_pdt = _fix_partial_datetime(test_constr_full_pdt)
        fixed_constr_full_point = _fix_partial_datetime(test_constr_full_point)
        self.assertNotIsInstance(fixed_constr_pdt._coord_values['time'],
                                 iris.time.PartialDateTime)
        self.assertNotIsInstance(fixed_constr_full_pdt._coord_values['time'],
                                 iris.time.PartialDateTime)
        self.assertNotIsInstance(fixed_constr_point._coord_values['time'],
                                 iris.time.PartialDateTime)
        cube_constr_point = test_cube.extract(fixed_constr_point).coord('time')
        cube_constr_pdt = test_cube.extract(fixed_constr_pdt).coord('time')
        cube_constr_full_pdt = test_cube.extract(
            fixed_constr_full_pdt).coord('time')
        cube_constr_full_point = test_cube.extract(
            fixed_constr_full_point).coord('time')
        self.assertEqual(cube_constr_point.points[0],
                         cube_constr_pdt.points[0])
        self.assertEqual(cube_constr_point.points[1],
                         cube_constr_pdt.points[1])
        self.assertEqual(cube_constr_full_point.points[0],
                         cube_constr_full_pdt.points[0])
        self.assertEqual(cube_constr_full_point.points[1],
                         cube_constr_full_pdt.points[1])

    def tearDown(self):
        super(TestCubeLoader, self).tearDown()
        if os.path.exists(self.tmp_dir + self.temp_1):
            os.remove(self.tmp_dir + self.temp_1)
        if os.path.exists(self.tmp_dir + self.temp_2):
            os.remove(self.tmp_dir + self.temp_2)
        if os.path.exists(self.tmp_dir + self.temp_3):
            os.remove(self.tmp_dir + self.temp_3)
        if os.path.exists(self.tmp_dir_time + self.temp_1_time):
            os.remove(self.tmp_dir_time + self.temp_1_time)
        if os.path.exists(self.tmp_dir_time + self.temp_2_time):
            os.remove(self.tmp_dir_time + self.temp_2_time)
        if os.path.exists(self.tmp_dir_time + self.temp_3_time):
            os.remove(self.tmp_dir_time + self.temp_3_time)
        os.removedirs(self.tmp_dir)
        os.removedirs(self.tmp_dir_time)


class TestLatestVersion(unittest.TestCase):
    """Test ch.latest_version()"""
    def setUp(self):
        # Display full diffs in event of failure
        self.maxDiff = None

    def test_one_var(self):
        input = [
            "/some/dir/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/amip/r1i1p1f3/Amon/hus/"
            "gn/v20190617/hus_Amon_HadGEM3-GC31-LL_amip_r1i1p1f3_gn_197901-201412.nc",
            "/some/dir/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/amip/r1i1p1f3/Amon/hus/"
            "gn/v20210401/hus_Amon_HadGEM3-GC31-LL_amip_r1i1p1f3_gn_197901-201412.nc",
        ]
        actual = latest_version(input)
        expected = [
            "/some/dir/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/amip/r1i1p1f3/Amon/hus/"
            "gn/v20210401/hus_Amon_HadGEM3-GC31-LL_amip_r1i1p1f3_gn_197901-201412.nc",
        ]
        self.assertEqual(expected, actual)

    def test_one_var_three_versions(self):
        input = [
            "/some/dir/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/amip/r1i1p1f3/Amon/hus/"
            "gn/v20190617/hus_Amon_HadGEM3-GC31-LL_amip_r1i1p1f3_gn_197901-201412.nc",
            "/some/dir/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/amip/r1i1p1f3/Amon/hus/"
            "gn/v20210401/hus_Amon_HadGEM3-GC31-LL_amip_r1i1p1f3_gn_197901-201412.nc",
            "/some/dir/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/amip/r1i1p1f3/Amon/hus/"
            "gn/v18500401/hus_Amon_HadGEM3-GC31-LL_amip_r1i1p1f3_gn_197901-201412.nc",
        ]
        actual = latest_version(input)
        expected = [
            "/some/dir/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/amip/r1i1p1f3/Amon/hus/"
            "gn/v20210401/hus_Amon_HadGEM3-GC31-LL_amip_r1i1p1f3_gn_197901-201412.nc",
        ]
        self.assertEqual(expected, actual)

    def test_two_vars(self):
        input = [
            "/some/dir/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/amip/r1i1p1f3/Amon/hus/"
            "gn/v20190617/hus_Amon_HadGEM3-GC31-LL_amip_r1i1p1f3_gn_197901-201412.nc",
            "/some/dir/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/amip/r1i1p1f3/Amon/hus/"
            "gn/v20210401/hus_Amon_HadGEM3-GC31-LL_amip_r1i1p1f3_gn_197901-201412.nc",
            "/some/dir/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/amip/r1i1p1f3/Amon/rlut/"
            "gn/v20210401/rlut_Amon_HadGEM3-GC31-LL_amip_r1i1p1f3_gn_197901-201412.nc",
        ]
        actual = latest_version(input)
        expected = [
            "/some/dir/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/amip/r1i1p1f3/Amon/hus/"
            "gn/v20210401/hus_Amon_HadGEM3-GC31-LL_amip_r1i1p1f3_gn_197901-201412.nc",
            "/some/dir/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/amip/r1i1p1f3/Amon/rlut/"
            "gn/v20210401/rlut_Amon_HadGEM3-GC31-LL_amip_r1i1p1f3_gn_197901-201412.nc",
        ]
        self.assertEqual(sorted(expected), sorted(actual))

    def test_input_unchanged(self):
        input = [
            "/some/dir/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/amip/r1i1p1f3/Amon/hus/"
            "gn/v20190617/hus_Amon_HadGEM3-GC31-LL_amip_r1i1p1f3_gn_197901-201412.nc",
            "/some/dir/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/amip/r1i1p1f3/Amon/hus/"
            "gn/v20210401/hus_Amon_HadGEM3-GC31-LL_amip_r1i1p1f3_gn_197901-201412.nc",
        ]
        original = copy.deepcopy(input)
        _actual = latest_version(input)
        self.assertEqual(original, input)


class TestGetDrsVersionString(unittest.TestCase):
    """Test cube_helper.cube_loader._get_drs_version_string()"""
    def test_normal_path(self):
        self.assertEqual(
            'v20320229',
            _get_drs_version_string('/some/path/CMIP8/var/v20320229/var.nc')
        )

    def test_get_version_on_own(self):
        self.assertEqual('v20320229', _get_drs_version_string('v20320229'))

    def test_first_of_two_versions(self):
        self.assertEqual('v20320229',
                         _get_drs_version_string('v20320229v20360229'))

    def test_bad_version(self):
        self.assertIsNone(
            _get_drs_version_string('/some/path/CMIP8/var/Z20320229/var.nc')
        )

    def test_blank_path(self):
        self.assertIsNone(_get_drs_version_string(''))


if __name__ == '__main__':
    unittest.main()
