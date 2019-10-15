import iris
from cube_helper.cube_help import safe_concatenate
from glob import glob


def test_safe_concatenate():
    filepaths = glob('/project/champ/data/cmip5/output1/ICHEC/EC-EARTH/'
                         'rcp85/mon/atmos/Amon/r1i1p1/v20171115/tas/*.nc')
    test_load = [iris.load_cube(cube) for cube in filepaths]
    test_case_a = safe_concatenate(test_load)
    test_load = iris.cube.CubeList(test_load)
    test_case_b = safe_concatenate(test_load)
    assert isinstance(test_case_a, iris.cube.Cube)
    assert isinstance(test_case_b, iris.cube.Cube)