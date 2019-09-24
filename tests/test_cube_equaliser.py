import unittest
import iris
from cube_helper.cube_loader import load_from_dir
from cube_helper.cube_equaliser import (equalise_attributes,
equalise_time_units, equalise_data_type, remove_attributes,
equalise_dim_coords, equalise_aux_coords, _sort_by_earliest_date)

class TestCubeEqualiser(unittest.TestCase):

    def test_equalise_attributes(self):
        filepath = 'test_data/air_temp'
        test_load = load_from_dir(filepath, filetype='.pp')
        equalise_attributes(test_load)
        for cubes in test_load:
            self.assertEqual(cubes.attributes, test_load[0].attributes)

    def test_unify_time_units(self):
        filepath = 'test_data/air_temp'
        test_load = load_from_dir(filepath, filetype='.pp')
        equalise_time_units(test_load)
        for index,cube in enumerate(test_load):
            for time_coords in cube.coords():
                if time_coords.units.is_time_reference():
                    self.assertEqual(cube[index].units.calendar,
                                     cube[index-1].units.calendar)

    def test_remove_attributes(self):
        filepath = 'test_data/air_temp'
        test_load = load_from_dir(filepath, filetype='.pp')
        remove_attributes(test_load)
        keys = list(test_load[0].attributes.keys())
        for cube in test_load:
            for key in keys:
                self.assertEqual(cube.attributes[key], '')

    def test_equalise_data_type(self):
        filepath = 'test_data/air_temp'
        test_load = load_from_dir(filepath, filetype='.pp')
        equalise_data_type(test_load)
        for cube in test_load:
            self.assertEqual(cube.dtype,'float32')
        equalise_data_type(test_load, 'float64')
        for cube in test_load:
            self.assertEqual(cube.dtype,'float64')
        equalise_data_type(test_load, 'int32')
        for cube in test_load:
            self.assertEqual(cube.dtype, 'int32')
        equalise_data_type(test_load, 'int64')
        for cube in test_load:
            self.assertEqual(cube.dtype, 'int64')

    def test_equalise_dim_coords(self):
        filepath = 'test_data/air_temp'
        test_load = load_from_dir(filepath, filetype='.pp')
        equalise_dim_coords(test_load)
        for cube in test_load:
            self.assertEqual(cube.dim_coords[0].name(), 'latitude')
            self.assertEqual(cube.dim_coords[1].name(), 'longitude')


    def test_equalise_aux_coords(self):
        filepath = '/project/champ/data/cmip5/output1/ICHEC/EC-EARTH/' \
                   'rcp85/mon/atmos/Amon/r1i1p1/v20171115/tas'
        test_load = load_from_dir(filepath, filetype='.nc')
        equalise_aux_coords(test_load)
        for cube in test_load:
            coords_list = [c.name() for c in cube.coords()]
            self.assertNotIn('height', coords_list)


    def test_sort_by_earliest_date(self):
        filepath = '/project/champ/data/cmip5/output1/ICHEC/EC-EARTH/' \
                   'rcp85/mon/atmos/Amon/r1i1p1/v20171115/tas'
        test_load = load_from_dir(filepath, filetype='.nc')
        cube_list = iris.cube.CubeList(test_load)
        cube_list.sort(key=_sort_by_earliest_date)
        self.assertEqual(cube_list[0].dim_coords[0].units.origin,
                         'days since 2006-01-01 00:00:00')
        self.assertEqual(cube_list[1].dim_coords[0].units.origin,
                         'days since 2010-01-01 00:00:00')
        self.assertEqual(cube_list[2].dim_coords[0].units.origin,
                         'days since 2020-01-01 00:00:00')
        self.assertEqual(cube_list[3].dim_coords[0].units.origin,
                         'days since 2030-01-01 00:00:00')
        self.assertEqual(cube_list[4].dim_coords[0].units.origin,
                         'days since 2040-01-01 00:00:00')
        self.assertEqual(cube_list[5].dim_coords[0].units.origin,
                         'days since 2050-01-01 00:00:00')
        self.assertEqual(cube_list[6].dim_coords[0].units.origin,
                         'days since 2060-01-01 00:00:00')
        self.assertEqual(cube_list[7].dim_coords[0].units.origin,
                         'days since 2070-01-01 00:00:00')
        self.assertEqual(cube_list[8].dim_coords[0].units.origin,
                         'days since 2080-01-01 00:00:00')
        self.assertEqual(cube_list[9].dim_coords[0].units.origin,
                         'days since 2090-01-01 00:00:00')
        self.assertEqual(cube_list[10].dim_coords[0].units.origin,
                         'days since 2100-1-1')



if __name__ == "__main__":
    unittest.main()

