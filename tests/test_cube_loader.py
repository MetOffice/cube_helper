import os
import iris
from cube_helper.cube_loader import (load_from_dir,
                                     load_from_filelist,
                                     _parse_directory)



def test_load_from_filelist():

    abs_path = os.path.dirname(os.path.abspath(__file__))
    filelist = ['test_data/air_temp/air_temp_2.pp',
                'test_data/air_temp/air_temp_4.pp',
                'test_data/air_temp/air_temp_5.pp',
                'test_data/air_temp/air_temp_1.pp',
                'test_data/air_temp/air_temp_3.pp']
    abs_filelist = []
    for file in filelist:
        abs_filelist.append(abs_path + '/' + file)
    test_load, test_names = load_from_filelist(abs_filelist,
                                               '.pp')
    print(test_names)
    assert isinstance(test_load, list)
    assert isinstance(test_names, list)
    for cube in test_load:
        assert isinstance(cube, iris.cube.Cube)
    for name in test_names:
        assert isinstance(name, str)
        assert os.path.exists(name)


def test_load_from_dir():
    abs_path = os.path.dirname(os.path.abspath(__file__))\
               + '/test_data/air_temp/'

    test_load, test_names = load_from_dir(abs_path, '.pp')
    assert isinstance(test_load, list)
    assert isinstance(test_names, list)
    for cube in test_load:
        assert isinstance(cube, iris.cube.Cube)
    for name in test_names:
        assert isinstance(name, str)
        assert os.path.exists(name)


def test_parse_directory():
    directory = 'test_data/air_temp/air_temp_1.pp'
    assert _parse_directory(directory) == \
           '/test_data/air_temp/air_temp_1.pp/'
