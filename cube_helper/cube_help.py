import iris
import iris.coord_categorisation
import six
from cube_helper.cube_loader import load_from_filelist, load_from_dir
from cube_helper.cube_equaliser import (equalise_time_units,
                                        equalise_attributes,
                                        equalise_dim_coords,
                                        equalise_aux_coords, compare_cubes)


def cube_loader(directory, filetype='.nc', constraints=None):

    directory = directory
    filetype = filetype
    constraints = constraints
    if isinstance(directory, six.string_types):
        loaded_cubes = load_from_dir(
            directory, filetype, constraints)
        if not loaded_cubes:
            return "No cubes found".format()
        else:
            result = compare_cubes(loaded_cubes)
            result = iris.cube.CubeList(result)
            result = result.concatenate_cube()
            return result

    elif isinstance(directory, list):
        loaded_cubes = load_from_filelist(
            directory, filetype, constraints)

        if not loaded_cubes:
            return "No cubes found".format()
        else:
            result = compare_cubes(loaded_cubes)
            result = iris.cube.CubeList(result)
            result = result.concatenate_cube()
            return result
