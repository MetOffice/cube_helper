import iris
from glob import glob
import os
import sys
import contextlib
from io import StringIO
from cube_helper.cube_equaliser import (_file_sort_by_earliest_date,
                                        _sort_by_earliest_date,
                                        equalise_attributes,
                                        equalise_time_units,
                                        equalise_aux_coords,
                                        equalise_dim_coords,
                                        equalise_data_type,
                                        remove_attributes,
                                        compare_cubes,
                                        equalise_all)


def test_equalise_attributes():
    abs_path = os.path.dirname(os.path.abspath(__file__))
    glob_path = abs_path + '/test_data/air_temp' + '/*.pp'
    filepaths = glob(glob_path)
    test_load = [iris.load_cube(cube) for cube in filepaths]
    test_load = equalise_attributes(test_load)
    for cubes in test_load:
        assert cubes.attributes == test_load[0].attributes


def test_equalise_time_units():
    abs_path = os.path.dirname(os.path.abspath(__file__))
    glob_path = abs_path + '/test_data/air_temp' + '/*.pp'
    filepaths = glob(glob_path)
    test_load = [iris.load_cube(cube) for cube in filepaths]
    test_load = equalise_time_units(test_load)
    for index, cube in enumerate(test_load):
        for time_coords in cube.coords():
            if time_coords.units.is_time_reference():
                assert cube[index].units.calendar == \
                       cube[index-1].units.calendar


def test_remove_attributes():
    abs_path = os.path.dirname(os.path.abspath(__file__))
    glob_path = abs_path + '/test_data/air_temp' + '/*.pp'
    filepaths = glob(glob_path)
    test_load = [iris.load_cube(cube) for cube in filepaths]
    remove_attributes(test_load)
    keys = list(test_load[0].attributes.keys())
    for cube in test_load:
        for key in keys:
            assert cube.attributes[key] == ''


def test_equalise_data_type():
    abs_path = os.path.dirname(os.path.abspath(__file__))
    glob_path = abs_path + '/test_data/air_temp' + '/*.pp'
    filepaths = glob(glob_path)
    test_load = [iris.load_cube(cube) for cube in filepaths]
    equalise_data_type(test_load)
    for cube in test_load:
        assert cube.dtype == 'float32'
    equalise_data_type(test_load, 'float64')
    for cube in test_load:
        assert cube.dtype == 'float64'
    equalise_data_type(test_load, 'int32')
    for cube in test_load:
        assert cube.dtype == 'int32'
    equalise_data_type(test_load, 'int64')
    for cube in test_load:
        assert cube.dtype == 'int64'


def test_equalise_dim_coords():
    abs_path = os.path.dirname(os.path.abspath(__file__))
    glob_path = abs_path + '/test_data/air_temp' + '/*.pp'
    filepaths = glob(glob_path)
    test_load = [iris.load_cube(cube) for cube in filepaths]
    test_load = equalise_dim_coords(test_load)
    for cube in test_load:
        assert cube.dim_coords[0].name() == 'latitude'
        assert cube.dim_coords[1].name() == 'longitude'


def test_equalise_aux_coords():
    filepaths = glob('/project/champ/data/cmip5/output1/ICHEC/EC-EARTH/'
                     'rcp85/mon/atmos/Amon/r1i1p1/v20171115/tas/*.nc')
    test_load = [iris.load_cube(cube) for cube in filepaths]
    test_load = equalise_aux_coords(test_load)
    for cube in test_load:
        coords_list = [c.name() for c in cube.coords()]
        assert 'height' not in coords_list


def test_compare_cubes():
    filepath = glob('/project/champ/data/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL'
                    '/piControl/r1i1p1f1/Amon/tasmin/gn/v20190628/*.nc')
    test_load = [iris.load_cube(cube) for cube in filepath]
    out = StringIO()
    with contextlib.redirect_stdout(out):
        compare_cubes(test_load)
    output = out.getvalue().strip()
    expected_output = """cube dim coordinates differ: 

	longitude coords inconsistent

	latitude coords inconsistent

cube attributes differ: 

	creation_date attribute inconsistent

	history attribute inconsistent

	tracking_id attribute inconsistent"""

    assert output == expected_output


def test_equalise_all():
    filepath = glob('/project/champ/data/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL'
                    '/piControl/r1i1p1f1/Amon/tasmin/gn/v20190628/*.nc')
    test_cubes = [iris.load_cube(cube) for cube in filepath]
    test_cubes = equalise_all(test_cubes)
    test_attr = list([cube.attributes.keys() for cube in test_cubes])
    assert "creation_date" not in test_attr
    assert "history" not in test_attr
    assert "trackind_id" not in test_attr


def test_sort_by_earliest_date():
    filepaths = glob('/project/champ/data/cmip5/output1/ICHEC/EC-EARTH/'
                     'rcp85/mon/atmos/Amon/r1i1p1/v20171115/tas/*.nc')
    test_load = [iris.load_cube(cube) for cube in filepaths]
    test_load = iris.cube.CubeList(test_load)
    test_load.sort(key=_sort_by_earliest_date)
    assert test_load[0].dim_coords[0].units.origin == 'days since 2006' \
                                                      '-01-01 00:00:00'
    assert test_load[1].dim_coords[0].units.origin == 'days since 2010' \
                                                      '-01-01 00:00:00'
    assert test_load[2].dim_coords[0].units.origin == 'days since 2020' \
                                                      '-01-01 00:00:00'
    assert test_load[3].dim_coords[0].units.origin == 'days since 2030' \
                                                      '-01-01 00:00:00'
    assert test_load[4].dim_coords[0].units.origin == 'days since 2040' \
                                                      '-01-01 00:00:00'
    assert test_load[5].dim_coords[0].units.origin == 'days since 2050' \
                                                      '-01-01 00:00:00'
    assert test_load[6].dim_coords[0].units.origin == 'days since 2060' \
                                                      '-01-01 00:00:00'
    assert test_load[7].dim_coords[0].units.origin == 'days since 2070' \
                                                      '-01-01 00:00:00'
    assert test_load[8].dim_coords[0].units.origin == 'days since 2080' \
                                                      '-01-01 00:00:00'
    assert test_load[9].dim_coords[0].units.origin == 'days since 2090' \
                                                      '-01-01 00:00:00'
    assert test_load[10].dim_coords[0].units.origin == 'days since 2100-1-1'


def test_file_sort_by_earliest_date():
    filepaths = glob('/project/champ/data/cmip5/output1/ICHEC/EC-EARTH/'
                     'rcp85/mon/atmos/Amon/r1i1p1/v20171115/tas/*.nc')
    filepaths.sort(key=_file_sort_by_earliest_date)
    test_load = [iris.load_cube(cube) for cube in filepaths]
    assert test_load[0].dim_coords[0].units.origin == 'days since 2006' \
                                                      '-01-01 00:00:00'
    assert test_load[1].dim_coords[0].units.origin == 'days since 2010' \
                                                      '-01-01 00:00:00'
    assert test_load[2].dim_coords[0].units.origin == 'days since 2020' \
                                                      '-01-01 00:00:00'
    assert test_load[3].dim_coords[0].units.origin == 'days since 2030' \
                                                      '-01-01 00:00:00'
    assert test_load[4].dim_coords[0].units.origin == 'days since 2040' \
                                                      '-01-01 00:00:00'
    assert test_load[5].dim_coords[0].units.origin == 'days since 2050' \
                                                      '-01-01 00:00:00'
    assert test_load[6].dim_coords[0].units.origin == 'days since 2060' \
                                                      '-01-01 00:00:00'
    assert test_load[7].dim_coords[0].units.origin == 'days since 2070' \
                                                      '-01-01 00:00:00'
    assert test_load[8].dim_coords[0].units.origin == 'days since 2080' \
                                                      '-01-01 00:00:00'
    assert test_load[9].dim_coords[0].units.origin == 'days since 2090' \
                                                      '-01-01 00:00:00'
    assert test_load[10].dim_coords[0].units.origin == 'days since 2100-1-1'
