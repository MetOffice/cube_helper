# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
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


def _season_year(**kwargs):
    iris.coord_categorisation.add_season_year(
        kwargs.get('cube'),
        kwargs.get('coord'),
        name='season_year')


def _season_membership(**kwargs):
    iris.coord_categorisation.add_season_membership(
        kwargs.get('cube'),
        kwargs.get('coord'),
        name='season_membership',
        season=kwargs.get('season'))


def _season_number(**kwargs):
    iris.coord_categorisation.add_season_number(
        kwargs.get('cube'),
        kwargs.get('coord'),
        name='season_number',
        seasons=kwargs.get('seasons'))


def _season(**kwargs):
    iris.coord_categorisation.add_season(
        kwargs.get('cube'),
        kwargs.get('coord'),
        name='season',
        seasons=kwargs.get('seasons'))


def _clim_season(**kwargs):
    iris.coord_categorisation.add_season(
        kwargs.get('cube'),
        kwargs.get('coord'),
        name='clim_season',
        seasons=kwargs.get('seasons'))


def _year(**kwargs):
    iris.coord_categorisation.add_year(
        kwargs.get('cube'),
        kwargs.get('coord'),
        name='year')


def _month_number(**kwargs):
    iris.coord_categorisation.add_month_number(
        kwargs.get('cube'),
        kwargs.get('coord'),
        name='month_number')


def _month_fullname(**kwargs):
    iris.coord_categorisation.add_month_fullname(
        kwargs.get('cube'),
        kwargs.get('coord'),
        name='month_fullname')


def _month(**kwargs):
    iris.coord_categorisation.add_month(
        kwargs.get('cube'),
        kwargs.get('coord'),
        name='month')


def _day_of_month(**kwargs):
    iris.coord_categorisation.add_day_of_month(
        kwargs.get('cube'),
        kwargs.get('coord'),
        name='day_of_month')


def _day_of_year(**kwargs):

    iris.coord_categorisation.add_day_of_year(
        kwargs.get('cube'),
        kwargs.get('coord'),
        name='day_of_year')


def _weekday_number(**kwargs):
    iris.coord_categorisation.add_weekday_number(
        kwargs.get('cube'),
        kwargs.get('coord'),
        name='weekday_number')


def _weekday_fullname(**kwargs):
    iris.coord_categorisation.add_weekday_fullname(
        kwargs.get('cube'),
        kwargs.get('coord'),
        name='weekday_fullname')


def _weekday(**kwargs):
    iris.coord_categorisation.add_weekday(
        kwargs.get('cube'),
        kwargs.get('coord'),
        name='weekday')


def _hour(**kwargs):
    iris.coord_categorisation.add_hour(
        kwargs.get('cube'),
        kwargs.get('coord'),
        name='hour')


def _annual_seasonal_mean(**kwargs):
    _clim_season(**kwargs)
    _season_year(**kwargs)


def _add_categorical(cube, categorical, coord, season, seasons):
    categorical_dict = {'season_year': _season_year,
                        'season_membership': _season_membership,
                        'season_number': _season_number,
                        'annual_seasonal_mean': _annual_seasonal_mean,
                        'number': _season_number,
                        'clim_season': _clim_season,
                        'season': _season,
                        'year': _year,
                        'month_number': _month_number,
                        'month_fullname': _month_fullname,
                        'month': _month,
                        'day_of_month': _day_of_month,
                        'day_of_year': _day_of_year,
                        'weekday_number': _weekday_number,
                        'weekday_fullname': _weekday_fullname,
                        'weekday': _weekday,
                        'hour': _hour
                        }

    categorical_dict.get(categorical)(cube=cube,
                                      cater_name=categorical,
                                      coord=coord,
                                      season=season,
                                      seasons=seasons)


def add_categorical(cubes, categorical, coord='time', season='djf',
                    seasons=('djf', 'mam', 'jja', 'son')):
    """
    Adds a coordinate categorisation(s) to the iterable of Iris Cubes.

    Currently this function provides a wrapper for the following
    standalone and compound categoricals:

    day_of_month:
        Add a day-of-month coordinate, vals 1-31.
    day_of_year:
        Add a day-of-year coordinate, vals 1-365 (366 in leap years).
    month:
        Add a month coordinate, vals ‘Jan’-’Dec’.
    month_fullname:
        Add a month coordinate, vals ‘January’-’December’.
    month_number:
        Add a month coordinate, vals 1-12.
    season:
        Add a season-of-year coordinate, with specified seasons.
    clim_season:
        Add a climatalogical season-of-year coordinate, with
        specified seasons.
    season_membership:
        Add a season membership coordinate for a specified season.
    season_number:
        Add a season-of-year coordinate, values 0..(N-1)
        where N is the number of user specified seasons.
    season_year:
        Add a categorical year-of-season coordinate, with specified seasons.
    weekday:
        Add a weekday coordinate, vals ‘Mon’-’Sun’.
    weekday_fullname:
        Add a weekday coordinate, vals ‘Monday’-’Sunday’.
    weekday_number:
        Add a weekday coordinate, vals 0-6 [0=Monday].
    year:
        Add a calendar-year coordinate.
    annual_seasonal_mean:
        Add a clim_season and a season_year coordinate.

    Args:
        cubes: A cube, a list of Loaded Cubes or a CubeList.

        categorical: A string or list of strings specifying
        the categorisation you wish to add. Additionally a compound
        categorisation can be added. E.g 'annual_seasonal_mean'.

        coords: the coordinate you wish to add a categorisation to. Set
        to 'time' by default.

        season: The season you need for the categorisation (where required).
        set to 'djf' by default.

        seasons: The seasons required for categorisation.

    Returns:
        cubes: An iterable of Cubes, either a list of loaded Cubes
        or an iris CubeList.
    """
    if isinstance(categorical, list):
        for categorical in categorical:

            if isinstance(cubes, list) or isinstance(cubes,
                                                     iris.cube.CubeList):
                for cube in cubes:
                    _add_categorical(cube, categorical, coord, season, seasons)
            else:
                _add_categorical(cubes, categorical, coord, season, seasons)
        return cubes
    else:
        if isinstance(cubes, list) or isinstance(cubes, iris.cube.CubeList):
            for cube in cubes:
                _add_categorical(cube, categorical, coord, season, seasons)
            return cubes

        else:
            _add_categorical(cubes, categorical, coord, season, seasons)
            return cubes


def aggregate_categorical(cube, categorical,
                          coord='time', season='djf',
                          seasons=('djf', 'mam', 'jja', 'son'),
                          agg_method=iris.analysis.MEAN):
    """
    Adds a coordinate categorisation(s) to the iterable of iris Cubes, then
    aggregates them by the given categoricals. Categoricals used are the
    same as the ones suppourted by add_categorical().

    Args:
        cubes: A cube, a list of loaded Cubes or a CubeList.

        categorical: A string or list of strings specifying
        the categorisation you wish to add. Additionally a compound
        categorisation can be added. E.g 'annual_seasonal_mean'.

        coords: the coordinate you wish to add a categoisation to. Set
        to 'time' by default.

        season: The season you need for the categorisation (where required).
        set to 'djf' by default.

        seasons: The seasons required for categorisation.

    Returns:
        cubes: A cube, a list of loaded Cubes, or an iris CubeList
        aggregated by a given categorical.
    """
    compound_dict = {'annual_seasonal_mean': ['clim_season',
                                              'season_year']}
    cube = add_categorical(cube, categorical, coord=coord, season=season,
                           seasons=seasons)
    try:
        categorical = compound_dict[categorical]
        cube = cube.aggregated_by(categorical, agg_method)
        return cube
    except KeyError:
        cube = cube.aggregated_by(categorical, agg_method)
        return cube


def extract_categorical(cube,
                        categorical,
                        constraint,
                        coord='time',
                        season='djf',
                        seasons=('djf', 'mam', 'jja', 'son')):
    """
    Adds a coordinate categorical, aggregates by said categorical,
    then extracts the given contraint. Categoricals used are the
    same as the ones suppourted by add_categorical() and
    aggregate_categorical().

    Args:
        cubes: A cube, a list of Loaded Cubes or a CubeList.

        categorical: A string or list of strings specifying
        the categorisation you wish to add. Additionally a compound
        categorisation can be added. E.g 'annual_seasonal_mean'.

        constraint: an iris constraint you wish to extract.

        coords: the coordinate you wish to add a categoisation to. Set
        to 'time' by default.

        season: The season you need for the categorisation (where required).
        set to 'djf' by default.
        
        seasons: The seasons required for categorisation.

    Returns:
        cubes: A cube, a list of loaded Cubes, or an iris CubeList
        extracted from a given constraint.
    """
    if not isinstance(constraint, iris.Constraint):
        raise NameError("No constraint given")

    else:
        cube = aggregate_categorical(cube,
                                     categorical,
                                     coord=coord,
                                     season=season,
                                     seasons=seasons)
        return cube.extract(constraint)


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
