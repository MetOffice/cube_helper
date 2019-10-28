from __future__ import (absolute_import, division, print_function)
import sys
import iris
import numpy as np
import cf_units
from collections import namedtuple
import dateutil.parser
import re


def _sort_by_date(time_coord):
    time_origin = time_coord.units.origin
    time_origin = re.sub('[a-zA-Z]', '', time_origin)
    time_origin = time_origin.strip(' ')
    time_origin = time_origin.strip(" 00:00:00")
    time = dateutil.parser.parse(time_origin)
    time_origin = time.strftime('%Y-%m-%d')
    return time_origin

def _file_sort_by_earliest_date(cube_filename):
    """
    Sorts file names by date from earliest to latest.

    Args:
        cube_filename: list of files in string format to sort,
        to be used with CubeList sort method when cube_load is called.

    Returns:
        datetime object of selected Cubes start time.
    """

    if isinstance(iris.load_raw(cube_filename), iris.cube.CubeList):
        for cube in iris.load_raw(cube_filename):
            if isinstance(cube.standard_name, str):
                for time_coord in cube.coords():
                    if time_coord.units.is_time_reference():
                        time_origin = _sort_by_date(time_coord)
                        return time_origin
    else:
        for time_coord in iris.load_cube(cube_filename).coords():
            if time_coord.units.is_time_reference():
                time_origin = _sort_by_date(time_coord)
                return time_origin


def _sort_by_earliest_date(cube):
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


def equalise_attributes(cubes, comp_only=False):
    """
    Equalises Cubes for concatenation and merging, cycles through the
    iterable of cubes (either a list of loaded cubes or aan iris CubeList)
    and removes any that are not common across all cubes, metadata,
    and variables.

    Args:
        cubes: Cubes to be equalised of attributes.

        comp_only: A boolean value, if set to True it will examine
        the cubes attributes and print inconsistencies
        but not equalise them.

    Returns:
        Equalised cube_dataset to the CubeHelp class

    """
    uncommon_keys = []
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
                uncommon_keys.append(key)
                if not comp_only:
                    del cube.attributes[key]

    uncommon_keys = list(dict.fromkeys(uncommon_keys))
    for key in uncommon_keys:
        if not comp_only:
            print("Deleting {} attribute from cubes\n".format(key))
        else:
            print("\t{} attribute inconsistent\n".format(key))

    return cubes


def equalise_time_units(cubes, comp_only=False):
    """
    Equalises time units by cycling through each cube in the given CubeList
    or list of loaded cubes.

    Args:
        cubes: Cubes to equalised of time coords.

        comp_only: A boolean value, if set to True it will examine
        the cubes time_coordinates and print inconsistencies but not
        equalise them.

    Returns:
        cubes with time coordinates unified.
    """
    comp_messages = set({})
    epochs = {}
    calendar = None
    origin = None
    for cube in cubes:
        for time_coord in cube.coords():
            if time_coord.units.is_time_reference():
                if comp_only:
                    if not calendar:
                        calendar = time_coord.units.calendar
                        origin = time_coord.units.origin
                    if time_coord.units.calendar != calendar:
                        comp_messages.add("\tcalendar format inconsistent\n")
                    if time_coord.units.origin != origin:
                        comp_messages.add("\ttime start date inconsistent\n")
                    break
                else:
                    epoch = epochs.setdefault(time_coord.units.calendar,
                                              time_coord.units.origin)

                    new_unit = cf_units.Unit(epoch, time_coord.units.calendar)
                    time_coord.convert_units(new_unit)
                    calendar = time_coord.units.calendar
                    origin = time_coord.units.origin
    if comp_messages:
        for message in comp_messages:
            print(message)
    else:
        print("New time origin set to {}\n".format(origin))
        print("New time calender set to {}\n".format(calendar))
    return cubes


def equalise_data_type(cubes, data_type='float32'):
    """
    Casts datatypes in iris numpy array to be of the same datatype.

    Args:
        cubes: Cubes to have their datatypes equalised.
        data_type: String specifying datatype, default is float32.


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


def equalise_dim_coords(cubes, comp_only=False):
    """
    Equalises dimensional coordinates of Cubes, specifically long_name,
    standard_name, and var_name.

    Args:
        cubes: CubeList or list of Cubes to equalise.

        comp_only: A boolean value, if set to True it will examine
        the cubes dimension coordinates and print inconsistencies
        but not equalise them.

    Returns:
        Cubes equalised across dimension coordinates.
    """
    comp_messages = set({})
    for cube in cubes:
        for dim_coord in cube.dim_coords:
            if comp_only:
                coord = dim_coord.name()
                if dim_coord.standard_name != coord:
                    comp_messages.add("\t{} coords inconsistent\n".
                                      format(coord))
                if dim_coord.long_name != coord:
                    comp_messages.add("\t{} coords inconsistent\n".
                                      format(coord))
                if dim_coord.var_name != coord:
                    comp_messages.add("\t{} coords inconsistent\n".
                                      format(coord))
            else:
                coord = dim_coord.name()
                dim_coord.standard_name = coord
                dim_coord.long_name = coord
                dim_coord.var_name = coord

    if comp_messages:
        for message in comp_messages:
            print(message)
    return cubes


def equalise_aux_coords(cubes, comp_only=False):
    """
    Equalises auxillary coordinates of cubes.

    Args:
        cubes: CubeList or list of Cubes to equalise.

        comp_only: A boolean value, if set to True it will examine
        the Cube's aux coordinates and print inconsistencies
        but not equalise them.

    Returns:
        Cubes equalised across auxillary coordinates.
    """
    comp_messages = set({})
    for cube_a in cubes:
        for cube_b in cubes:
            if cube_a.coords() != cube_b.coords():
                cube_a_coords = {c.name() for c in cube_a.coords()}
                cube_b_coords = {c.name() for c in cube_b.coords()}
                common_coords = list(cube_a_coords.intersection(cube_b_coords))
                for coord in list(cube_a_coords):
                    if coord not in common_coords:
                        if comp_only:
                            comp_messages.add("\t{} coords inconsistent\n".
                                              format(coord))
                        else:
                            print("Removing {} coords from cube\n".
                                  format(coord))
                            cube_a.remove_coord(coord)
                for coord in list(cube_b_coords):
                    if coord not in common_coords:
                        if comp_only:
                            comp_messages.add("\t{} coords inconsistent\n".
                                              format(coord))
                        else:
                            print("Removing {} coords from cube\n".
                                  format(coord))
                            cube_b.remove_coord(coord)
    if comp_messages:
        for message in comp_messages:
            print(message)
    return cubes


def remove_attributes(cubes):
    """
    Sets all cube attributes to an empty string.
    be unaffected.

    Args:
        cubes: Cubes to have attributes stripped.

    Returns:
        Cubes with attributes replaced with empty string ''.
    """
    for cube in cubes:
        for attr in cube.attributes:
            cube.attributes[attr] = ''


def equalise_all(cubes):
    """
    Invokes equalise_aux_coords, equalise_attributes,
    equalise_dim_coords and equalise_time units all at once.
    Used before cube_load concatenates the cubes.

    Args:
        cubes: Cubes to be equalised.

    Returns:
        cubes: Cubes equalised across metadata and coords.


    """
    cubes = equalise_aux_coords(cubes)
    cubes = equalise_attributes(cubes)
    cubes = equalise_dim_coords(cubes)
    cubes = equalise_time_units(cubes)
    return cubes


def compare_cubes(cubes):
    """
    Examines coordinates and attributes across iterable of iris cubes
    And calls equalise functions (with comp_only arg set to true) where
    appropriate.

    Args:
        cubes: An iterable of iris Cubes or CubeList to be compared
        for inconsostencies.

    Returns:
        A printed string detailing the inconsistencies in the cubes.
    """
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

            if cube_a.aux_coords != cube_b.aux_coords:
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
        print("\ncube aux coordinates differ: \n")
        equalise_aux_coords(cubes, comp_only=True)

    if uneq_dim_coords:
        print("\ncube dim coordinates differ: \n")
        equalise_dim_coords(cubes, comp_only=True)

    if uneq_attr:
        print("cube attributes differ: \n")
        equalise_attributes(cubes, comp_only=True)

    if uneq_time_coords:
        print("cube time coordinates differ: \n")
        equalise_time_units(cubes, comp_only=True)


def examine_dim_bounds(cubes, cube_files):
    """
    Examines the dimensional bounds of time should concatenate fail.
    Cycles through cubes and determines if the times are contiguous.

    Args:
         cubes: Iris cubes to examine the time bounds of
         cube_files: the respective files of cubes, to give users
         info as to what cubes are causing problems with concatentation.

    Returns:
        A printed string detailing any overlap in the time bounds.
    """
    Range = namedtuple('Range', ['start', 'end'])
    for i, cube_a in enumerate(cubes):
        for j, cube_b in enumerate(cubes):
            if i != j:
                range_a = Range(start=cube_a.coord('time').bounds[0][0],
                                end=cube_a.coord('time').bounds[-1][-1])
                range_b = Range(start=cube_b.coord('time').bounds[0][0],
                                end=cube_b.coord('time').bounds[-1][-1])
                latest_start = max(range_a.start, range_b.start)
                earliest_end = min(range_a.end, range_b.end)
                delta = earliest_end - latest_start
                overlap = max(0, delta)
                if overlap > 0:
                    print("\nThe time coordinates overlap at cube {}"
                          " and cube {}".format(i, j))
                    print("\nThese cubes are: \n\t{}\n\t{}".
                          format(cube_files[i], cube_files[j]))
                    break
