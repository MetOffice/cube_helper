
Cube Helper: A Walk-through guide
---------------------------------

This Python module has been produced to mitigate the issues faced by
researchers whilst trying to manipulate multiple cubes.

Before starting, the module needs to be added to your python
environment:

.. code:: ipython3

    !export PYTHONPATH=/net/home/h01/jbedwell/Downloads/cube_helper

The main class of interest for this module is the ``CubeHelp`` class. To
illustrate it’s usage, lets start by importing the module (and Iris!)

.. code:: ipython3

    import iris
    from cube_helper import CubeHelp

The ``CubeHelp`` object once instantiated loads the given dataset as
Follows:

.. code:: ipython3

    dataset = CubeHelp('/project/champ/data/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/piControl/r1i1p1f1/Amon/tasmin/gn/v20190628')


.. parsed-literal::

    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))


Here we see that the module will load the cubes automatically. Once the
``CubeHelp`` object has been created we can view the loaded dataset:

.. code:: ipython3

    dataset




.. parsed-literal::

    0: air_temperature / (K)               (time: 1200; latitude: 144; longitude: 192)
    1: air_temperature / (K)               (time: 1200; latitude: 144; longitude: 192)
    2: air_temperature / (K)               (time: 1200; latitude: 144; longitude: 192)
    3: air_temperature / (K)               (time: 1200; latitude: 144; longitude: 192)
    4: air_temperature / (K)               (time: 1200; latitude: 144; longitude: 192)



A very common problem when concatenatting and merging cubes is that the
attributes mismatch, this can be illustrated when we try to invoke the
wraped Iris ``concatenate_cube()`` function. Below we see an example of
this error message:

.. code:: ipython3

    import glob
    filelist = glob.glob('/project/champ/data/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/piControl/r1i1p1f1/Amon/tasmin/gn/v20190628/*.nc')

.. code:: ipython3

    cubes = iris.load(filelist)


.. parsed-literal::

    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))


And then we try concatenate:

.. code:: ipython3

    cubes.concatenate_cube()


::


    ---------------------------------------------------------------------------

    ConcatenateError                          Traceback (most recent call last)

    <ipython-input-13-cdd4eeb66b76> in <module>
    ----> 1 cubes.concatenate_cube()
    

    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/cube.py in concatenate_cube(self, check_aux_coords)
        500             res = iris._concatenate.concatenate(
        501                 self, error_on_mismatch=True,
    --> 502                 check_aux_coords=check_aux_coords)
        503             n_res_cubes = len(res)
        504             if n_res_cubes == 1:


    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/_concatenate.py in concatenate(cubes, error_on_mismatch, check_aux_coords)
        270         for proto_cube in proto_cubes:
        271             registered = proto_cube.register(cube, axis, error_on_mismatch,
    --> 272                                              check_aux_coords)
        273             if registered:
        274                 axis = proto_cube.axis


    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/_concatenate.py in register(self, cube, axis, error_on_mismatch, check_aux_coords)
        716         # Check for compatible cube signatures.
        717         cube_signature = _CubeSignature(cube)
    --> 718         match = self._cube_signature.match(cube_signature, error_on_mismatch)
        719 
        720         # Check for compatible coordinate signatures.


    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/_concatenate.py in match(self, other, error_on_mismatch)
        474         match = not bool(msgs)
        475         if error_on_mismatch and not match:
    --> 476             raise iris.exceptions.ConcatenateError(msgs)
        477         return match
        478 


    ConcatenateError: failed to concatenate into a single cube.
      Cube metadata differs for phenomenon: air_temperature


Here we see that differences in metadata prevent the cube from being
concatenated, and throws a very verbous and long winded error.

Here we can use cube_helper, which cycles through each cube, and removes
attributes, aux coords and dim coords that are not uniform across the
dataset. Lets try it out:

.. code:: ipython3

    print(dataset.get_concatenated_cube())


.. parsed-literal::

    air_temperature / (K)               (time: 6000; latitude: 144; longitude: 192)
         Dimension coordinates:
              time                           x               -               -
              latitude                       -               x               -
              longitude                      -               -               x
         Scalar coordinates:
              height: 1.5 m
         Attributes:
              Conventions: CF-1.7 CMIP-6.2
              activity_id: CMIP
              branch_method: standard
              branch_time_in_child: 0.0
              branch_time_in_parent: 267840.0
              cmor_version: 3.4.0
              comment: minimum near-surface (usually, 2 meter) air temperature (add cell_method...
              cv_version: 6.2.20.1
              data_specs_version: 01.00.29
              experiment: pre-industrial control
              experiment_id: piControl
              external_variables: areacella
              forcing_index: 1
              frequency: mon
              further_info_url: https://furtherinfo.es-doc.org/CMIP6.MOHC.HadGEM3-GC31-LL.piControl.no...
              grid: Native N96 grid; 192 x 144 longitude/latitude
              grid_label: gn
              initialization_index: 1
              institution: Met Office Hadley Centre, Fitzroy Road, Exeter, Devon, EX1 3PB, UK
              institution_id: MOHC
              license: CMIP6 model data produced by the Met Office Hadley Centre is licensed under...
              mip_era: CMIP6
              mo_runid: u-ar766
              nominal_resolution: 250 km
              original_name: mo: mon_mean_from_day((stash: m01s03i236, lbproc: 4096))
              parent_activity_id: CMIP
              parent_experiment_id: piControl-spinup
              parent_mip_era: CMIP6
              parent_source_id: HadGEM3-GC31-LL
              parent_time_units: days since 1850-01-01-00-00-00
              parent_variant_label: r1i1p1f1
              physics_index: 1
              product: model-output
              realization_index: 1
              realm: atmos
              source: HadGEM3-GC31-LL (2016): 
    aerosol: UKCA-GLOMAP-mode
    atmos: MetUM-HadGEM3-GA7.1...
              source_id: HadGEM3-GC31-LL
              source_type: AOGCM AER
              sub_experiment: none
              sub_experiment_id: none
              table_id: Amon
              table_info: Creation Date:(13 December 2018) MD5:2b12b5db6db112aa8b8b0d6c1645b121
              title: HadGEM3-GC31-LL output prepared for CMIP6
              variable_id: tasmin
              variant_label: r1i1p1f1
         Cell methods:
              mean: area
              minimum within days: time
              mean over days: time


As shown the function returns a concatenated cube. This functionality is
not limited to equalising and concatenating cubes. Functions are also
provided for converting one unit to another, below this is illustrated,
with the argument ``'celsius'`` passed converting the dataset’s units:

.. code:: ipython3

    dataset.convert_units('celsius')
    dataset




.. parsed-literal::

    0: air_temperature / (celsius)         (time: 1200; latitude: 144; longitude: 192)
    1: air_temperature / (celsius)         (time: 1200; latitude: 144; longitude: 192)
    2: air_temperature / (celsius)         (time: 1200; latitude: 144; longitude: 192)
    3: air_temperature / (celsius)         (time: 1200; latitude: 144; longitude: 192)
    4: air_temperature / (celsius)         (time: 1200; latitude: 144; longitude: 192)



And back again into Kelvin (``'K'``)

.. code:: ipython3

    dataset.convert_units('K')
    dataset




.. parsed-literal::

    0: air_temperature / (K)               (time: 1200; latitude: 144; longitude: 192)
    1: air_temperature / (K)               (time: 1200; latitude: 144; longitude: 192)
    2: air_temperature / (K)               (time: 1200; latitude: 144; longitude: 192)
    3: air_temperature / (K)               (time: 1200; latitude: 144; longitude: 192)
    4: air_temperature / (K)               (time: 1200; latitude: 144; longitude: 192)



We can also access individual cubes in the dataset through an index with
``dataset.cube_dataset[index]``:

.. code:: ipython3

    print(dataset.cube_dataset[0])


.. parsed-literal::

    air_temperature / (K)               (time: 1200; latitude: 144; longitude: 192)
         Dimension coordinates:
              time                           x               -               -
              latitude                       -               x               -
              longitude                      -               -               x
         Scalar coordinates:
              height: 1.5 m
         Attributes:
              Conventions: CF-1.7 CMIP-6.2
              activity_id: CMIP
              branch_method: standard
              branch_time_in_child: 0.0
              branch_time_in_parent: 267840.0
              cmor_version: 3.4.0
              comment: minimum near-surface (usually, 2 meter) air temperature (add cell_method...
              cv_version: 6.2.20.1
              data_specs_version: 01.00.29
              experiment: pre-industrial control
              experiment_id: piControl
              external_variables: areacella
              forcing_index: 1
              frequency: mon
              further_info_url: https://furtherinfo.es-doc.org/CMIP6.MOHC.HadGEM3-GC31-LL.piControl.no...
              grid: Native N96 grid; 192 x 144 longitude/latitude
              grid_label: gn
              initialization_index: 1
              institution: Met Office Hadley Centre, Fitzroy Road, Exeter, Devon, EX1 3PB, UK
              institution_id: MOHC
              license: CMIP6 model data produced by the Met Office Hadley Centre is licensed under...
              mip_era: CMIP6
              mo_runid: u-ar766
              nominal_resolution: 250 km
              original_name: mo: mon_mean_from_day((stash: m01s03i236, lbproc: 4096))
              parent_activity_id: CMIP
              parent_experiment_id: piControl-spinup
              parent_mip_era: CMIP6
              parent_source_id: HadGEM3-GC31-LL
              parent_time_units: days since 1850-01-01-00-00-00
              parent_variant_label: r1i1p1f1
              physics_index: 1
              product: model-output
              realization_index: 1
              realm: atmos
              source: HadGEM3-GC31-LL (2016): 
    aerosol: UKCA-GLOMAP-mode
    atmos: MetUM-HadGEM3-GA7.1...
              source_id: HadGEM3-GC31-LL
              source_type: AOGCM AER
              sub_experiment: none
              sub_experiment_id: none
              table_id: Amon
              table_info: Creation Date:(13 December 2018) MD5:2b12b5db6db112aa8b8b0d6c1645b121
              title: HadGEM3-GC31-LL output prepared for CMIP6
              variable_id: tasmin
              variant_label: r1i1p1f1
         Cell methods:
              mean: area
              minimum within days: time
              mean over days: time


Should the equalise function not work there is a function to completely
remove all attributes, demonstrated below:

.. code:: ipython3

    dataset.remove_attributes()
    print(dataset.cube_dataset[0])


.. parsed-literal::

    air_temperature / (K)               (time: 1200; latitude: 144; longitude: 192)
         Dimension coordinates:
              time                           x               -               -
              latitude                       -               x               -
              longitude                      -               -               x
         Scalar coordinates:
              height: 1.5 m
         Attributes:
              Conventions: 
              activity_id: 
              branch_method: 
              branch_time_in_child: 
              branch_time_in_parent: 
              cmor_version: 
              comment: 
              cv_version: 
              data_specs_version: 
              experiment: 
              experiment_id: 
              external_variables: 
              forcing_index: 
              frequency: 
              further_info_url: 
              grid: 
              grid_label: 
              initialization_index: 
              institution: 
              institution_id: 
              license: 
              mip_era: 
              mo_runid: 
              nominal_resolution: 
              original_name: 
              parent_activity_id: 
              parent_experiment_id: 
              parent_mip_era: 
              parent_source_id: 
              parent_time_units: 
              parent_variant_label: 
              physics_index: 
              product: 
              realization_index: 
              realm: 
              source: 
              source_id: 
              source_type: 
              sub_experiment: 
              sub_experiment_id: 
              table_id: 
              table_info: 
              title: 
              variable_id: 
              variant_label: 
         Cell methods:
              mean: area
              minimum within days: time
              mean over days: time


Functions can also be used to collapse a given dimension, below we can
see the ``time`` dimension being collapsed with a mean average (further
ways to collapse data sets such as over time periods and seasons etc.
will be added in later releases):

.. code:: ipython3

    dataset.collapsed_dimension('time')
    dataset




.. parsed-literal::

    0: air_temperature / (K)               (latitude: 144; longitude: 192)
    1: air_temperature / (K)               (latitude: 144; longitude: 192)
    2: air_temperature / (K)               (latitude: 144; longitude: 192)
    3: air_temperature / (K)               (latitude: 144; longitude: 192)
    4: air_temperature / (K)               (latitude: 144; longitude: 192)



This shows some of cube_helper’s more basic methods, but we can do more
advanced stuff! This time, we will load some cubes with filenames rather
than a directory.

.. code:: ipython3

    import glob
    filenames = glob.glob('/net/home/h03/frpt/EC-EARTH_rcp85/*.nc')

Using this glob returns a list of cube filenames:

.. code:: ipython3

    filenames




.. parsed-literal::

    ['/net/home/h03/frpt/EC-EARTH_rcp85/tas_Amon_EC-EARTH_rcp85_r1i1p1_201001-201912.nc',
     '/net/home/h03/frpt/EC-EARTH_rcp85/tas_Amon_EC-EARTH_rcp85_r1i1p1_202001-202912.nc',
     '/net/home/h03/frpt/EC-EARTH_rcp85/tas_Amon_EC-EARTH_rcp85_r1i1p1_203001-203912.nc',
     '/net/home/h03/frpt/EC-EARTH_rcp85/tas_Amon_EC-EARTH_rcp85_r1i1p1_204001-204912.nc',
     '/net/home/h03/frpt/EC-EARTH_rcp85/tas_Amon_EC-EARTH_rcp85_r1i1p1_205001-205912.nc',
     '/net/home/h03/frpt/EC-EARTH_rcp85/tas_Amon_EC-EARTH_rcp85_r1i1p1_206001-206912.nc',
     '/net/home/h03/frpt/EC-EARTH_rcp85/tas_Amon_EC-EARTH_rcp85_r1i1p1_207001-207912.nc',
     '/net/home/h03/frpt/EC-EARTH_rcp85/tas_Amon_EC-EARTH_rcp85_r1i1p1_208001-208912.nc',
     '/net/home/h03/frpt/EC-EARTH_rcp85/tas_Amon_EC-EARTH_rcp85_r1i1p1_209001-209912.nc']



These can be loaded into CubeHelp by simply calling:

.. code:: ipython3

    dataset = CubeHelp(filenames)
    dataset




.. parsed-literal::

    0: air_temperature / (K)               (time: 120; latitude: 160; longitude: 320)
    1: air_temperature / (K)               (time: 120; latitude: 160; longitude: 320)
    2: air_temperature / (K)               (time: 120; latitude: 160; longitude: 320)
    3: air_temperature / (K)               (time: 120; latitude: 160; longitude: 320)
    4: air_temperature / (K)               (time: 120; latitude: 160; longitude: 320)
    5: air_temperature / (K)               (time: 120; latitude: 160; longitude: 320)
    6: air_temperature / (K)               (time: 120; latitude: 160; longitude: 320)
    7: air_temperature / (K)               (time: 120; latitude: 160; longitude: 320)
    8: air_temperature / (K)               (time: 120; latitude: 160; longitude: 320)



Here we see a new dataset loaded, we can currently apply some
constraints by first defining the constraints as follows:

.. code:: ipython3

    future_constraint = iris.Constraint(clim_season = 'jja', season_year=lambda cell:  cell >= 2010 and cell <=2060)

We then equalise the cube as before, however this time we will use the
``concatenate_cube()`` method as opposed to the ``get_concatenate_cube``
method. This concatenates the dataset rather than returning a
concatenated dataset, as shown:

.. code:: ipython3

    print(dataset.get_concatenated_cube())


.. parsed-literal::

    air_temperature / (K)               (time: 1080; latitude: 160; longitude: 320)
         Dimension coordinates:
              time                           x               -               -
              latitude                       -               x               -
              longitude                      -               -               x
         Attributes:
              CDI: Climate Data Interface version 1.4.4 (http://code.zmaw.de/projects/cdi...
              CDO: Climate Data Operators version 1.4.4 (http://code.zmaw.de/projects/cdo...
              Conventions: CF-1.4
              associated_files: baseURL: http://cmip-pcmdi.llnl.gov/CMIP5/dataLocation gridspecFile: gridspec_atmos_fx_EC-EARTH_rcp85_r0i0p0.nc...
              branch_time: 2281.0
              cmor_version: 2.8.0
              comment: Equilibrium reached after preindustrial spin-up after which data were output...
              contact: Alastair McKinstry <alastair.mckinstry@ichec.ie>
              experiment: RCP8.5
              experiment_id: rcp85
              forcing: Nat,Ant
              frequency: mon
              grid_type: gaussian
              initialization_method: 1
              institute_id: ICHEC
              institution: EC-Earth (European Earth System Model)
              model_id: EC-EARTH
              modeling_realm: atmos
              original_name: 2T
              parent_experiment: historical
              parent_experiment_id: historical
              parent_experiment_rip: r1i1p1
              physics_version: 1
              product: output
              project_id: CMIP5
              realization: 1
              references: Model described by Hazeleger et al. (Bull. Amer. Meteor. Soc., 2010, 91,...
              table_id: Table Amon (26 July 2011) b26379e76858ab98b927917878a63d01
              title: EC-EARTH model output prepared for CMIP5 RCP8.5
         Cell methods:
              mean: time (3 hours)


.. code:: ipython3

    dataset




.. parsed-literal::

    0: air_temperature / (K)               (time: 120; latitude: 160; longitude: 320)
    1: air_temperature / (K)               (time: 120; latitude: 160; longitude: 320)
    2: air_temperature / (K)               (time: 120; latitude: 160; longitude: 320)
    3: air_temperature / (K)               (time: 120; latitude: 160; longitude: 320)
    4: air_temperature / (K)               (time: 120; latitude: 160; longitude: 320)
    5: air_temperature / (K)               (time: 120; latitude: 160; longitude: 320)
    6: air_temperature / (K)               (time: 120; latitude: 160; longitude: 320)
    7: air_temperature / (K)               (time: 120; latitude: 160; longitude: 320)
    8: air_temperature / (K)               (time: 120; latitude: 160; longitude: 320)



Here we see that using ``get_concatenated_cube()`` does not alter the
dataset, it just returns a concatenated version of it. However, when we
use ``concatenate_cube()`` we get…

.. code:: ipython3

    dataset.concatenate_cube()
    dataset


.. parsed-literal::

    air_temperature / (K)               (time: 1080; latitude: 160; longitude: 320)
         Dimension coordinates:
              time                           x               -               -
              latitude                       -               x               -
              longitude                      -               -               x
         Attributes:
              CDI: Climate Data Interface version 1.4.4 (http://code.zmaw.de/projects/cdi...
              CDO: Climate Data Operators version 1.4.4 (http://code.zmaw.de/projects/cdo...
              Conventions: CF-1.4
              associated_files: baseURL: http://cmip-pcmdi.llnl.gov/CMIP5/dataLocation gridspecFile: gridspec_atmos_fx_EC-EARTH_rcp85_r0i0p0.nc...
              branch_time: 2281.0
              cmor_version: 2.8.0
              comment: Equilibrium reached after preindustrial spin-up after which data were output...
              contact: Alastair McKinstry <alastair.mckinstry@ichec.ie>
              experiment: RCP8.5
              experiment_id: rcp85
              forcing: Nat,Ant
              frequency: mon
              grid_type: gaussian
              initialization_method: 1
              institute_id: ICHEC
              institution: EC-Earth (European Earth System Model)
              model_id: EC-EARTH
              modeling_realm: atmos
              original_name: 2T
              parent_experiment: historical
              parent_experiment_id: historical
              parent_experiment_rip: r1i1p1
              physics_version: 1
              product: output
              project_id: CMIP5
              realization: 1
              references: Model described by Hazeleger et al. (Bull. Amer. Meteor. Soc., 2010, 91,...
              table_id: Table Amon (26 July 2011) b26379e76858ab98b927917878a63d01
              title: EC-EARTH model output prepared for CMIP5 RCP8.5
         Cell methods:
              mean: time (3 hours)




.. parsed-literal::

    



Now we can try and extract some data based on our specified constraints,
note that clim_season and season year are not auxillary coordinates.
This will not work, as Iris will conclude that NONE of the data falls
into these catergories, and remove ALL cubes from ``cube_dataset``:

.. code:: ipython3

    dataset.extract(future_constraint)
    dataset




.. parsed-literal::

    < No cubes >



So let’s try that again. This time we will add time catergoricals.

.. code:: ipython3

    dataset = CubeHelp('/project/champ/data/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/piControl/r1i1p1f1/Amon/tasmin/gn/v20190628')
    dataset.concatenate_cube()


.. parsed-literal::

    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))


Here we see no clim_season or season_year Auxillary coordinates:

.. code:: ipython3

    print(dataset.cube_dataset[0])


.. parsed-literal::

    air_temperature / (K)               (time: 6000; latitude: 144; longitude: 192)
         Dimension coordinates:
              time                           x               -               -
              latitude                       -               x               -
              longitude                      -               -               x
         Scalar coordinates:
              height: 1.5 m
         Attributes:
              Conventions: CF-1.7 CMIP-6.2
              activity_id: CMIP
              branch_method: standard
              branch_time_in_child: 0.0
              branch_time_in_parent: 267840.0
              cmor_version: 3.4.0
              comment: minimum near-surface (usually, 2 meter) air temperature (add cell_method...
              cv_version: 6.2.20.1
              data_specs_version: 01.00.29
              experiment: pre-industrial control
              experiment_id: piControl
              external_variables: areacella
              forcing_index: 1
              frequency: mon
              further_info_url: https://furtherinfo.es-doc.org/CMIP6.MOHC.HadGEM3-GC31-LL.piControl.no...
              grid: Native N96 grid; 192 x 144 longitude/latitude
              grid_label: gn
              initialization_index: 1
              institution: Met Office Hadley Centre, Fitzroy Road, Exeter, Devon, EX1 3PB, UK
              institution_id: MOHC
              license: CMIP6 model data produced by the Met Office Hadley Centre is licensed under...
              mip_era: CMIP6
              mo_runid: u-ar766
              nominal_resolution: 250 km
              original_name: mo: mon_mean_from_day((stash: m01s03i236, lbproc: 4096))
              parent_activity_id: CMIP
              parent_experiment_id: piControl-spinup
              parent_mip_era: CMIP6
              parent_source_id: HadGEM3-GC31-LL
              parent_time_units: days since 1850-01-01-00-00-00
              parent_variant_label: r1i1p1f1
              physics_index: 1
              product: model-output
              realization_index: 1
              realm: atmos
              source: HadGEM3-GC31-LL (2016): 
    aerosol: UKCA-GLOMAP-mode
    atmos: MetUM-HadGEM3-GA7.1...
              source_id: HadGEM3-GC31-LL
              source_type: AOGCM AER
              sub_experiment: none
              sub_experiment_id: none
              table_id: Amon
              table_info: Creation Date:(13 December 2018) MD5:2b12b5db6db112aa8b8b0d6c1645b121
              title: HadGEM3-GC31-LL output prepared for CMIP6
              variable_id: tasmin
              variant_label: r1i1p1f1
         Cell methods:
              mean: area
              minimum within days: time
              mean over days: time


However we can add these with the following commands:

.. code:: ipython3

    dataset.add_time_catergorical('season_year')
    dataset.add_time_catergorical('clim_season')
    print(dataset.cube_dataset[0])


.. parsed-literal::

    air_temperature / (K)               (time: 6000; latitude: 144; longitude: 192)
         Dimension coordinates:
              time                           x               -               -
              latitude                       -               x               -
              longitude                      -               -               x
         Auxiliary coordinates:
              clim_season                    x               -               -
              season_year                    x               -               -
         Scalar coordinates:
              height: 1.5 m
         Attributes:
              Conventions: CF-1.7 CMIP-6.2
              activity_id: CMIP
              branch_method: standard
              branch_time_in_child: 0.0
              branch_time_in_parent: 267840.0
              cmor_version: 3.4.0
              comment: minimum near-surface (usually, 2 meter) air temperature (add cell_method...
              cv_version: 6.2.20.1
              data_specs_version: 01.00.29
              experiment: pre-industrial control
              experiment_id: piControl
              external_variables: areacella
              forcing_index: 1
              frequency: mon
              further_info_url: https://furtherinfo.es-doc.org/CMIP6.MOHC.HadGEM3-GC31-LL.piControl.no...
              grid: Native N96 grid; 192 x 144 longitude/latitude
              grid_label: gn
              initialization_index: 1
              institution: Met Office Hadley Centre, Fitzroy Road, Exeter, Devon, EX1 3PB, UK
              institution_id: MOHC
              license: CMIP6 model data produced by the Met Office Hadley Centre is licensed under...
              mip_era: CMIP6
              mo_runid: u-ar766
              nominal_resolution: 250 km
              original_name: mo: mon_mean_from_day((stash: m01s03i236, lbproc: 4096))
              parent_activity_id: CMIP
              parent_experiment_id: piControl-spinup
              parent_mip_era: CMIP6
              parent_source_id: HadGEM3-GC31-LL
              parent_time_units: days since 1850-01-01-00-00-00
              parent_variant_label: r1i1p1f1
              physics_index: 1
              product: model-output
              realization_index: 1
              realm: atmos
              source: HadGEM3-GC31-LL (2016): 
    aerosol: UKCA-GLOMAP-mode
    atmos: MetUM-HadGEM3-GA7.1...
              source_id: HadGEM3-GC31-LL
              source_type: AOGCM AER
              sub_experiment: none
              sub_experiment_id: none
              table_id: Amon
              table_info: Creation Date:(13 December 2018) MD5:2b12b5db6db112aa8b8b0d6c1645b121
              title: HadGEM3-GC31-LL output prepared for CMIP6
              variable_id: tasmin
              variant_label: r1i1p1f1
         Cell methods:
              mean: area
              minimum within days: time
              mean over days: time


Now it’s been added we can safely filter data based on constraints:

.. code:: ipython3

    dataset.extract(future_constraint)

.. code:: ipython3

    print(dataset.cube_dataset[0])


.. parsed-literal::

    air_temperature / (K)               (time: 153; latitude: 144; longitude: 192)
         Dimension coordinates:
              time                           x              -               -
              latitude                       -              x               -
              longitude                      -              -               x
         Auxiliary coordinates:
              clim_season                    x              -               -
              season_year                    x              -               -
         Scalar coordinates:
              height: 1.5 m
         Attributes:
              Conventions: CF-1.7 CMIP-6.2
              activity_id: CMIP
              branch_method: standard
              branch_time_in_child: 0.0
              branch_time_in_parent: 267840.0
              cmor_version: 3.4.0
              comment: minimum near-surface (usually, 2 meter) air temperature (add cell_method...
              cv_version: 6.2.20.1
              data_specs_version: 01.00.29
              experiment: pre-industrial control
              experiment_id: piControl
              external_variables: areacella
              forcing_index: 1
              frequency: mon
              further_info_url: https://furtherinfo.es-doc.org/CMIP6.MOHC.HadGEM3-GC31-LL.piControl.no...
              grid: Native N96 grid; 192 x 144 longitude/latitude
              grid_label: gn
              initialization_index: 1
              institution: Met Office Hadley Centre, Fitzroy Road, Exeter, Devon, EX1 3PB, UK
              institution_id: MOHC
              license: CMIP6 model data produced by the Met Office Hadley Centre is licensed under...
              mip_era: CMIP6
              mo_runid: u-ar766
              nominal_resolution: 250 km
              original_name: mo: mon_mean_from_day((stash: m01s03i236, lbproc: 4096))
              parent_activity_id: CMIP
              parent_experiment_id: piControl-spinup
              parent_mip_era: CMIP6
              parent_source_id: HadGEM3-GC31-LL
              parent_time_units: days since 1850-01-01-00-00-00
              parent_variant_label: r1i1p1f1
              physics_index: 1
              product: model-output
              realization_index: 1
              realm: atmos
              source: HadGEM3-GC31-LL (2016): 
    aerosol: UKCA-GLOMAP-mode
    atmos: MetUM-HadGEM3-GA7.1...
              source_id: HadGEM3-GC31-LL
              source_type: AOGCM AER
              sub_experiment: none
              sub_experiment_id: none
              table_id: Amon
              table_info: Creation Date:(13 December 2018) MD5:2b12b5db6db112aa8b8b0d6c1645b121
              title: HadGEM3-GC31-LL output prepared for CMIP6
              variable_id: tasmin
              variant_label: r1i1p1f1
         Cell methods:
              mean: area
              minimum within days: time
              mean over days: time


.. code:: ipython3

    dataset


.. parsed-literal::

    air_temperature / (K)               (time: 153; latitude: 144; longitude: 192)
         Dimension coordinates:
              time                           x              -               -
              latitude                       -              x               -
              longitude                      -              -               x
         Auxiliary coordinates:
              clim_season                    x              -               -
              season_year                    x              -               -
         Scalar coordinates:
              height: 1.5 m
         Attributes:
              Conventions: CF-1.7 CMIP-6.2
              activity_id: CMIP
              branch_method: standard
              branch_time_in_child: 0.0
              branch_time_in_parent: 267840.0
              cmor_version: 3.4.0
              comment: minimum near-surface (usually, 2 meter) air temperature (add cell_method...
              cv_version: 6.2.20.1
              data_specs_version: 01.00.29
              experiment: pre-industrial control
              experiment_id: piControl
              external_variables: areacella
              forcing_index: 1
              frequency: mon
              further_info_url: https://furtherinfo.es-doc.org/CMIP6.MOHC.HadGEM3-GC31-LL.piControl.no...
              grid: Native N96 grid; 192 x 144 longitude/latitude
              grid_label: gn
              initialization_index: 1
              institution: Met Office Hadley Centre, Fitzroy Road, Exeter, Devon, EX1 3PB, UK
              institution_id: MOHC
              license: CMIP6 model data produced by the Met Office Hadley Centre is licensed under...
              mip_era: CMIP6
              mo_runid: u-ar766
              nominal_resolution: 250 km
              original_name: mo: mon_mean_from_day((stash: m01s03i236, lbproc: 4096))
              parent_activity_id: CMIP
              parent_experiment_id: piControl-spinup
              parent_mip_era: CMIP6
              parent_source_id: HadGEM3-GC31-LL
              parent_time_units: days since 1850-01-01-00-00-00
              parent_variant_label: r1i1p1f1
              physics_index: 1
              product: model-output
              realization_index: 1
              realm: atmos
              source: HadGEM3-GC31-LL (2016): 
    aerosol: UKCA-GLOMAP-mode
    atmos: MetUM-HadGEM3-GA7.1...
              source_id: HadGEM3-GC31-LL
              source_type: AOGCM AER
              sub_experiment: none
              sub_experiment_id: none
              table_id: Amon
              table_info: Creation Date:(13 December 2018) MD5:2b12b5db6db112aa8b8b0d6c1645b121
              title: HadGEM3-GC31-LL output prepared for CMIP6
              variable_id: tasmin
              variant_label: r1i1p1f1
         Cell methods:
              mean: area
              minimum within days: time
              mean over days: time




.. parsed-literal::

    


