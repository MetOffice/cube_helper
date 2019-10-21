import os
import iris
import glob
from iris.exceptions import MergeError, ConstraintMismatchError
from cube_helper.cube_equaliser import (_sort_by_earliest_date,
                                        _file_sort_by_earliest_date)


def _parse_directory(directory):
    """
    Parses the string representing the directory, makes sure a '/'
    backspace is present at the start and end of the directory string
    so glob can work properly.

    Args:
         directory: the directory string to parse.

    Returns:
        a string representing the directory, having been parsed if
        cd docneeded.
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

        constraints (optional): a string specifying any constraints
        You wish to load the dataset with.

    Returns:
        iris.cube.CubeList(loaded_cubes), a CubeList of the loaded
        Cubes.
    """
    if constraint is None:
        loaded_cubes = []
        cube_files = []
        directory = _parse_directory(directory)
        for path in glob.glob(directory + '*' + filetype):
            try:
                loaded_cubes.append(iris.load_cube(path))
                cube_files.append(path)
            except (MergeError, ConstraintMismatchError):
                for cube in iris.load_raw(path):
                    if isinstance(cube.standard_name, str):
                        loaded_cubes.append(cube)
                        cube_files.append(path)
        loaded_cubes.sort(key=_sort_by_earliest_date)
        cube_files.sort(key=_file_sort_by_earliest_date)
        return loaded_cubes, cube_files
    else:
        loaded_cubes = []
        cube_files = []
        directory = _parse_directory(directory)
        for path in glob.glob(directory + '*' + filetype):
            try:
                loaded_cubes.append(iris.load_cube(path, constraint))
                cube_files.append(path)
            except (MergeError, ConstraintMismatchError):
                for cube in iris.load_raw(path, constraint):
                    if isinstance(cube.standard_name, str):
                        loaded_cubes.append(cube)
                        cube_files.append(path)
        loaded_cubes.sort(key=_sort_by_earliest_date)
        cube_files.sort(key=_file_sort_by_earliest_date)
        return loaded_cubes, cube_files


def load_from_filelist(data_filelist, filetype, constraint=None):
    """
    Loads the specified files. Individual files are
    returned in a
    CubeList.

    Args:
        data_filelist: a chosen list of filenames to operate on.

        filetype (optional): a string specifying the expected type
        Of files found in the dataset

        constraints (optional): a string, iterable of strings or an
        iris.Constraint specifying any constraints you wish to load
        the dataset with.

    Returns:
        iris.cube.CubeList(loaded_cubes), a CubeList of the loaded
        Cubes.
    """
    loaded_cubes = []
    cube_files = []
    for filename in data_filelist:
        if not filename.endswith(filetype):
            data_filelist.remove(filename)

    for filename in data_filelist:
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
            try:
                loaded_cubes.append(iris.load_cube(filename, constraint))
            except (MergeError, ConstraintMismatchError):
                for cube in iris.load_raw(filename, constraint):
                    if isinstance(cube.standard_name, str):
                        loaded_cubes.append(iris.load_raw(filename,
                                                          constraint))
                        cube_files.append(filename)
    loaded_cubes.sort(key=_sort_by_earliest_date)
    cube_files.sort(key=_file_sort_by_earliest_date)
    return loaded_cubes, cube_files
