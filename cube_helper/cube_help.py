import iris
import iris.coord_categorisation
from six import string_types
from cube_helper.cube_loader import load_from_filelist, load_from_dir
from cube_helper.cube_equaliser import compare_cubes, examine_dim_bounds


def cube_load(directory, filetype='.nc', constraints=None):

    directory = directory
    filetype = filetype
    constraints = constraints
    if isinstance(directory, string_types):
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

def _add_catergorical(cater_name, cube, coord, season, seasons):

    if cater_name == 'season_year':
        iris.coord_categorisation.add_season_year(
            cube, coord, name='season_year')

    elif cater_name == 'season_membership':
        iris.coord_categorisation.add_season_membership(
            cube, coord, name='season_membership',
            season=season)

    elif cater_name == 'season_number' or cater_name == 'number':
        iris.coord_categorisation.add_season_number(
            cube, coord, name='season_number',
            seasons=seasons)

    elif cater_name == 'clim_season' or cater_name =='season':
        iris.coord_categorisation.add_season(
            cube, coord, name='season', seasons=seasons)

    elif cater_name == 'year':
        iris.coord_categorisation.add_year(
            cube, coord, name='year')

    elif cater_name == 'month_number':
        iris.coord_categorisation.add_month_number(
            cube, coord, name='month_number')

    elif cater_name == 'month_fullname':
        iris.coord_categorisation.add_month_fullname(
            cube, coord, name='month_fullname')

    elif cater_name == 'month':
        iris.coord_categorisation.add_month(
            cube, coord, name='month')

    elif cater_name == 'day_of_month':
        iris.coord_categorisation.add_day_of_month(
            cube, coord, name='day_of_month')

    elif cater_name == 'day_of_year':
        iris.coord_categorisation.add_day_of_year(
            cube, coord, name='day_of_year')

    elif cater_name == 'weekday_number':
        iris.coord_categorisation.add_weekday_number(
            cube, coord, name='weekday_number')

    elif cater_name == 'weekday_fullname':
        iris.coord_categorisation.add_weekday_fullname(
            cube, coord, name='weekday_fullname')

    elif cater_name == 'weekday':
        iris.coord_categorisation.add_weekday(
            cube, coord, name='weekday')

    elif cater_name == 'hour':
        iris.coord_categorisation.add_hour(
            cube, coord, name='hour')

    else:
        pass
def add_catergorical(cater_name, cubes, coord='time', season='djf'
                     , seasons=('djf', 'mam', 'jja', 'son')):

    if isinstance(cubes, iris.cube.CubeList) or isinstance(cubes, list):
        for cube in cubes:
            _add_catergorical(cater_name, cube,
                              coord, season, seasons)
        return cubes

    else:
        _add_catergorical(cater_name, cubes,
                          coord, season, seasons)
        return cubes

def safe_concatenate(cubes):
    cube_list = compare_cubes(iris.cube.CubeList(cubes))
    cube = cube_list.concatenate_cube()
    return cube

