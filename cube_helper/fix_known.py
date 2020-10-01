# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.
from abc import ABCMeta, abstractmethod
import six

import iris

from cube_helper.logger import log_module


@six.add_metaclass(ABCMeta)
class FixKnownIssue:
    """
    An abstract base class to identify and fix known issues with data loaded
    into an `iris.cube.Cube`.

    Args:
        cube: the cube to check, and if necessary fix.
    """
    def __init__(self, cube):
        self.cube = cube
        self.logger = log_module()
        self.message = ''

    @abstractmethod
    def is_fix_needed(self):
        """
        Check if this fix applies to the object's cube.

        Returns:
            True if this fix should be applied to the cube that it was
            instantiated with.
        """
        pass

    @abstractmethod
    def fix_cube(self):
        """
        Apply the fix to the object's cube and inform about the name and
        contents of the fix that has been applied.
        """
        log_message = 'Applying {}. {}'.format(self.__class__.__name__,
                                               self.message)
        self.logger.info(log_message)


@six.add_metaclass(ABCMeta)
class FixKnownIssueIdentifyAttributes(FixKnownIssue):
    """
    An abstract base class to identify and fix known issues with data loaded
    into an `iris.cube.Cube`. A cube that needs this fix is identified by
    the class' `cube_attributes_required` attribute key-value pairs being
    found in `cube.attributes`.

    Args:
        cube: the cube to check, and if necessary fix.
    """
    @abstractmethod
    def __init__(self, cube):
        super(FixKnownIssueIdentifyAttributes, self).__init__(cube)
        self.cube_attributes_required = {}

    def is_fix_needed(self):
        """
        Check if this fix applies to the object's cube by checking that all of
        the key-value pairs in `self.cube_attributes_required` occur in
        `cube.attributes`.

        Returns:
            True if this fix should be applied to the cube that it was
            instantiated with.
        """
        test_result = True
        for key, value in six.iteritems(self.cube_attributes_required):
            if key in self.cube.attributes:
                if self.cube.attributes[key] != value:
                    test_result = False
                    break
            else:
                test_result = False
                break
        # Haven't found anything that doesn't match
        return test_result


class FixCmip6CasFgoals(FixKnownIssueIdentifyAttributes):
    """
    Fix the latitude and longitude bounds in

    * mip_era: CMIP6
    * institution_id: CAS
    * source_id: FGOALS-f3-L

    that are not contiguous and use `iris.coords.Coord.guess_bounds()` to
    calculate new bounds for these two coordinates.

    Args:
        cube: the cube to check, and if necessary fix.
    """
    def __init__(self, cube):
        super(FixCmip6CasFgoals, self).__init__(cube)
        self.cube_attributes_required = {
            'mip_era': 'CMIP6',
            'institution_id': 'CAS',
            'source_id': 'FGOALS-f3-L'
        }
        self.message = 'Fixing latitude and longitude bounds.'

    def fix_cube(self):
        """
        Delete the existing faulty bounds on the latitude and longitude
        coordinates and then calculate new bounds.
        """
        super(FixCmip6CasFgoals, self).fix_cube()
        self.cube.coord('latitude').bounds = None
        self.cube.coord('latitude').guess_bounds()
        self.cube.coord('longitude').bounds = None
        self.cube.coord('longitude').guess_bounds()


class FixCmip6FioqlnmFioesm20Historical(FixKnownIssueIdentifyAttributes):
    """
    Fix the latitude and longitude bounds in

    * mip_era: CMIP6
    * institution_id: FIO-QLNM
    * source_id: FIO-ESM-2-0
    * experiment: historical

    which are different to other FIO-ESM-2-0 experiments and are not monotonic,
    preventing latitude from being a dimension coordinate.
    `iris.coords.Coord.guess_bounds()` calculates bounds for these two
    coordinates that are identical to the bounds in other experiments and allow
    latitude to be promoted to a dimension coordinate.

    Args:
        cube: the cube to check, and if necessary fix.
    """
    def __init__(self, cube):
        super(FixCmip6FioqlnmFioesm20Historical, self).__init__(cube)
        self.cube_attributes_required = {
            'mip_era': 'CMIP6',
            'institution_id': 'FIO-QLNM',
            'source_id': 'FIO-ESM-2-0',
            'experiment_id': 'historical'
        }
        self.message = ('Fixing latitude and longitude bounds and promoting '
                        'latitude to a dimension coordinate.')

    def fix_cube(self):
        """
        Delete the existing faulty bounds on the latitude and longitude
        coordinates and then calculate new bounds.
        """
        super(FixCmip6FioqlnmFioesm20Historical, self).fix_cube()
        self.cube.coord('latitude').bounds = None
        self.cube.coord('latitude').guess_bounds()
        self.cube.coord('longitude').bounds = None
        self.cube.coord('longitude').guess_bounds()
        iris.util.promote_aux_coord_to_dim_coord(self.cube, 'latitude')


# List all concrete fixes that should be applied. They should also be
# described in the docstring for `fix_known_issues()`
ALL_FIXES = [FixCmip6CasFgoals, FixCmip6FioqlnmFioesm20Historical]


def fix_known_issues(cube):
    """
    Identify any issues that are known about in the input cube, fix these
    in-place and warn the user what has been fixed.

    The issues currently fixed are:

    **mip_era** `CMIP6` **institution_id** `CAS` **source_id** `FGOALS-f3-L`
    remove the latitude and longitude bounds, which are not contiguous, and
    use `iris.coords.Coord.guess_bounds()` to calculate new bounds for
    these two coordinates.

    **mip_era** `CMIP6` **institution_id** `FIO-QLNM` **source_id**
    `FIO-ESM-2-0` **experiment** `historical`
    remove the latitude and longitude bounds, which are not monotonic, and
    use `iris.coords.Coord.guess_bounds()` to calculate new bounds for
    these two coordinates, which are identical to the bounds in other
    `FIO-ESM-2-0` experiments. latitude is then promoted to a dimension
    coordinate.

    Args:
        cube: the iris.cube.Cube to fix
    """
    for fixer in ALL_FIXES:
        fix = fixer(cube)
        if fix.is_fix_needed():
            fix.fix_cube()
