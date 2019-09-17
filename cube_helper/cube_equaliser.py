import numpy as np
import cf_units
from datetime import datetime


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
            time_origin = time_origin.strip("days since ")
            time_origin = time_origin.strip(" 00:00:00")
            current_cube_date = datetime.strptime(time_origin, '%Y-%m-%d')
            return current_cube_date

def equalise_attributes(cubes):
    """
    Equalises Cubes for concatenation and merging, cycles through the cube_
    Dataset (CubeList) attribute and removes any that are not common across all cubes.
    metadata and variables.

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
    if data_type == 'float64':
        for cube in cubes:
            cube.data = np.float64(cube.data)
    if data_type == 'int32':
        for cube in cubes:
            cube.data = np.int32(cube.data)
    if data_type == 'int62':
        for cube in cubes:
            cube.data = np.int64(cube.data)


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
        for i in range(0, len(cube.dim_coords)-1):
            coord_name = cube.dim_coords[i].name()
            cube.dim_coords[i].standard_name = coord_name
            cube.dim_coords[i].long_name = coord_name
            cube.dim_coords[i].var_name = coord_name

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
