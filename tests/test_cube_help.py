# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

import iris
from cube_helper.cube_help import load, concatenate, add_categorical
from glob import glob
import os

def test_concatenate():
    abs_path = os.path.dirname(os.path.abspath(__file__))
    glob_path = abs_path + '/test_data/realistic_3d_time' + '/*.nc'
    filepaths = glob(glob_path)
    test_load = [iris.load_cube(cube) for cube in filepaths]
    test_case_a = concatenate(test_load)
    test_load = iris.cube.CubeList(test_load)
    test_case_b = concatenate(test_load)
    assert isinstance(test_case_a, iris.cube.Cube)
    assert isinstance(test_case_b, iris.cube.Cube)


def test_load():
    abs_path = os.path.dirname(os.path.abspath(__file__))
    glob_path = abs_path + '/test_data/realistic_3d_time' + '/*.nc'
    filepaths = glob(glob_path)
    directory = abs_path + '/test_data/realistic_3d_time'
    test_case_a = load(filepaths)
    assert isinstance(test_case_a, iris.cube.Cube)
    assert test_case_a.dim_coords[0].units.origin == "hours" \
                                                     " since 1970-01-01" \
                                                     " 00:00:00"
    assert test_case_a.dim_coords[0].units.calendar == "gregorian"
    test_case_b = load(directory)
    assert test_case_b.dim_coords[0].units.origin == "hours" \
                                                     " since 1970-01-01" \
                                                     " 00:00:00"
    assert test_case_b.dim_coords[0].units.calendar == "gregorian"


def test_add_categorical():
    abs_path = os.path.dirname(os.path.abspath(__file__))
    glob_path = abs_path + '/test_data/realistic_3d_time' + '/*.nc'
    filepaths = glob(glob_path)
    test_case_a = load(filepaths)
    test_case_b = [iris.load_cube(cube) for cube in filepaths]
    test_categoricals = ["season_year", "season_number",
                          "season_membership", "season",
                          "year", "month_number",
                          "month_fullname", "month",
                          "day_of_month", "day_of_year",
                          "weekday_number", "weekday_fullname",
                          "weekday", "hour"]
    for categorical in test_categoricals:
        test_case_a = add_categorical(categorical, test_case_a)
        assert test_case_a.coord(categorical)
        test_case_a.remove_coord(categorical)

    for categorical in test_categoricals:
        for cube in test_case_b:
            cube = add_categorical(categorical, cube)
            assert cube.coord(categorical)
            cube.remove_coord(categorical)
