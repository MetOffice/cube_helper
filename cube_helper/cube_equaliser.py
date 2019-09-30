from __future__ import (absolute_import, division, print_function)
import sys
import numpy as np
import cf_units
from datetime import datetime
from collections import namedtuple


import re


def _sort_by_earliest_date(cube):
    """
    Sorts Cubes by date from earliest to latest.

    Args:
        cube: CubeList or list to sort, to be used with CubeList
                sort method on instantiation of CubeHelp object.

    Returns:
        datetime object of selected cubes start time.
    """

    for time_coord in cube.coords():
        if time_coord.units.is_time_reference():
            time_origin = time_coord.units.origin
            time_origin = re.sub('[a-zA-Z]', '', time_origin)
            time_origin = time_origin.strip(' ')
            time_origin = time_origin.strip(" 00:00:00")
            current_cube_date = datetime.strptime(time_origin, '%Y-%m-%d')
            return current_cube_date


def equalise_attributes(cubes):
    """
    Equalises Cubes for concatenation and merging, cycles through the cube_
    Dataset (CubeList) attribute and removes any that are not common across
    all cubes, metadata, and variables.

    Args:
        cubes: Cubes to be equalised of attributes

    Returns:
        Equalised cube_dataset to the CubeHelp class

    """
    common_keys = cubes[0].attributes.keys()
    for cube in cubes[1:]:
        cube_keys = cube.attributes.keys()
        common_keys = [
            key for key in common_keys
            if (key in cube_keys and
                np.all(cube.attributes[key] == cubes[0].attributes[key]))]

    # Remove all the other attributes.
    for cube in cubes:
        for key in list(cube.attributes.keys()):
            if key not in common_keys:
                del cube.attributes[key]
    return cubes

def equalise_time_units(cubes):
    """
    Equalises time units by cycling through each cube in the given CubeList.

    Args:
        cubes: Cubes to equalised of time coords.

    Returns:
        cubes with time coordinates unified.
    """
    epochs = {}
    for cube in cubes:
        for time_coord in cube.coords():
            if time_coord.units.is_time_reference():
                epoch = epochs.setdefault(time_coord.units.calendar,
                                          time_coord.units.origin)

                new_unit = cf_units.Unit(epoch, time_coord.units.calendar)
                time_coord.convert_units(new_unit)
    return cubes

def equalise_data_type(cubes, data_type='float32'):
    """
    Casts datatypes in iris numpy array to be of the same datatype.

    Args:
        cubes: Cubes to have their datatypes equalised.
        data_type: String specifying datatype, default is float32

    Returns:
        cubes: Cubes with their data types identical.
    """
    if data_type == 'float32':
        for cube in cubes:
            cube.data = np.float32(cube.data)
    elif data_type == 'float64':
        for cube in cubes:
            cube.data = np.float64(cube.data)
    elif data_type == 'int32':
        for cube in cubes:
            cube.data = np.int32(cube.data)
    elif data_type == 'int64':
        for cube in cubes:
            cube.data = np.int64(cube.data)
    else:
        print("invalid data type")


def equalise_dim_coords(cubes):
    """
    Equalises dimensional coordinates of cubes, specifically long_name,
    standard_name, and var_name.

    Args:
        cubes: CubeList or list of cubes to equalise.

    Returns:
        Cubes equalised across `dim_coord.
    """
    for cube in cubes:
        for dim_coord in cube.dim_coords:
            coord_name = dim_coord.name()
            dim_coord.standard_name = coord_name
            dim_coord.long_name = coord_name
            dim_coord.var_name = coord_name

    return cubes

def equalise_aux_coords(cubes):
    """
    Equalises auxillary coordinates of cubes.

    Args:
        cubes: CubeList or list of cubes to equalise.

    Returns:
        Cubes equalised across auxillary coordinates.
    """
    for cube_a in cubes:
        for cube_b in cubes:
            if cube_a.coords() != cube_b.coords():
                cube_a_coords = {c.name() for c in cube_a.coords()}
                cube_b_coords = {c.name() for c in cube_b.coords()}
                common_coords = list(cube_a_coords.intersection(cube_b_coords))
                for coord in list(cube_a_coords):
                    if coord not in common_coords:
                        cube_a.remove_coord(coord)
                for coord in list(cube_b_coords):
                    if coord not in common_coords:
                        cube_b.remove_coord(coord)
    return cubes

def remove_attributes(cubes):
    """
    Sets all cube attributes to an empty string.
    be unaffected.

    Args:
        cubes: Cubes to have attributes stripped.

    Returns:
        cubes with attributes replaced with empty string ''.
    """
    for cube in cubes:
        for attr in cube.attributes:
            cube.attributes[attr] = ''

def compare_cubes(cubes):

    uneq_aux_coords = False
    uneq_dim_coords = False
    uneq_attr = False
    uneq_time_coords = False
    uneq_ndim = False
    for cube_a in cubes:
        for cube_b in cubes:
            if (uneq_aux_coords and
                    uneq_attr and
                    uneq_dim_coords and
                    uneq_time_coords and
                    uneq_ndim):
                break

            if cube_a.coords() != cube_b.coords():
                uneq_aux_coords = True


            if cube_a.dim_coords != cube_b.dim_coords:
                uneq_dim_coords = True

            if cube_a.attributes != cube_b.attributes:
                uneq_attr = True

            if cube_a.ndim != cube_b.ndim:
                uneq_ndim = True
                break

            for time_coord_a in cube_a.coords():
                for time_coord_b in cube_b.coords():
                    if (time_coord_a.units.is_time_reference()
                            and time_coord_b.units.is_time_reference()):
                        if time_coord_a.units != time_coord_b.units:
                            uneq_time_coords = True
                            break


    if uneq_ndim:
        print("\n Number of dimensions for cubes differ,"
              "please load cubes of matching ndim")
        sys.exit(2)

    if uneq_aux_coords:
        print("\ncube aux coordinates differ,"
              " equalising...\n")
        equalise_aux_coords(cubes)

    if uneq_dim_coords:
        print("cube dimensional coordinates differ,"
              " equalising...\n")
        equalise_dim_coords(cubes)

    if uneq_attr:
        print("cube attributes differ,"
              " equalising...\n")
        equalise_attributes(cubes)

    if uneq_time_coords:
        print("cube time coordinates differ,"
              "equalising...\n")
        equalise_time_units(cubes)

    return cubes

def examine_dim_bounds(cubes):
    Range = namedtuple('Range', ['start', 'end'])
    for i, cube_a in enumerate(cubes):
        for j, cube_b in enumerate(cubes):
            if i != j:
                range_a = Range(start=cube_a.coord('time').bounds[0][0], end=cube_a.coord('time').bounds[-1][-1])
                range_b = Range(start=cube_b.coord('time').bounds[0][0], end=cube_b.coord('time').bounds[-1][-1])
                latest_start = max(range_a.start, range_b.start)
                earliest_end = min(range_a.end, range_b.end)
                delta = earliest_end - latest_start
                overlap = max(0, delta)
                if overlap > 0:
                    print("The time coordinates overlap at cube {} and cube {}".format(i, j))
                    print(overlap)
                    break

    return cubes