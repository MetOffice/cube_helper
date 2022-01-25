# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

import os
import glob
from datetime import datetime

import iris
import iris.cube
from iris.exceptions import MergeError, ConstraintMismatchError
import iris.time
from six import string_types


def _check_pdt_year(cell, partial_datetime):
    if partial_datetime.year:
        return partial_datetime.year
    else:
        return cell.point.year


def _check_pdt_month(cell, partial_datetime):
    if partial_datetime.month:
        return partial_datetime.month
    else:
        return cell.point.month


def _check_pdt_day(cell, partial_datetime):
    if partial_datetime.day:
        return partial_datetime.day
    else:
        return cell.point.day


def _check_pdt_hour(cell, partial_datetime):
    if partial_datetime.hour:
        return partial_datetime.hour
    else:
        return cell.point.hour


def _check_pdt_minute(cell, partial_datetime):
    if partial_datetime.minute:
        return partial_datetime.minute
    else:
        return cell.point.minute


def _check_pdt_second(cell, partial_datetime):
    if partial_datetime.second:
        return partial_datetime.second
    else:
        return cell.point.second


def _check_pdt_microsecond(cell, partial_datetime):
    if partial_datetime.microsecond:
        return partial_datetime.microsecond
    else:
        return cell.point.microsecond


def _fix_partial_datetime(constraint):
    if isinstance(constraint._coord_values['time'], iris.time.PartialDateTime):
        part_datetime = constraint._coord_values['time']
        new_constraint = iris.Constraint(
            time=lambda cell:
            cell.point.year == _check_pdt_year(cell, part_datetime) and
            cell.point.month == _check_pdt_month(cell, part_datetime) and
            cell.point.day == _check_pdt_day(cell, part_datetime) and
            cell.point.hour == _check_pdt_hour(cell, part_datetime) and
            cell.point.minute == _check_pdt_minute(cell, part_datetime) and
            cell.point.second == _check_pdt_second(cell, part_datetime) and
            cell.point.microsecond ==
            _check_pdt_microsecond(cell, part_datetime))
        return new_constraint
    else:
        return constraint


def _constraint_compatible(constraint, cube):
    try:
        cube.extract(constraint)
        return True
    except (TypeError, ConstraintMismatchError):
        return False


def _parse_directory(directory):
    """
    Parses the string representing the directory, makes sure a '/'
    backspace is present at the start and end of the directory string
    so glob can work properly.

    Args:
         directory: the directory string to parse.

    Returns:
        a string representing the directory, having been parsed if
        needed.
    """
    if not directory.endswith('/'):
        directory = directory + '/'

    if not directory.startswith('/'):
        if os.path.isdir(directory):
            return directory

        else:
            directory = '/' + directory
            return directory
    else:
        return directory


def _sort_by_date(time_coord):
    """
    Private sorting function used by _file
    _sort_by_earliest_date() and sort_by_earliest_date().

    Args:
        time_coord: Cube time coordinate for each cube
        to be sorted by.

    Returns:
        time_origin: The time origin to sort cubes
        by, as a specific start date e.g 1850.
    """
    time_origin = time_coord.units.num2date(0)
    if not isinstance(time_origin, datetime):
        if time_origin.datetime_compatible:
            time_origin = time_origin._to_real_datetime()
        else:
            time_origin = datetime(time_origin.year,
                                   time_origin.month,
                                   time_origin.day)
    return time_origin


def file_sort_by_earliest_date(cube_filename):
    """
    Sorts file names by date from earliest to latest.

    Args:
        cube_filename: list of files in string format to sort,
        to be used with CubeList sort method when cube_load is called.

    Returns:
        datetime object of selected Cubes start time.
    """
    raw_cubes = iris.load_raw(cube_filename)
    if isinstance(raw_cubes, iris.cube.CubeList):
        for cube in raw_cubes:
            if isinstance(cube.standard_name, string_types):
                for time_coord in cube.coords():
                    if time_coord.units.is_time_reference():
                        time_origin = _sort_by_date(time_coord)
                        return time_origin
    else:
        for time_coord in iris.load_cube(cube_filename).coords():
            if time_coord.units.is_time_reference():
                time_origin = _sort_by_date(time_coord)
                return time_origin


def sort_by_earliest_date(cube):
    """
    Sorts Cubes by date from earliest to latest.

    Args:
        cube: CubeList or list to sort, to be used with CubeList
        sort method when cube_load is called.

    Returns:
        datetime object of selected Cubes start time.
    """

    for time_coord in cube.coords():
        if time_coord.units.is_time_reference():
            time_origin = _sort_by_date(time_coord)
            return time_origin


def load_from_dir(directory, filetype, constraint=None):
    """
    Loads a set of cubes from a given directory, single cubes are loaded
    and returned as a CubeList.

    Args:
        directory: a chosen directory
        to operate on. directory MUST start and end with forward
        slashes.

        filetype (optional): a string specifying the expected type
        Of files found in the dataset.

        constraint (optional): a string specifying any constraints
        You wish to load the dataset with.

    Returns:
        iris.cube.CubeList(loaded_cubes), a CubeList of the loaded
        Cubes.
    """
    if constraint is None:
        loaded_cubes = []
        cube_files = []
        directory = _parse_directory(directory)
        cube_paths = glob.glob(directory + '*' + filetype)
        for path in cube_paths:
            try:
                loaded_cubes.append(iris.load_cube(path))
                cube_files.append(path)
            except (MergeError, ConstraintMismatchError):
                for cube in iris.load_raw(path):
                    if isinstance(cube.standard_name, str):
                        loaded_cubes.append(cube)
                        cube_files.append(path)
        loaded_cubes.sort(key=sort_by_earliest_date)
        cube_files.sort(key=file_sort_by_earliest_date)
        return loaded_cubes, cube_files
    else:
        loaded_cubes = []
        cube_files = []
        directory = _parse_directory(directory)
        cube_paths = glob.glob(directory + '*' + filetype)
        if not _constraint_compatible(constraint,
                                      iris.load_cube(cube_paths[0])):
            constraint = _fix_partial_datetime(constraint)
        for path in cube_paths:
            try:
                loaded_cubes.append(iris.load_cube(path, constraint))
                cube_files.append(path)
            except (MergeError, ConstraintMismatchError):
                for cube in iris.load_raw(path, constraint):
                    if isinstance(cube.standard_name, str):
                        loaded_cubes.append(cube)
                        cube_files.append(path)
        loaded_cubes.sort(key=sort_by_earliest_date)
        cube_files.sort(key=file_sort_by_earliest_date)
        return loaded_cubes, cube_files


def load_from_filelist(paths, filetype, constraint=None):
    """
    Loads the specified files. Individual files are
    returned in a
    CubeList.

    Args:
        paths: a chosen list of filenames to operate on.

        filetype (optional): a string specifying the expected type
        Of files found in the dataset

        constraint (optional): a string, iterable of strings or an
        iris.Constraint specifying any constraints you wish to load
        the dataset with.

    Returns:
        iris.cube.CubeList(loaded_cubes), a CubeList of the loaded
        Cubes.
    """
    loaded_cubes = []
    cube_files = []
    for filename in paths:
        if not filename.endswith(filetype):
            paths.remove(filename)

    for filename in paths:
        if constraint is None:
            try:
                loaded_cubes.append(iris.load_cube(filename))
                cube_files.append(filename)
            except (MergeError, ConstraintMismatchError):
                for cube in iris.load_raw(filename):
                    if isinstance(cube.standard_name, str):
                        loaded_cubes.append(cube)
                        cube_files.append(filename)

        else:
            if not _constraint_compatible(constraint,
                                          iris.load_cube(paths[0])):
                constraint = _fix_partial_datetime(constraint)
            try:
                loaded_cubes.append(iris.load_cube(filename, constraint))
                cube_files.append(filename)
            except (MergeError, ConstraintMismatchError):
                for cube in iris.load_raw(filename, constraint):
                    if isinstance(cube.standard_name, str):
                        loaded_cubes.append(iris.load_raw(filename,
                                                          constraint))
                        cube_files.append(filename)
    loaded_cubes.sort(key=sort_by_earliest_date)
    cube_files.sort(key=file_sort_by_earliest_date)
    return loaded_cubes, cube_files
