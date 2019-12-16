# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

from __future__ import (absolute_import, division, print_function)
import iris
import iris.coord_categorisation
from six import string_types
from cube_helper.cube_loader import load_from_filelist, load_from_dir
from cube_helper.cube_equaliser import (compare_cubes,
                                        examine_dim_bounds,
                                        equalise_all)


def load(directory, filetype='.nc', constraints=None):
    """
    A function that loads and concatenates iris Cubes.

    Args:
        directory: A String specifying the directory or filename of the Cubes
        you wish to concatenate. Accepts either directory location or a list
        or glob object of individual Cubes.

        filetype: Extension of iris Cubes to Load. set to '.nc' by default.
        constraints: Any constraints to be applied to Cubes on load.

    Returns:
        result: A concatenated iris Cube.
    """
    if isinstance(directory, string_types):
        loaded_cubes, cube_files = load_from_dir(
            directory, filetype, constraints)
        if not loaded_cubes:
            raise OSError("No cubes loaded")
        else:
            compare_cubes(loaded_cubes)
            result = equalise_all(loaded_cubes)
            result = iris.cube.CubeList(result)
            try:
                result = result.concatenate_cube()
            except iris.exceptions.ConcatenateError:
                print("\nOops, there was an error in concatenation\n")
                examine_dim_bounds(result, cube_files)
            return result

    elif isinstance(directory, list):
        loaded_cubes, cube_files = load_from_filelist(
            directory, filetype, constraints)

        if not loaded_cubes:
            raise OSError("No cubes loaded")
        else:
            compare_cubes(loaded_cubes)
            result = equalise_all(loaded_cubes)
            result = iris.cube.CubeList(result)
            try:
                result = result.concatenate_cube()
            except iris.exceptions.ConcatenateError:
                print("\nOops, there was an error in concatenation\n")
                examine_dim_bounds(result, cube_files)
            return result


def _add_categorical(cater_name, cube, coord, season, seasons):
    """
    Private function implementing the logic needed to select different
    catergorisations for add_categorical()
    """
    if cater_name == 'season_year':
        iris.coord_categorisation.add_season_year(
            cube, coord, name='season_year')

    elif cater_name == 'season_membership':
        iris.coord_categorisation.add_season_membership(
            cube, coord, name='season_membership',
            season=season)

    elif cater_name == 'season_number' or cater_name == 'number':
        iris.coord_categorisation.add_season_number(
            cube, coord, name='season_number',
            seasons=seasons)

    elif cater_name == 'clim_season' or cater_name == 'season':
        iris.coord_categorisation.add_season(
            cube, coord, name='season', seasons=seasons)

    elif cater_name == 'year':
        iris.coord_categorisation.add_year(
            cube, coord, name='year')

    elif cater_name == 'month_number':
        iris.coord_categorisation.add_month_number(
            cube, coord, name='month_number')

    elif cater_name == 'month_fullname':
        iris.coord_categorisation.add_month_fullname(
            cube, coord, name='month_fullname')

    elif cater_name == 'month':
        iris.coord_categorisation.add_month(
            cube, coord, name='month')

    elif cater_name == 'day_of_month':
        iris.coord_categorisation.add_day_of_month(
            cube, coord, name='day_of_month')

    elif cater_name == 'day_of_year':
        iris.coord_categorisation.add_day_of_year(
            cube, coord, name='day_of_year')

    elif cater_name == 'weekday_number':
        iris.coord_categorisation.add_weekday_number(
            cube, coord, name='weekday_number')

    elif cater_name == 'weekday_fullname':
        iris.coord_categorisation.add_weekday_fullname(
            cube, coord, name='weekday_fullname')

    elif cater_name == 'weekday':
        iris.coord_categorisation.add_weekday(
            cube, coord, name='weekday')

    elif cater_name == 'hour':
        iris.coord_categorisation.add_hour(
            cube, coord, name='hour')
    else:
        pass


def add_categorical(cater_name, cubes, coord='time', season='djf',
                    seasons=('djf', 'mam', 'jja', 'son')):
    """
    Adds a coordinate catergorisation to the iterable of iris Cubes.

    Args:
        cater_name: A string specifying the catergorisation you wish to add.
        cubes: A list of Loaded Cubes or a CubeList.
        coords: the coordinate you wish to add a catergoisation to. Set
        to 'time' by default.
        season: The season you need for the catergorisation (where required).
        set to 'djf' by default.
        seasons: The seasons required for catergorisation.

    Returns:
        cubes: An iterable of Cubes, either a list of loaded Cubes
        or an iris CubeList.
    """
    if isinstance(cubes, iris.cube.CubeList) or isinstance(cubes, list):
        for cube in cubes:
            _add_categorical(cater_name, cube,
                             coord, season, seasons)
        return cubes

    else:
        _add_categorical(cater_name, cubes,
                         coord, season, seasons)
        return cubes


def concatenate(cubes):
    """
    Concatentates a list of iris Cubes. Equalises the list of cubes first
    then concatenates.

    Args:
         cubes: An iterable of iris Cubes to concatenate, either list of
         loaded cubes or a CubeList

    Returns:
        cube: A concatenated iris Cube.
    """
    cubes = equalise_all(cubes)
    cube_list = iris.cube.CubeList(equalise_all(cubes))
    cube = cube_list.concatenate_cube()
    return cube
