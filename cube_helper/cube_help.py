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


def _season_year(cube, coord):
    iris.coord_categorisation.add_season_year(
        cube,
        coord,
        name='season_year')


def _season_membership(cube, coord, season):
    iris.coord_categorisation.add_season_membership(
        cube,
        coord,
        name='season_membership',
        season=season)


def _season_number(cube, coord, seasons):
    iris.coord_categorisation.add_season_number(
        cube,
        coord,
        name='season_number',
        seasons=seasons)


def _clim_season(cube, coord, seasons):
    iris.coord_categorisation.add_season(
        cube,
        coord,
        name='season',
        seasons=seasons)


def _year(cube, coord):
    iris.coord_categorisation.add_year(
        cube,
        coord,
        name='year')


def _month_number(cube, coord):
    iris.coord_categorisation.add_month_number(
        cube,
        coord,
        name='month_number')


def _month_fullname(cube, coord):
    iris.coord_categorisation.add_month_fullname(
        cube,
        coord,
        name='month_fullname')


def _month(cube, coord):
    iris.coord_categorisation.add_month(
        cube,
        coord,
        name='month')


def _day_of_month(cube, coord):
    iris.coord_categorisation.add_day_of_month(
        cube,
        coord,
        name='day_of_month')


def _day_of_year(cube, coord):

    iris.coord_categorisation.add_day_of_year(
        cube,
        coord,
        name='day_of_year')


def _weekday_number(cube, coord):
    iris.coord_categorisation.add_weekday_number(
        cube,
        coord,
        name='weekday_number')


def _weekday_fullname(cube, coord):
    iris.coord_categorisation.add_weekday_fullname(
        cube,
        coord,
        name='weekday_fullname')


def _weekday(cube, coord):
    iris.coord_categorisation.add_weekday(
        cube,
        coord,
        name='weekday')


def _hour(cube, coord):
    iris.coord_categorisation.add_hour(
        cube,
        coord,
        name='hour')


def _add_categorical(cater_name, cube, coord, season, seasons):
    cater_dict = {'season_year':
                      lambda cube:
                      _season_year(cube, coord),
                  'season_membership':
                      lambda cube:
                      _season_membership(cube, coord, season),
                  'season_number':
                      lambda cube:
                      _season_number(cube, coord, seasons),
                  'number':
                      lambda cube:
                      _season_number(cube, coord, seasons),
                  'clim_season':
                      lambda cube:
                      _clim_season(cube, coord, seasons),
                  'season':
                      lambda cube:
                      _clim_season(cube, coord, seasons),
                  'year':
                      lambda cube:
                      _year(cube, coord),
                  'month_number':
                      lambda cube:
                      _month_number(cube, coord),
                  'month_fullname':
                      lambda cube:
                      _month_fullname(cube, coord),
                  'month':
                      lambda cube:
                      _month(cube, coord),
                  'day_of_month':
                      lambda cube:
                      _day_of_month(cube, coord),
                  'day_of_year':
                      lambda cube:
                      _day_of_year(cube, coord),
                  'weekday_number':
                      lambda cube:
                      _weekday_number(cube, coord),
                  'weekday_fullname':
                      lambda cube:
                      _weekday_fullname(cube, coord),
                  'weekday':
                      lambda cube:
                      _weekday(cube, coord),
                  'hour':
                      lambda cube:
                      _hour(cube, coord)}

    cater_dict.get(cater_name)(cube)


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
            _add_categorical(cater_name, cube, coord, season, seasons)
        return cubes

    else:
        _add_categorical(cater_name, cubes, coord, season, seasons)
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
