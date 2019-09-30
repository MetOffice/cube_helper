import iris
import iris.coord_categorisation
import six
from cube_helper.cube_loader import load_from_filelist, load_from_dir
from cube_helper.cube_equaliser import compare_cubes, examine_dim_bounds


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
            try:
                result = result.concatenate_cube()
            except iris.exceptions.ConcatenateError:
                print("Oops, there was an error in concatenation")
                examine_dim_bounds(result)
            return result

    elif isinstance(directory, list):
        loaded_cubes = load_from_filelist(
            directory, filetype, constraints)

        if not loaded_cubes:
            return "No cubes found".format()
        else:
            result = compare_cubes(loaded_cubes)
            result = iris.cube.CubeList(result)
            try:
                result = result.concatenate_cube()
            except iris.exceptions.ConcatenateError:
                print("Oops, there was an error in concatenation")
                examine_dim_bounds(result)
            return result
