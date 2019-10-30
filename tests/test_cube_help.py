import iris
from cube_helper.cube_help import cube_load, concatenate, add_categorical
from glob import glob


def test_concatenate():
    filepaths = glob('/project/champ/data/cmip5/output1/ICHEC/EC-EARTH'
                     '/rcp85/mon/atmos/Amon/r1i1p1/v20171115/tas/*.nc')
    test_load = [iris.load_cube(cube) for cube in filepaths]
    test_case_a = concatenate(test_load)
    test_load = iris.cube.CubeList(test_load)
    test_case_b = concatenate(test_load)
    assert isinstance(test_case_a, iris.cube.Cube)
    assert isinstance(test_case_b, iris.cube.Cube)


def test_cube_load():
    filepaths = glob('/project/champ/data/cmip5/output1/ICHEC/EC-EARTH/'
                     'rcp85/mon/atmos/Amon/r1i1p1/v20171115/tas/*.nc')
    directory = '/project/champ/data/cmip5/output1/ICHEC/EC-EARTH/' \
                'rcp85/mon/atmos/Amon/r1i1p1/v20171115/tas/'

    test_case_a = cube_load(filepaths)
    assert isinstance(test_case_a, iris.cube.Cube)
    assert test_case_a.dim_coords[0].units.origin == "days" \
                                                     " since 2006-01-01" \
                                                     " 00:00:00"
    assert test_case_a.dim_coords[0].units.calendar == "gregorian"
    test_case_b = cube_load(directory)
    assert test_case_b.dim_coords[0].units.origin == "days" \
                                                     " since 2006-01-01" \
                                                     " 00:00:00"
    assert test_case_b.dim_coords[0].units.calendar == "gregorian"


def test_add_categorical():
    filepaths = glob('/project/champ/data/cmip5/output1/ICHEC/EC-EARTH/'
                     'rcp85/mon/atmos/Amon/r1i1p1/v20171115/tas/*.nc')
    test_case_a = cube_load(filepaths)
    test_case_b = [iris.load_cube(cube) for cube in filepaths]
    test_categoricals = ["season_year", "season_number",
                          "season_membership", "season",
                          "year", "month_number",
                          "month_fullname", "month",
                          "day_of_month", "day_of_year",
                          "weekday_number", "weekday_fullname",
                          "weekday", "hour"]
    for categorical in test_categoricals:
        test_case_a = add_categorical(categorical, test_case_a)
        assert test_case_a.coord(categorical)
        test_case_a.remove_coord(categorical)

    for categorical in test_categoricals:
        for cube in test_case_b:
            cube = add_categorical(categorical, cube)
            assert cube.coord(categorical)
            cube.remove_coord(categorical)
