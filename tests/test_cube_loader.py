# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

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
    test_load, test_names = load_from_dir(abs_path, '.nc')
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

#No filepaths needed, REFRACTOR:
def test_sort_by_earliest_date():
    abs_path = os.path.dirname(os.path.abspath(__file__))
    glob_path = abs_path + '/test_data/realistic_3d_time' + '/*.nc'
    filepaths = glob(glob_path)
    test_load = [iris.load_cube(cube) for cube in filepaths]
    test_load = iris.cube.CubeList(test_load)
    test_load.sort(key=sort_by_earliest_date)
    assert test_load[0].dim_coords[0].units.origin == "hours" \
                                                     " since 1970-01-01" \
                                                     " 00:00:00"
    assert test_load[1].dim_coords[0].units.origin == "hours" \
                                                     " since 1980-01-01" \
                                                     " 00:00:00"
    assert test_load[2].dim_coords[0].units.origin == "hours" \
                                                     " since 1990-01-01" \
                                                     " 00:00:00"


def test_file_sort_by_earliest_date():
    abs_path = os.path.dirname(os.path.abspath(__file__))
    glob_path = abs_path + '/test_data/realistic_3d_time' + '/*.nc'
    filepaths = glob(glob_path)
    filepaths.sort(key=file_sort_by_earliest_date)
    test_load = [iris.load_cube(cube) for cube in filepaths]
    assert test_load[0].dim_coords[0].units.origin == "hours" \
                                                     " since 1970-01-01" \
                                                     " 00:00:00"
    assert test_load[1].dim_coords[0].units.origin == "hours" \
                                                     " since 1980-01-01" \
                                                     " 00:00:00"
    assert test_load[2].dim_coords[0].units.origin == "hours" \
                                                     " since 1990-01-01" \
                                                     " 00:00:00"