# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

import unittest
from iris.tests import stock
import iris
import cube_helper as ch
from glob import glob
import os
import cf_units
import iris.coords as icoords
from iris.coord_systems import GeogCS, RotatedGeogCS
import numpy as np


class TestCubeHelp(unittest.TestCase):

    def _generate_extended_cube(self):
        cube_list = []
        lower_bound = 0
        upper_bound = 70
        period = 70
        data = np.arange(70 * 9 * 11).reshape((70, 9, 11))
        lat_pts = np.linspace(-4, 4, 9)
        lon_pts = np.linspace(-5, 5, 11)
        ll_cs = RotatedGeogCS(37.5, 177.5, ellipsoid=GeogCS(6371229.0))
        for i in range(0, 100):
            time_pts = np.linspace(lower_bound, upper_bound - 1, 70)
            lat = icoords.DimCoord(
                lat_pts,
                standard_name="grid_latitude",
                units="degrees",
                coord_system=ll_cs,
            )
            lon = icoords.DimCoord(
                lon_pts,
                standard_name="grid_longitude",
                units="degrees",
                coord_system=ll_cs,
            )
            time = icoords.DimCoord(
                time_pts,
                standard_name="time",
                units="days since 1970-01-01 00:00:00"
            )
            cube = iris.cube.Cube(
                data,
                standard_name="air_potential_temperature",
                units="K",
                dim_coords_and_dims=[(time, 0),
                                     (lat, 1),
                                     (lon, 2)],
                attributes={"source": "Iris test case"},
            )
            lower_bound = lower_bound + 70
            upper_bound = upper_bound + 70
            period = period + 70
            cube_list.append(cube)
        cube_list = iris.cube.CubeList(cube_list)
        cube = cube_list.concatenate_cube()
        return cube

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

    def test_add_categorical_compound(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepaths = glob(glob_path)
        test_case_a = ch.load(filepaths)
        test_case_a = ch.add_categorical(test_case_a,
                                         'annual_seasonal_mean')
        self.assertTrue(test_case_a.coord('season_year'))
        self.assertTrue(test_case_a.coord('clim_season'))

    def test_aggregate_categorical_compounds(self):
        test_cube_a = self._generate_extended_cube()
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'annual_seasonal_mean')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('time').bounds[0][0],
                         0)
        self.assertEqual(test_cube_a.coord('time').bounds[0][1],
                         58.0)
        self.assertEqual(test_cube_a.coord('time').points[0],
                         29.0)
        self.assertEqual(test_cube_a.coord('clim_season').points[0],
                         'djf')
        self.assertEqual(test_cube_a.coord('season_year').points[0],
                         1970)

    def test_aggregate_categorical_weekday(self):
        test_cube_a = self._generate_extended_cube()
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'weekday')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('weekday').points[0],
                         'Thu')
        self.assertEqual(test_cube_a.coord('weekday').points[2],
                         'Sat')
        self.assertEqual(test_cube_a.coord('weekday').points[4],
                         'Mon')
        self.assertEqual(test_cube_a.coord('weekday').points[6],
                         'Wed')
        self.assertEqual(test_cube_a.coord('time').points[0],
                         3496.5)
        self.assertEqual(test_cube_a.coord('time').points[2],
                         3498.5)
        self.assertEqual(test_cube_a.coord('time').points[4],
                         3500.5)
        self.assertEqual(test_cube_a.coord('time').points[6],
                         3502.5)

    def test_aggregate_categorical_weekday_fullname(self):
        test_cube_a = self._generate_extended_cube()
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'weekday_fullname')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('weekday_fullname').points[0],
                         'Thursday')
        self.assertEqual(test_cube_a.coord('weekday_fullname').points[2],
                         'Saturday')
        self.assertEqual(test_cube_a.coord('weekday_fullname').points[4],
                         'Monday')
        self.assertEqual(test_cube_a.coord('weekday_fullname').points[6],
                         'Wednesday')
        self.assertEqual(test_cube_a.coord('time').points[0],
                         3496.5)
        self.assertEqual(test_cube_a.coord('time').points[2],
                         3498.5)
        self.assertEqual(test_cube_a.coord('time').points[4],
                         3500.5)
        self.assertEqual(test_cube_a.coord('time').points[6],
                         3502.5)

    def test_aggregate_categorical_weekday_number(self):
        test_cube_a = self._generate_extended_cube()
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'weekday_number')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('weekday_number').points[0],
                         3)
        self.assertEqual(test_cube_a.coord('weekday_number').points[2],
                         5)
        self.assertEqual(test_cube_a.coord('weekday_number').points[4],
                         0)
        self.assertEqual(test_cube_a.coord('weekday_number').points[6],
                         2)
        self.assertEqual(test_cube_a.coord('time').points[0],
                         3496.5)
        self.assertEqual(test_cube_a.coord('time').points[2],
                         3498.5)
        self.assertEqual(test_cube_a.coord('time').points[4],
                         3500.5)
        self.assertEqual(test_cube_a.coord('time').points[6],
                         3502.5)

    def test_aggregate_categorical_month(self):
        test_cube_a = self._generate_extended_cube()
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'month')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('month').points[0],
                         'Jan')
        self.assertEqual(test_cube_a.coord('month').points[4],
                         'May')
        self.assertEqual(test_cube_a.coord('month').points[9],
                         'Oct')
        self.assertEqual(test_cube_a.coord('month').points[11],
                         'Dec')
        self.assertEqual(test_cube_a.coord('time').points[0],
                         3485.0)
        self.assertEqual(test_cube_a.coord('time').points[4],
                         3422.5)
        self.assertEqual(test_cube_a.coord('time').points[9],
                         3575.5)
        self.assertEqual(test_cube_a.coord('time').points[11],
                         3636.5)

    def test_aggregate_categorical_month_fullname(self):
        test_cube_a = self._generate_extended_cube()
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'month_fullname')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('month_fullname').points[0],
                         'January')
        self.assertEqual(test_cube_a.coord('month_fullname').points[4],
                         'May')
        self.assertEqual(test_cube_a.coord('month_fullname').points[9],
                         'October')
        self.assertEqual(test_cube_a.coord('month_fullname').points[11],
                         'December')
        self.assertEqual(test_cube_a.coord('time').points[0],
                         3485.0)
        self.assertEqual(test_cube_a.coord('time').points[4],
                         3422.5)
        self.assertEqual(test_cube_a.coord('time').points[9],
                         3575.5)
        self.assertEqual(test_cube_a.coord('time').points[11],
                         3636.5)

    def test_aggregate_categorical_month_number(self):
        test_cube_a = self._generate_extended_cube()
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'month_number')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('month_number').points[0],
                         1)
        self.assertEqual(test_cube_a.coord('month_number').points[4],
                         5)
        self.assertEqual(test_cube_a.coord('month_number').points[9],
                         10)
        self.assertEqual(test_cube_a.coord('month_number').points[11],
                         12)
        self.assertEqual(test_cube_a.coord('time').points[0],
                         3485.0)
        self.assertEqual(test_cube_a.coord('time').points[4],
                         3422.5)
        self.assertEqual(test_cube_a.coord('time').points[9],
                         3575.5)
        self.assertEqual(test_cube_a.coord('time').points[11],
                         3636.5)

    def test_aggregate_categorical_year(self):
        test_cube_a = self._generate_extended_cube()
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'year')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('year').points[0],
                         1970)
        self.assertEqual(test_cube_a.coord('year').points[4],
                         1974)
        self.assertEqual(test_cube_a.coord('year').points[9],
                         1979)
        self.assertEqual(test_cube_a.coord('year').points[14],
                         1984)
        self.assertEqual(test_cube_a.coord('time').points[0],
                         182.0)
        self.assertEqual(test_cube_a.coord('time').points[4],
                         1643.0)
        self.assertEqual(test_cube_a.coord('time').points[9],
                         3469.0)
        self.assertEqual(test_cube_a.coord('time').points[14],
                         5295.5)

    def test_aggregate_categorical_season_year(self):
        test_cube_a = self._generate_extended_cube()
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'season_year')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('season_year').points[0],
                         1970)
        self.assertEqual(test_cube_a.coord('season_year').points[4],
                         1974)
        self.assertEqual(test_cube_a.coord('season_year').points[9],
                         1979)
        self.assertEqual(test_cube_a.coord('season_year').points[14],
                         1984)
        self.assertEqual(test_cube_a.coord('time').points[0],
                         166.5)
        self.assertEqual(test_cube_a.coord('time').points[4],
                         1612.0)
        self.assertEqual(test_cube_a.coord('time').points[9],
                         3438.0)
        self.assertEqual(test_cube_a.coord('time').points[14],
                         5264.5)

    def test_aggregate_categorical_clim_season(self):
        test_cube_a = self._generate_extended_cube()
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'clim_season')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('clim_season').points[0],
                         'djf')
        self.assertEqual(test_cube_a.coord('clim_season').points[1],
                         'mam')
        self.assertEqual(test_cube_a.coord('clim_season').points[2],
                         'jja')
        self.assertEqual(test_cube_a.coord('clim_season').points[3],
                         'son')
        self.assertEqual(test_cube_a.coord('time').points[0],
                         3499.0)
        self.assertEqual(test_cube_a.coord('time').points[1],
                         3529.0)
        self.assertEqual(test_cube_a.coord('time').points[2],
                         3484.0)
        self.assertEqual(test_cube_a.coord('time').points[3],
                         3575.5)

    def test_aggregate_categorical_season(self):
        test_cube_a = self._generate_extended_cube()
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'season')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('season').points[0],
                         'djf')
        self.assertEqual(test_cube_a.coord('season').points[1],
                         'mam')
        self.assertEqual(test_cube_a.coord('season').points[2],
                         'jja')
        self.assertEqual(test_cube_a.coord('season').points[3],
                         'son')
        self.assertEqual(test_cube_a.coord('time').points[0],
                         3499.0)
        self.assertEqual(test_cube_a.coord('time').points[1],
                         3529.0)
        self.assertEqual(test_cube_a.coord('time').points[2],
                         3484.0)
        self.assertEqual(test_cube_a.coord('time').points[3],
                         3575.5)

    def test_aggregate_categorical_season_membership(self):
        test_cube_a = self._generate_extended_cube()
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'season_membership')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('season_membership').points[0],
                         True)

    def test_aggregate_categorical_day_of_year(self):
        test_cube_a = self._generate_extended_cube()
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'day_of_year')
        self.assertEqual(test_cube_a.coord('day_of_year').points[0],
                         1)
        self.assertEqual(test_cube_a.coord('day_of_year').points[47],
                         48)
        self.assertEqual(test_cube_a.coord('day_of_year').points[133],
                         134)
        self.assertEqual(test_cube_a.coord('day_of_year').points[260],
                         261)
        self.assertEqual(test_cube_a.coord('time').points[0],
                         3470.0)
        self.assertEqual(test_cube_a.coord('time').points[47],
                         3517.0)
        self.assertEqual(test_cube_a.coord('time').points[133],
                         3420.0)
        self.assertEqual(test_cube_a.coord('time').points[260],
                         3547.0)

    def test_aggregate_categorical_day_of_month(self):
        test_cube_a = self._generate_extended_cube()
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'day_of_month')
        self.assertEqual(test_cube_a.coord('day_of_month').points[0],
                         1)
        self.assertEqual(test_cube_a.coord('day_of_month').points[5],
                         6)
        self.assertEqual(test_cube_a.coord('day_of_month').points[10],
                         11)
        self.assertEqual(test_cube_a.coord('day_of_month').points[15],
                         16)
        self.assertEqual(test_cube_a.coord('day_of_month').points[20],
                         21)
        self.assertEqual(test_cube_a.coord('day_of_month').points[25],
                         26)
        self.assertEqual(test_cube_a.coord('time').points[0],
                         3499.5)
        self.assertEqual(test_cube_a.coord('time').points[5],
                         3490.5)
        self.assertEqual(test_cube_a.coord('time').points[10],
                         3495.5)
        self.assertEqual(test_cube_a.coord('time').points[15],
                         3500.5)

    def test_extract_categorical_compounds(self):
        test_cube_a = self._generate_extended_cube()
        constraint = iris.Constraint(clim_season='djf',
                                     season_year=lambda cell:
                                     cell >= 1970 and cell <= 1980)
        test_cube_a = ch.extract_categorical(test_cube_a,
                                             'annual_seasonal_mean',
                                             constraint=constraint)
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('time').bounds[0][0],
                         0)
        self.assertEqual(test_cube_a.coord('time').bounds[0][1],
                         58.0)
        self.assertEqual(test_cube_a.coord('time').points[0],
                         29.0)
        self.assertEqual(test_cube_a.coord('clim_season').points[0],
                         'djf')
        self.assertEqual(test_cube_a.coord('season_year').points[0],
                         1970)

    def test_extract_categorical_weekday(self):
        test_cube_a = self._generate_extended_cube()
        constraint = iris.Constraint(weekday='Sat')
        test_cube_a = ch.extract_categorical(test_cube_a,
                                             'weekday',
                                             constraint=constraint)
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('weekday').points[0],
                         'Sat')
        self.assertEqual(test_cube_a.coord('time').points[0],
                         3498.5)

    def test_extract_categorical_weekday_fullname(self):
        test_cube_a = self._generate_extended_cube()
        constraint = iris.Constraint(weekday_fullname='Saturday')
        test_cube_a = ch.extract_categorical(test_cube_a,
                                             'weekday_fullname',
                                             constraint=constraint)
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('weekday_fullname').points[0],
                         'Saturday')
        self.assertEqual(test_cube_a.coord('time').points[0],
                         3498.5)

    def test_extract_categorical_weekday_number(self):
        test_cube_a = self._generate_extended_cube()
        constraint = iris.Constraint(weekday_number=5)
        test_cube_a = ch.extract_categorical(test_cube_a,
                                             'weekday_number',
                                             constraint=constraint)
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('weekday_number').points[0],
                         5)
        self.assertEqual(test_cube_a.coord('time').points[0],
                         3498.5)

    def test_extract_categorical_month(self):
        test_cube_a = self._generate_extended_cube()
        constraint = iris.Constraint(month='Dec')
        test_cube_a = ch.extract_categorical(test_cube_a,
                                             'month',
                                             constraint=constraint)
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('month').points[0],
                         'Dec')
        self.assertEqual(test_cube_a.coord('time').points[0],
                         3636.5)

    def test_extract_categorical_month_fullname(self):
        test_cube_a = self._generate_extended_cube()
        constraint = iris.Constraint(month_fullname='December')
        test_cube_a = ch.extract_categorical(test_cube_a,
                                             'month_fullname',
                                             constraint=constraint)
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('month_fullname').points[0],
                         'December')
        self.assertEqual(test_cube_a.coord('time').points[0],
                         3636.5)

    def test_extract_categorical_month_number(self):
        test_cube_a = self._generate_extended_cube()
        constraint = iris.Constraint(month_number=12)
        test_cube_a = ch.extract_categorical(test_cube_a,
                                             'month_number',
                                             constraint=constraint)
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('month_number').points[0],
                         12)
        self.assertEqual(test_cube_a.coord('time').points[0],
                         3636.5)

    def test_extract_categorical_year(self):
        test_cube_a = self._generate_extended_cube()
        const = iris.Constraint(year=lambda cell: cell > 1970 and cell < 1976)
        test_cube_a = ch.extract_categorical(test_cube_a,
                                             'year',
                                             constraint=const)
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('year').points[0],
                         1971)
        self.assertEqual(test_cube_a.coord('year').points[4],
                         1975)
        self.assertEqual(test_cube_a.coord('time').points[0],
                         547.0)
        self.assertEqual(test_cube_a.coord('time').points[4],
                         2008.0)

    def test_extract_categorical_season_year(self):
        test_cube_a = self._generate_extended_cube()
        const = iris.Constraint(
            season_year=lambda cell: cell > 1970 and cell < 1976)
        test_cube_a = ch.extract_categorical(test_cube_a,
                                             'season_year',
                                             constraint=const)
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('season_year').points[0],
                         1971)
        self.assertEqual(test_cube_a.coord('season_year').points[4],
                         1975)
        self.assertEqual(test_cube_a.coord('time').points[0],
                         516.0)
        self.assertEqual(test_cube_a.coord('time').points[4],
                         1977.0)

    def test_extract_categorical_clim_season(self):
        test_cube_a = self._generate_extended_cube()
        constraint = iris.Constraint(clim_season='son')
        test_cube_a = ch.extract_categorical(test_cube_a,
                                             'clim_season',
                                             constraint=constraint)
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('clim_season').points[0],
                         'son')
        self.assertEqual(test_cube_a.coord('time').points[0],
                         3575.5)

    def test_extract_categorical_season(self):
        test_cube_a = self._generate_extended_cube()
        constraint = iris.Constraint(season='son')
        test_cube_a = ch.extract_categorical(test_cube_a,
                                             'season',
                                             constraint=constraint)
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('season').points[0],
                         'son')
        self.assertEqual(test_cube_a.coord('time').points[0],
                         3575.5)

    def test_extract_categorical_day_of_year(self):
        test_cube_a = self._generate_extended_cube()
        constraint = iris.Constraint(day_of_year=134)
        test_cube_a = ch.extract_categorical(test_cube_a,
                                             'day_of_year',
                                             constraint=constraint)
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('day_of_year').points[0],
                         134)
        self.assertEqual(test_cube_a.coord('time').points[0],
                         3420.0)

    def test_extract_categorical_day_of_month(self):
        test_cube_a = self._generate_extended_cube()
        constraint = iris.Constraint(
            day_of_month=lambda cell: cell > 0 and cell < 17)
        test_cube_a = ch.extract_categorical(test_cube_a,
                                             'day_of_month',
                                             constraint=constraint)
        self.assertEqual(test_cube_a.coord('day_of_month').points[0],
                         1)
        self.assertEqual(test_cube_a.coord('day_of_month').points[5],
                         6)
        self.assertEqual(test_cube_a.coord('day_of_month').points[10],
                         11)
        self.assertEqual(test_cube_a.coord('day_of_month').points[15],
                         16)
        self.assertEqual(test_cube_a.coord('time').points[0],
                         3499.5)
        self.assertEqual(test_cube_a.coord('time').points[5],
                         3490.5)
        self.assertEqual(test_cube_a.coord('time').points[10],
                         3495.5)
        self.assertEqual(test_cube_a.coord('time').points[15],
                         3500.5)

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
