import os
import iris
from glob import glob
from cube_helper.cube_loader import (load_from_dir,
                                     load_from_filelist,
                                     _parse_directory,
                                     _sort_by_date,
                                     file_sort_by_earliest_date,
                                     sort_by_earliest_date)


def test_load_from_filelist():
    abs_path = os.path.dirname(os.path.abspath(__file__))
    filelist = ['test_data/realistic_3d/realistic_3d_0.nc',
                'test_data/realistic_3d/realistic_3d_1.nc',
                'test_data/realistic_3d/realistic_3d_2.nc']
    abs_filelist = []
    for file in filelist:
        abs_filelist.append(abs_path + '/' + file)
    test_load, test_names = load_from_filelist(abs_filelist,
                                               '.nc')
    print(test_names)
    assert isinstance(test_load, list)
    assert isinstance(test_names, list)
    for cube in test_load:
        assert isinstance(cube, iris.cube.Cube)
    for name in test_names:
        assert isinstance(name, str)
        assert os.path.exists(name)


def test_load_from_dir():
    abs_path = os.path.dirname(os.path.abspath(__file__))\
               + '/test_data/realistic_3d/'

    test_load, test_names = load_from_dir(abs_path, '.pp')
    assert isinstance(test_load, list)
    assert isinstance(test_names, list)
    for cube in test_load:
        assert isinstance(cube, iris.cube.Cube)
    for name in test_names:
        assert isinstance(name, str)
        assert os.path.exists(name)


def test_parse_directory():
    directory = 'test_data/realistic_3d/realistic_3d_0.nc'
    assert _parse_directory(directory) == '/test_data/' \
                                          'realistic_3d/' \
                                          'realistic_3d_0.nc/'

def test_sort_by_earliest_date():
    filepaths = glob('/project/champ/data/cmip5/output1/ICHEC/EC-EARTH/'
                     'rcp85/mon/atmos/Amon/r1i1p1/v20171115/tas/*.nc')
    test_load = [iris.load_cube(cube) for cube in filepaths]
    test_load = iris.cube.CubeList(test_load)
    test_load.sort(key=sort_by_earliest_date)
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
    filepaths.sort(key=file_sort_by_earliest_date)
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