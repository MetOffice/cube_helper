import unittest
import iris
import cube_helper
from cube_helper import CubeHelp


class TestCubeHelper(unittest.TestCase):

    def test_initilisation(self):
        example = CubeHelp('test_data/air_temp',
                           filetype='.pp', constraints='air_temperature')
        self.assertEqual(example.directory, 'test_data/air_temp')
        self.assertEqual(example.filetype, '.pp')
        self.assertEqual(example.constraints, 'air_temperature')
        self.assertIsInstance(example.cube_dataset,
                              cube_helper.cube_dataset.CubeSet)
        filelist = ['test_data/air_temp/air_temp_1.pp',
                    'test_data/air_temp/air_temp_2.pp',
                    'test_data/air_temp/air_temp_3.pp',
                    'test_data/air_temp/air_temp_4.pp',
                    'test_data/air_temp/air_temp_5.pp']
        example = CubeHelp(filelist, filetype='.pp')
        self.assertIsInstance(example.directory, list)

    def test_get_concatenated_cube(self):
        filepath = '/project/champ/data/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/' \
                   'piControl/r1i1p1f1/Amon/tasmin/gn/v20190628'
        example = CubeHelp(filepath)
        test_method = example.get_concatenated_cube()
        self.assertIsInstance(test_method, iris.cube.Cube)
        self.assertEqual(test_method.ndim, 3)

    def test_concatenate_cube(self):
        filepath = '/project/champ/data/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/' \
                   'piControl/r1i1p1f1/Amon/tasmin/gn/v20190628'
        example = CubeHelp(filepath)
        example.concatenate_cube()
        self.assertIsInstance(example.cube_dataset, iris.cube.CubeList)
        self.assertEqual(example.cube_dataset[0].ndim, 3)

    def test_get_concatenated(self):
        example = CubeHelp('test_data/north_sea_ice', filetype='.pp')
        test_method = example.get_concatenated()
        self.assertIsInstance(test_method, iris.cube.CubeList)

    def test_concatenate(self):
        example = CubeHelp('test_data/north_sea_ice', filetype='.pp')
        example.concatenate()
        self.assertIsInstance(example.cube_dataset, iris.cube.CubeList)

    def test_get_merged(self):
        example = CubeHelp('test_data/north_sea_ice', filetype='.pp')
        test_method = example.get_merged()
        self.assertIsInstance(test_method, iris.cube.CubeList)

    def test_merge(self):
        example = CubeHelp('test_data/north_sea_ice', filetype='.pp')
        example.merge()
        self.assertIsInstance(example.cube_dataset, iris.cube.CubeList)

    def test_get_merged_cube(self):
        example = CubeHelp('test_data/north_sea_ice', filetype='.pp')
        merged_cube = example.get_merged_cube()
        self.assertIsInstance(merged_cube, iris.cube.Cube)
        self.assertEqual(merged_cube.ndim, 3)

    def test_merge_cube(self):
        example = CubeHelp('test_data/north_sea_ice', filetype='.pp')
        example.merge_cube()
        self.assertIsInstance(example.cube_dataset, iris.cube.CubeList)
        self.assertEqual(example.cube_dataset[0].ndim, 3)

    def test_convert_units(self):
        example = CubeHelp('test_data/air_temp', filetype='.pp')
        example.convert_units('celsius')
        for cube in example.cube_dataset:
            self.assertEqual(cube.units, 'celsius')

    def test_collapsed_dimension(self):
        example = CubeHelp('test_data/north_sea_ice', filetype='.pp')
        example.collapsed_dimension('longitude')
        for cube in example.cube_dataset:
            self.assertEqual(cube.ndim, 1)

    def test_get_cube(self):
        example = CubeHelp('test_data/north_sea_ice', filetype='.pp')
        test = example.get_cube(0)
        self.assertIsInstance(test, iris.cube.Cube)

    def test_remove_cube(self):
        example = CubeHelp('test_data/north_sea_ice', filetype='.pp')
        example.remove_cube(0)
        self.assertEqual(len(example.cube_dataset), 3)

    def test_add_time_catergorical(self):
        example = CubeHelp('/net/home/h03/frpt/EC-EARTH_rcp85/')
        cube = example.get_concatenated_cube()
        example.concatenate_cube()
        example.add_time_catergorical('season_year')
        example.add_time_catergorical('clim_season')
        iris.coord_categorisation.add_season_year(cube,
                                                  'time', name='season_year')
        iris.coord_categorisation.add_season(cube,
                                             'time', name='clim_season')
        self.assertEqual(example.cube_dataset[0].coord('time'),
                         cube.coord('time'))
        self.assertEqual(example.cube_dataset[0].dim_coords,
                         cube.dim_coords)
        self.assertEqual(example.cube_dataset[0].aux_coords,
                         cube.aux_coords)
        self.assertEqual(example.cube_dataset[0].ndim,
                         cube.ndim)

    def test_aggregate(self):
        example = CubeHelp('/net/home/h03/frpt/EC-EARTH_rcp85/')
        cube = example.get_concatenated_cube()
        example.concatenate_cube()
        example.add_time_catergorical('season_year')
        example.add_time_catergorical('clim_season')
        example.aggregate(['clim_season', 'season_year'])
        iris.coord_categorisation.add_season_year(cube, 'time',
                                                  name='season_year')
        iris.coord_categorisation.add_season(cube, 'time',
                                             name='clim_season')
        cube = cube.aggregated_by(['clim_season', 'season_year'],
                                  iris.analysis.MEAN)
        self.assertEqual(example.cube_dataset[0].coord('time'),
                         cube.coord('time'))
        self.assertEqual(example.cube_dataset[0].dim_coords,
                         cube.dim_coords)
        self.assertEqual(example.cube_dataset[0].aux_coords,
                         cube.aux_coords)
        self.assertEqual(example.cube_dataset[0].ndim, cube.ndim)

    def test_extract(self):
        future_constraint = iris.Constraint(
            clim_season='jja',
            season_year=lambda cell: cell >= 2010 and cell <= 2060)
        example = CubeHelp('/net/home/h03/frpt/EC-EARTH_rcp85/')
        cube = example.get_concatenated_cube()
        example.concatenate_cube()
        example.add_time_catergorical('season_year')
        example.add_time_catergorical('clim_season')
        example.aggregate(['clim_season', 'season_year'])
        example.extract(future_constraint)
        iris.coord_categorisation.add_season_year(cube,
                                                  'time', name='season_year')
        iris.coord_categorisation.add_season(cube,
                                             'time', name='clim_season')
        cube = cube.aggregated_by(
            ['clim_season', 'season_year'], iris.analysis.MEAN)
        cube = cube.extract(future_constraint)
        self.assertEqual(example.cube_dataset[0].coord('time'),
                         cube.coord('time'))
        self.assertEqual(example.cube_dataset[0].dim_coords,
                         cube.dim_coords)
        self.assertEqual(example.cube_dataset[0].aux_coords,
                         cube.aux_coords)
        self.assertEqual(example.cube_dataset[0].ndim,
                         cube.ndim)


if __name__ == "__main__":
    unittest.main()
