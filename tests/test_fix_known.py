# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.
import sys
if sys.version_info >= (3, 3):
    from unittest import mock
else:
    import mock
from unittest import TestCase              # noqa: E402

import iris                                # noqa: E402
from iris.tests.stock import realistic_3d  # noqa: E402
import numpy as np                         # noqa: E402

import cube_helper as ch                   # noqa: E402


class ExampleConcreteClass(
    ch.fix_known.FixKnownIssueIdentifyAttributes
):
    """
    A concrete class of the abstract FixKnownIssueIdentifyAttributes to allow
    its concrete methods to be tested.
    """
    def __init__(self, cube):
        super(ExampleConcreteClass, self).__init__(cube)
        self.cube_attributes_required = {
            'attrib_1': 'a',
            'attrib_2': 'b'
        }

    def fix_cube(self):
        super(ExampleConcreteClass, self).fix_cube()


class TestIdentifyAttributesFixNeeded(TestCase):
    """
    Test
    cube_helper.fix_known.FixKnownIssueIdentifyAttributes.is_fix_needed()
    """
    def test_missing_attribute(self):
        cube = realistic_3d()
        fix = ExampleConcreteClass(cube)
        self.assertFalse(fix.is_fix_needed())

    def test_different_attr_value(self):
        cube = realistic_3d()
        cube.attributes['attrib_1'] = 'a'
        cube.attributes['attrib_2'] = 'a'
        fix = ExampleConcreteClass(cube)
        self.assertFalse(fix.is_fix_needed())

    def test_all_attributes_match(self):
        cube = realistic_3d()
        cube.attributes['attrib_1'] = 'a'
        cube.attributes['attrib_2'] = 'b'
        fix = ExampleConcreteClass(cube)
        self.assertTrue(fix.is_fix_needed())


class TestFixCmip6CasFgoals(TestCase):
    """Test cube_helper.fix_known.FixCmip6CasFgoals"""
    def setUp(self):
        self.cube = _make_fgoals_cube()

        patch = mock.patch('cube_helper.fix_known.log_module')
        self.mock_logger = patch.start()
        self.addCleanup(patch.stop)

    def test_is_fix_needed(self):
        fix = ch.fix_known.FixCmip6CasFgoals(self.cube)
        self.assertTrue(fix.is_fix_needed())

    def test_is_fix_needed_fails_mip_era(self):
        self.cube.attributes['mip_era'] = 'ABCD'
        fix = ch.fix_known.FixCmip6CasFgoals(self.cube)
        self.assertFalse(fix.is_fix_needed())

    def test_is_fix_needed_fails_institution_id(self):
        del self.cube.attributes['institution_id']
        fix = ch.fix_known.FixCmip6CasFgoals(self.cube)
        self.assertFalse(fix.is_fix_needed())

    def test_is_fix_needed_fails_source_id(self):
        self.cube.attributes['source_id'] = '1234'
        fix = ch.fix_known.FixCmip6CasFgoals(self.cube)
        self.assertFalse(fix.is_fix_needed())

    def test_log_message(self):
        fix = ch.fix_known.FixCmip6CasFgoals(self.cube)
        fix.fix_cube()
        fix.logger.info.assert_called_with('Applying FixCmip6CasFgoals')

    def test_constructed_cube_not_contiguous(self):
        """Check that the constructed test cube coords are not contiguous"""
        for coord_name in ['latitude', 'longitude']:
            coord = self.cube.coord(coord_name)
            self.assertFalse(coord.is_contiguous())

    def test_bounds_contiguous(self):
        fix = ch.fix_known.FixCmip6CasFgoals(self.cube)
        fix.fix_cube()
        for coord_name in ['latitude', 'longitude']:
            coord = self.cube.coord(coord_name)
            self.assertTrue(coord.is_contiguous())


class TestFixCmip6FioqlnmFioesm20Historical(TestCase):
    """Test cube_helper.fix_known.FixCmip6FioqlnmFioesm20Historical"""
    def setUp(self):
        self.cube = _make_fioesm20_historical_cube()

        patch = mock.patch('cube_helper.fix_known.log_module')
        self.mock_logger = patch.start()
        self.addCleanup(patch.stop)

    def test_is_fix_needed(self):
        fix = ch.fix_known.FixCmip6FioqlnmFioesm20Historical(self.cube)
        self.assertTrue(fix.is_fix_needed())

    def test_is_fix_needed_fails_mip_era(self):
        self.cube.attributes['mip_era'] = 'ABCD'
        fix = ch.fix_known.FixCmip6FioqlnmFioesm20Historical(self.cube)
        self.assertFalse(fix.is_fix_needed())

    def test_is_fix_needed_fails_institution_id(self):
        del self.cube.attributes['institution_id']
        fix = ch.fix_known.FixCmip6FioqlnmFioesm20Historical(self.cube)
        self.assertFalse(fix.is_fix_needed())

    def test_is_fix_needed_fails_source_id(self):
        self.cube.attributes['source_id'] = '1234'
        fix = ch.fix_known.FixCmip6FioqlnmFioesm20Historical(self.cube)
        self.assertFalse(fix.is_fix_needed())

    def test_is_fix_needed_fails_experiment_id(self):
        self.cube.attributes['experiment_id'] = '1234'
        fix = ch.fix_known.FixCmip6FioqlnmFioesm20Historical(self.cube)
        self.assertFalse(fix.is_fix_needed())

    def test_log_message(self):
        fix = ch.fix_known.FixCmip6FioqlnmFioesm20Historical(self.cube)
        fix.fix_cube()
        fix.logger.info.assert_called_with('Applying FixCmip6FioqlnmFioesm20'
                                           'Historical')

    def test_constructed_cube_not_monotonic(self):
        """Check that the constructed test cube latitude is not monotonic"""
        self.assertFalse(self.cube.coord('latitude').is_monotonic())

    def test_constructed_cube_dim_coords(self):
        """Check that the constructed test cube latitude is not dim coord"""
        dim_coord_names = [dim_coord.standard_name
                           for dim_coord in self.cube.dim_coords]
        expected_names = ['time', 'longitude']
        self.assertEqual(dim_coord_names, expected_names)

    def test_bounds_monotonic(self):
        fix = ch.fix_known.FixCmip6FioqlnmFioesm20Historical(self.cube)
        fix.fix_cube()
        coord = self.cube.coord('latitude')
        self.assertTrue(coord.is_monotonic())

    def test_dim_coords(self):
        fix = ch.fix_known.FixCmip6FioqlnmFioesm20Historical(self.cube)
        fix.fix_cube()
        dim_coords_names = [dim_coord.standard_name
                            for dim_coord in self.cube.dim_coords]
        expected_names = ['time', 'latitude', 'longitude']
        self.assertEqual(dim_coords_names, expected_names)


class TestFixKnownIssue(TestCase):
    """Test cube_helper.fix_known.fix_known_issues()"""
    def setUp(self):
        patch = mock.patch('cube_helper.fix_known.log_module')
        log_module = patch.start()
        self.mock_logger = mock.Mock()
        log_module.return_value = self.mock_logger
        self.addCleanup(patch.stop)

    def test_fgoals_message(self):
        cube = _make_fgoals_cube()
        ch.fix_known_issues(cube)
        self.mock_logger.info.assert_called_with('Applying FixCmip6CasFgoals')

    def test_no_fix_required_message(self):
        cube = realistic_3d()
        ch.fix_known_issues(cube)
        self.mock_logger.info.assert_not_called()

    def test_fgoals_is_contiguous(self):
        cube = _make_fgoals_cube()
        ch.fix_known_issues(cube)
        for coord_name in ['latitude', 'longitude']:
            coord = cube.coord(coord_name)
            self.assertTrue(coord.is_contiguous())

    def test_normal_cube_is_unchanged(self):
        cube = realistic_3d()
        reference_cube = realistic_3d()
        ch.fix_known_issues(cube)
        self.assertEqual(cube, reference_cube)


def _make_fgoals_cube():
    """
    Use an Iris test cube and modify the metadata and bounds to make it look
    like a CMIP6.CAS.FGOALS-f3-L cube. The FGOALS-f3-L bounds are not
    contiguous.

    Returns:
        An `Iris.cube.Cube` object that looks like a cube loaded from file
        for the CMIP6.CAS.FGOALS-f3-L model.
    """
    cube = realistic_3d()
    cube.attributes['mip_era'] = 'CMIP6'
    cube.attributes['institution_id'] = 'CAS'
    cube.attributes['source_id'] = 'FGOALS-f3-L'
    for coord_name in ['latitude', 'longitude']:
        coord = cube.coord('grid_' + coord_name)
        coord.standard_name = coord_name
        point_spacing = coord.points[1] - coord.points[0]
        coord.bounds = (np.array([coord.points - (0.4 * point_spacing),
                                 coord.points + (0.4 * point_spacing)]).
                        transpose())
    return cube


def _make_fioesm20_historical_cube():
    """
    Use an Iris test cube and modify the metadata and bounds to make it look
    like a CMIP6.CMIP.FIO-QLNM.FIO-ESM-2-0.historical cube, which has a
    non-monotonic latitude coordinate that is an auxillary coordinate rather
    than a dimension coordinate.

    Returns:
        An `Iris.cube.Cube` object that looks like a cube loaded from file
        for the CMIP6.CMIP.FIO-QLNM.FIO-ESM-2-0.historical experiment.
    """
    cube = realistic_3d()
    cube.attributes['mip_era'] = 'CMIP6'
    cube.attributes['institution_id'] = 'FIO-QLNM'
    cube.attributes['source_id'] = 'FIO-ESM-2-0'
    cube.attributes['experiment_id'] = 'historical'
    for coord_name in ['latitude', 'longitude']:
        coord = cube.coord('grid_' + coord_name)
        coord.standard_name = coord_name

    iris.util.demote_dim_coord_to_aux_coord(cube, 'latitude')
    # Cannot set invalid bounds because the setter checks them and so
    # construct new coordinate instead and replace the existing latitude
    latitude = cube.coord('latitude')
    point_spacing = latitude.points[1] - latitude.points[0]
    bounds = (np.array([latitude.points,
                        latitude.points + point_spacing]).transpose())
    bounds[-1, 1] = latitude.points[-1]

    new_latitude = iris.coords.AuxCoord(
        latitude.points,
        standard_name=latitude.standard_name,
        long_name=latitude.long_name,
        var_name=latitude.var_name,
        units=latitude.units,
        bounds=bounds,
        attributes=latitude.attributes,
        coord_system=latitude.coord_system
    )
    cube.replace_coord(new_latitude)
    return cube
