# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.
import sys
import cf_units
import iris
import iris.coords as icoords
from iris.coord_systems import GeogCS, RotatedGeogCS
import numpy as np
import contextlib


def _generate_ocean_cube():
    """
    Returns a realistic 3d ocean cube with an extended time range.
    """
    cube_list = iris.cube.CubeList()
    lower_bound = 0
    upper_bound = 70
    period = 70
    for i in range(0, 100):
        data = np.arange(70 * 9 * 11).reshape((70, 9, 11))
        lat_pts = np.arange(9 * 11).reshape(9, 11)
        lon_pts = np.arange(9 * 11).reshape(9, 11)

        time_pts = np.linspace(lower_bound, upper_bound - 1, 70)
        cell_index_first = np.linspace(0, 8, 9)
        cell_index_second = np.linspace(0, 10, 11)

        lat = icoords.AuxCoord(
            lat_pts,
            standard_name="grid_latitude",
            units="degrees",
        )
        lon = icoords.AuxCoord(
            lon_pts,
            standard_name="grid_longitude",
            units="degrees",
        )
        time = icoords.DimCoord(
            time_pts, standard_name="time",
            units="days since 1970-01-01 00:00:00"
        )
        cell_index_first = icoords.DimCoord(
            cell_index_first, units=cf_units.Unit('1'),
            long_name='cell index along first dimension', var_name='i'
        )

        cell_index_second = icoords.DimCoord(
            cell_index_second, units=cf_units.Unit('1'),
            long_name='cell index along second dimension', var_name='j'
        )

        cube = iris.cube.Cube(
            data,
            standard_name='surface_downward_mass_flux_of_carbon'
                          '_dioxide_expressed_as_carbon',
            units=cf_units.Unit('kg m-2 s-1'),
            dim_coords_and_dims=[(time, 0),
                                 (cell_index_first, 1),
                                 (cell_index_second, 2)],
            aux_coords_and_dims=[(lat, (1, 2)), (lon, (1, 2))],
            attributes={"source": "Iris test case"},
        )
        lower_bound = lower_bound + 70
        upper_bound = upper_bound + 70
        period = period + 70
        cube_list.append(cube)
    return cube_list


def _generate_extended_cube():
    cube_list = iris.cube.CubeList()
    lower_bound = 0
    upper_bound = 70
    period = 70
    data = np.arange(70 * 9 * 11).reshape((70, 9, 11))
    lat_pts = np.linspace(-4, 4, 9)
    lon_pts = np.linspace(-5, 5, 11)
    ll_cs = RotatedGeogCS(37.5, 177.5, ellipsoid=GeogCS(6371229.0))
    for i in range(0, 100):
        time_pts = np.linspace(lower_bound, upper_bound - 1, 70)
        lat = icoords.DimCoord(
            lat_pts,
            standard_name="grid_latitude",
            units="degrees",
            coord_system=ll_cs,
        )
        lon = icoords.DimCoord(
            lon_pts,
            standard_name="grid_longitude",
            units="degrees",
            coord_system=ll_cs,
        )
        time = icoords.DimCoord(
            time_pts,
            standard_name="time",
            units="days since 1970-01-01 00:00:00"
        )
        cube = iris.cube.Cube(
            data,
            standard_name="air_potential_temperature",
            units="K",
            dim_coords_and_dims=[(time, 0),
                                 (lat, 1),
                                 (lon, 2)],
            attributes={"source": "Iris test case"},
        )
        lower_bound = lower_bound + 70
        upper_bound = upper_bound + 70
        period = period + 70
        cube_list.append(cube)
    cube = cube_list.concatenate_cube()
    return cube


@contextlib.contextmanager
def _redirect_stdout(target):
    original = sys.stdout
    sys.stdout = target
    yield
    sys.stdout = original

@contextlib.contextmanager
def _redirect_stderr(target):
    original = sys.stderr
    sys.stderr = target
    yield
    sys.stderr = original

