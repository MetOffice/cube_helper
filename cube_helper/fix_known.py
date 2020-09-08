# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.
from abc import ABCMeta, abstractmethod
import six

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
        Apply the fix to the object's cube.
        """
        pass


@six.add_metaclass(ABCMeta)
class FixKnownIssueIdentifyAttributes(FixKnownIssue):
    """
    An abstract base class to identify and fix known issues with data loaded
    into an `iris.cube.Cube`. A cube that needs this fix is identified by
    the attributes key-value pairs being found in `cube.attributes`.

    Args:
        cube: the cube to check, and if necessary fix.
    """
    @abstractmethod
    def __init__(self, cube):
        super(FixKnownIssueIdentifyAttributes, self).__init__(cube)
        self.attributes = {}

    def is_fix_needed(self):
        """
        Check if this fix applies to the object's cube by checking that all of
        the key-value pairs in `self.attributes` occur in `cube.attributes`.

        Returns:
            True if this fix should be applied to the cube that it was
            instantiated with.
        """
        for key in self.attributes:
            if key in self.cube.attributes:
                if self.cube.attributes[key] != self.attributes[key]:
                    return False
            else:
                return False
        # Haven't found anything that doesn't match
        return True


class FixCmip6CasFgoals(FixKnownIssueIdentifyAttributes):
    """
    Fix the latitude and longitude bounds in mip_era: CMIP6 institution_id: CAS
    source_id: FGOALS-f3-L, which are not contiguous and use
    `iris.coords.Coord.guess_bounds()` to calculate new bounds for these two
    coordinates.
    """
    def __init__(self, cube):
        super(FixCmip6CasFgoals, self).__init__(cube)
        self.attributes = {
            'mip_era': 'CMIP6',
            'institution_id': 'CAS',
            'source_id': 'FGOALS-f3-L'
        }

    def fix_cube(self):
        """
        Delete the existing faulty bounds on the latitude and longitude
        coordinates and then calculate new bounds.
        """
        log_message = 'Applying {}'.format(self.__class__.__name__)
        self.logger.info(log_message)

        self.cube.coord('latitude').bounds = None
        self.cube.coord('latitude').guess_bounds()
        self.cube.coord('longitude').bounds = None
        self.cube.coord('longitude').guess_bounds()


ALL_FIXES = [FixCmip6CasFgoals]


def fix_known_issues(cube):
    """
    Identify any issues that are known about in the input cube, fix these
    in-place and warn the user what has been fixed.

    The issues currently fixed are:

    mip_era: CMIP6 institution_id: CAS source_id: FGOALS-f3-L
        remove the latitude and longitude bounds, which are not contiguous and
        use `iris.coords.Coord.guess_bounds()` to calculate new bounds for
        these two coordinates.

    Args:
        cube: the iris.cube.Cube to fix
    """
    for klass in ALL_FIXES:
        fix = klass(cube)
        if fix.is_fix_needed():
            fix.fix_cube()
