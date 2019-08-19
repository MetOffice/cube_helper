import numpy as np
import cf_units


def equalise_attributes(cubes):
    """
    Equalises cubes for concatenation and merging, cycles through the cube_
    Dataset (CubeList) attribute and removes any that are not common across all cubes.
    metadata and variables.

    Args:
        cubes: Cubes to be equalised of attributes

    Returns:
        Equalised cube_dataset to the CubeHelp class
    """
    uncommon_keys = []
    common_keys = list(cubes[0].attributes.keys())
    for cube in cubes[1:]:
        cube_keys = list(cube.attributes.keys())
        common_keys = [
            key for key in common_keys
            if (key in cube_keys and
                cube.attributes[key] == cubes[0].attributes[key])]

    for cube in cubes:
        for key in cube.attributes.keys():
            if key not in common_keys:
                uncommon_keys.append(cube.attributes[key])
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


def remove_attributes(cubes):
    """
    Sets all cube attributes to an empty string.
    be unaffected.

    Args:
        cubes: Cubes to have attributes stripped.

    Returns:
        cubes with attributes replaced with empty string ''
    """
    for cube in cubes:
        for attr in cube.attributes:
            cube.attributes[attr] = ''


def equalise_data_type(cubes):
    """
    Casts datatypes in iris numpy array to be of the same datatype.

    Args:
        cubes: Cubes to have their datatypes equalised.

    Returns:
        cubes: Cubes with their data types identical.
    """
    for cube in cubes:
        cube.data = np.float32(cube.data)
