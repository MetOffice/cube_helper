import iris
import iris.coord_categorisation
import six
from cube_helper.cube_loader import load_from_filelist, load_from_dir
from cube_helper.cube_equaliser import compare_cubes, examine_dim_bounds


def cube_load(directory, filetype='.nc', constraints=None):

    directory = directory
    filetype = filetype
    constraints = constraints
    if isinstance(directory, six.string_types):
        loaded_cubes, cube_files = load_from_dir(
            directory, filetype, constraints)
        if not loaded_cubes:
            return "No cubes found".format()
        else:
            result = compare_cubes(loaded_cubes)
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
            return "No cubes found".format()
        else:
            result = compare_cubes(loaded_cubes)
            result = iris.cube.CubeList(result)
            try:
                result = result.concatenate_cube()
            except iris.exceptions.ConcatenateError:
                print("\nOops, there was an error in concatenation\n")
                examine_dim_bounds(result, cube_files)
            return result

def _add_catergorical(name, cube, coord):
    if name == 'season_year':
        iris.coord_categorisation.add_season_year(
            cube, coord, name='season_year')
    elif name == 'season_membership':
        iris.coord_categorisation.add_season_membership(
            cube, coord, name='season_membership')
    elif name == 'season_number':
        iris.coord_categorisation.add_season_number(
            cube, coord, name='number')
    elif name == 'clim_season':
        iris.coord_categorisation.add_season(
            cube, coord, name='clim_season')
    elif name == 'year':
        iris.coord_catergorisation.add_year(
            cube, coord, name='year')
    elif name == 'month_number':
        iris.coord_catergorisation.add_month_number(
            cube, coord, name='month_number')
    elif name == 'month_fullname':
        iris.coord_catergorisation.add_month_fullname(
            cube, coord, name='month_fullname')
    elif name == 'month':
        iris.coord_catergorisation.add_month(
            cube, coord, name='month')
    elif name == 'day_of_the_month':
        iris.coord_catergorisation.add_day_of_the_month(
            cube, coord, name='day_of_the_month')
    elif name == 'day_of_the_year':
        iris.coord_catergorisation.add_day_of_the_year(
            cube, coord, name='day_of_the_year')
    elif name == 'weekday_number':
        iris.coord_catergorisation.add_weekday_number(
            cube, coord, name='weekday_number')
    elif name == 'weekday_fullname':
        iris.coord_catergorisation.add_weekday_fullname(
            cube, coord, name='weekday_fullname')
    elif name == 'weekday':
        iris.coord_catergorisation.add_weekday(
            cube, coord, name='weekday')
    elif name == 'hour':
        iris.coord_catergorisation.add_hour(
            cube, coord, name='hour')

def add_catergorical(cubes, name, coord='time'):

    if isinstance(cubes, iris.cube.CubeList):
        for cube in cubes:
            _add_catergorical(name, cube, coord)
        return cubes

    else:
        _add_catergorical(name, cubes, coord)
        return cubes

def safe_concatenate(cubes):
    cube_list = compare_cubes(iris.cube.CubeList(cubes))
    cube = cube_list.concatenate_cube()
    return cube

