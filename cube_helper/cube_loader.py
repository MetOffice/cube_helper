import os
import iris

def load_from_dir(directory, constraint=None, filetype='.nc'):
    """
    Loads a set of cubes from a given directory, single cubes are loaded
    and returned as a CubeList.

    Args:
        directory: a chosen directory
        to operate on.

        filetype (optional): a string specifying the expected type
        Of files found in the dataset

        constraints (optional): a string specifying any constraints
        You wish to load the dataset with.

    Returns:
        iris.cube.CubeList(loaded_cubes), a CubeList of the loaded
        Cubes.
    """
    if constraint is None:
        loaded_cubes = []
        for path in os.listdir(directory):
            full_path = os.path.join(directory, path)
            if os.path.isfile(full_path):
                if full_path.endswith(filetype):
                    try:
                        loaded_cubes.append(iris.load_cube(full_path))
                    except:
                        for cube in iris.load_raw(full_path):
                            if cube.ndim >= 2:
                                loaded_cubes.append(cube)

        return iris.cube.CubeList(loaded_cubes)
    else:
        loaded_cubes = []
        for path in os.listdir(directory):
            full_path = os.path.join(directory, path)
            if os.path.isfile(full_path):
                if full_path.endswith(filetype):
                    try:
                        loaded_cubes.append(iris.load_cube(full_path, constraint))
                    except:
                        for cube in iris.load_raw(full_path, constraint):
                            if cube.ndim >= 2:
                                loaded_cubes.append(cube)
        return iris.cube.CubeList(loaded_cubes)


def load_from_filelist(data_filelist, constraint=None,
                       filetype='.nc'):
    """
    Loads the specified files. Individual files are
    returned in a
    CubeList.

    Args:
        data_filelist: a chosen list of filenames to operate on.

        filetype (optional): a string specifying the expected type
        Of files found in the dataset

        constraints (optional): a string, iterable of strings or an iris.Constraint specifying any constraints
        You wish to load the dataset with.

    Returns:
        iris.cube.CubeList(loaded_cubes), a CubeList of the loaded
        Cubes.
    """
    loaded_cubes = []
    for filename in data_filelist:
        if not filename.endswith(filetype):
            data_filelist.remove(filename)

    for filename in data_filelist:
        if constraint is None:
            try:
                loaded_cubes.append(iris.load_cube(filename))
            except:
                loaded_cubes.append(iris.load_raw(filename).pop(3))

        else:
            try:
                loaded_cubes.append(iris.load_cube(filename, constraint))
            except:
                loaded_cubes.append(iris.load_raw(filename, constraint).pop(3))

    return iris.cube.CubeList(loaded_cubes)
