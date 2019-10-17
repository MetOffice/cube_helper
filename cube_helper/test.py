from cube_helper import cube_load
from glob import glob


file1 = glob('/project/champ/data/cmip5/output1/NOAA-GFDL/GFDL-ESM2M/historical/mon/atmos/Amon/r1i1p1/v20111228/tas/*.nc')
file2 = glob('/project/champ/data/cmip5/output1/NOAA-GFDL/GFDL-ESM2M/rcp85/mon/atmos/Amon/r1i1p1/v20111228/tas/*.nc')
file1.extend(file2)
cube = cube_load(file1)
