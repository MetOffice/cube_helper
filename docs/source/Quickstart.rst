Quickstart
==========

A quick starting guide to get you using ``cube_helper`` in a matter of minutes.

Loading a cube
^^^^^^^^^^^^^^
To load a cube from a directory of netCDF files:

.. code-block:: python

   >>> import cube_helper as ch
   >>> cube = ch.load('/path/to/cmip/data/HadGEM3-GC31-LL/piControl/r1i1p1f1/Amon/tasmin/gn/v20190628')

Loading a cube with constraints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

   >>> import iris
   >>> longitude_constraint = iris.Constraint(longitude = lambda cell : cell > 0 and cell < 180)
   >>> cube = ch.load('/path/to/cmip/data/HadGEM3-GC31-LL/piControl/r1i1p1f1/Amon/tasmin/gn/v20190628', constraints=longitude_constraint)

Loading a cube from a list of files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To load from a list of fname strings. Useful when combining datasets.

.. code-block:: python

   >>> from glob import glob
   >>> fnames = glob('/path/to/cmip/data/output1/ICHEC/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/v20131231/tas/*.nc')
   >>> cube = ch.load(fnames)

Concatenating a cube
^^^^^^^^^^^^^^^^^^^^
If you are dealing with cubes that have already been loaded, for CubeLists and list of loaded cubes.

.. code-block:: python

   >>> cubes
   [<iris 'Cube' of air_temperature / (K) (time: 1200; latitude: 144; longitude: 192)>,
   <iris 'Cube' of air_temperature / (K) (time: 1200; latitude: 144; longitude: 192)>,
   <iris 'Cube' of air_temperature / (K) (time: 1200; latitude: 144; longitude: 192)>,
   <iris 'Cube' of air_temperature / (K) (time: 1200; latitude: 144; longitude: 192)>,
   <iris 'Cube' of air_temperature / (K) (time: 1200; latitude: 144; longitude: 192)>]

   >>> cube = ch.concatenate(cubes)
   Deleting history, creation_date, and tracking_id attributes from cubes


   >>> cube
   <iris 'Cube' of air_temperature / (K) (time: 6000; latitude: 144; longitude: 192)>

Adding a categorical to a cube
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Add a categorical coordinate to an iterable of iris cubes or a standalone cube.

.. code-block:: python

   >>> cube
   <iris 'Cube' of air_temperature / (K) (time: 1919; latitude: 160; longitude: 320)>
   >>> cube = ch.add_categorical(cube, 'clim_season')
   >>> print(cube)
   air_temperature / (K)               (time: 1919; latitude: 160; longitude: 320)
        Dimension coordinates:
             time                           x               -               -
             latitude                       -               x               -
             longitude                      -               -               x
        Auxiliary coordinates:
             clim_season                    x               -               -
        Attributes:
             CDI: Climate Data Interface version 1.4.4 (http://code.zmaw.de/projects/cdi...
             CDO: Climate Data Operators version 1.4.4 (http://code.zmaw.de/projects/cdo...
             Conventions: CF-1.4
             associated_files: baseURL: http://cmip-pcmdi.llnl.gov/CMIP5/dataLocation gridspecFile: gridspec_atmos_fx_EC-EARTH_historical_r0i0p0.nc...
             branch_time: 2125.0
             cmor_version: 2.8.0
             comment: Equilibrium reached after preindustrial spin-up after which data were output...
             contact: Alastair McKinstry <alastair.mckinstry@ichec.ie>
             experiment: historical
             experiment_id: historical
             forcing: Nat,Ant
             frequency: mon
             grid_type: gaussian
             initialization_method: 1
             institute_id: ICHEC
             institution: EC-Earth (European Earth System Model)
             model_id: EC-EARTH
             modeling_realm: atmos
             original_name: 2T
             parent_experiment: pre-industrial control
             parent_experiment_id: piControl
             parent_experiment_rip: r1i1p1
             physics_version: 1
             product: output
             project_id: CMIP5
             realization: 1
             references: Model described by Hazeleger et al. (Bull. Amer. Meteor. Soc., 2010, 91,...
             table_id: Table Amon (26 July 2011) b26379e76858ab98b927917878a63d01
             title: EC-EARTH model output prepared for CMIP5 historical
        Cell methods:
             mean: time (3 hours)

Adding multiple categoricals to a cube
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

   >>> cube
   <iris 'Cube' of air_temperature / (K) (time: 1919; latitude: 160; longitude: 320)>
   >>> cube = ch.add_categorical(cube, ['clim_season', 'season_year'])
   >>> print(cube)
   air_temperature / (K)               (time: 1919; latitude: 160; longitude: 320)
        Dimension coordinates:
             time                           x               -               -
             latitude                       -               x               -
             longitude                      -               -               x
        Auxiliary coordinates:
             clim_season                    x               -               -
             season_year                    x               -               -
        Attributes:
             CDI: Climate Data Interface version 1.4.4 (http://code.zmaw.de/projects/cdi...
             CDO: Climate Data Operators version 1.4.4 (http://code.zmaw.de/projects/cdo...
             Conventions: CF-1.4
             associated_files: baseURL: http://cmip-pcmdi.llnl.gov/CMIP5/dataLocation gridspecFile: gridspec_atmos_fx_EC-EARTH_historical_r0i0p0.nc...
             branch_time: 2125.0
             cmor_version: 2.8.0
             comment: Equilibrium reached after preindustrial spin-up after which data were output...
             contact: Alastair McKinstry <alastair.mckinstry@ichec.ie>
             experiment: historical
             experiment_id: historical
             forcing: Nat,Ant
             frequency: mon
             grid_type: gaussian
             initialization_method: 1
             institute_id: ICHEC
             institution: EC-Earth (European Earth System Model)
             model_id: EC-EARTH
             modeling_realm: atmos
             original_name: 2T
             parent_experiment: pre-industrial control
             parent_experiment_id: piControl
             parent_experiment_rip: r1i1p1
             physics_version: 1
             product: output
             project_id: CMIP5
             realization: 1
             references: Model described by Hazeleger et al. (Bull. Amer. Meteor. Soc., 2010, 91,...
             table_id: Table Amon (26 July 2011) b26379e76858ab98b927917878a63d01
             title: EC-EARTH model output prepared for CMIP5 historical
        Cell methods:
             mean: time (3 hours)

Adding a compound categorical to a cube
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If the categoricals you are adding are part of a compound categorical, you can use special calls such as:

.. code-block:: python

   >>> cube
   <iris 'Cube' of air_temperature / (K) (time: 1919; latitude: 160; longitude: 320)>
   >>> annual_seasonal_mean = ch.add_categorical(cube, 'annual_seasonal_mean')
   >>> print(annual_seasonal_mean)
   air_temperature / (K)               (time: 1919; latitude: 160; longitude: 320)
        Dimension coordinates:
             time                           x               -               -
             latitude                       -               x               -
             longitude                      -               -               x
        Auxiliary coordinates:
             clim_season                    x               -               -
             season_year                    x               -               -
        Attributes:
             CDI: Climate Data Interface version 1.4.4 (http://code.zmaw.de/projects/cdi...
             CDO: Climate Data Operators version 1.4.4 (http://code.zmaw.de/projects/cdo...
             Conventions: CF-1.4
             associated_files: baseURL: http://cmip-pcmdi.llnl.gov/CMIP5/dataLocation gridspecFile: gridspec_atmos_fx_EC-EARTH_historical_r0i0p0.nc...
             branch_time: 2125.0
             cmor_version: 2.8.0
             comment: Equilibrium reached after preindustrial spin-up after which data were output...
             contact: Alastair McKinstry <alastair.mckinstry@ichec.ie>
             experiment: historical
             experiment_id: historical
             forcing: Nat,Ant
             frequency: mon
             grid_type: gaussian
             initialization_method: 1
             institute_id: ICHEC
             institution: EC-Earth (European Earth System Model)
             model_id: EC-EARTH
             modeling_realm: atmos
             original_name: 2T
             parent_experiment: pre-industrial control
             parent_experiment_id: piControl
             parent_experiment_rip: r1i1p1
             physics_version: 1
             product: output
             project_id: CMIP5
             realization: 1
             references: Model described by Hazeleger et al. (Bull. Amer. Meteor. Soc., 2010, 91,...
             table_id: Table Amon (26 July 2011) b26379e76858ab98b927917878a63d01
             title: EC-EARTH model output prepared for CMIP5 historical
        Cell methods:
             mean: time (3 hours)

Aggregating by categoricals
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Returns an aggregated cube.

.. code-block:: python

   >>> cube
   <iris 'Cube' of air_temperature / (K) (time: 1919; latitude: 160; longitude: 320)>
   >>> cube = ch.aggregate_categorical(cube, 'clim_season')
   >>> print(cube)
   air_temperature / (K)               (time: 4; latitude: 160; longitude: 320)
        Dimension coordinates:
             time                           x            -               -
             latitude                       -            x               -
             longitude                      -            -               x
        Auxiliary coordinates:
             clim_season                    x            -               -
        Attributes:
             CDI: Climate Data Interface version 1.4.4 (http://code.zmaw.de/projects/cdi...
             CDO: Climate Data Operators version 1.4.4 (http://code.zmaw.de/projects/cdo...
             Conventions: CF-1.4
             associated_files: baseURL: http://cmip-pcmdi.llnl.gov/CMIP5/dataLocation gridspecFile: gridspec_atmos_fx_EC-EARTH_historical_r0i0p0.nc...
             branch_time: 2125.0
             cmor_version: 2.8.0
             comment: Equilibrium reached after preindustrial spin-up after which data were output...
             contact: Alastair McKinstry <alastair.mckinstry@ichec.ie>
             experiment: historical
             experiment_id: historical
             forcing: Nat,Ant
             frequency: mon
             grid_type: gaussian
             initialization_method: 1
             institute_id: ICHEC
             institution: EC-Earth (European Earth System Model)
             model_id: EC-EARTH
             modeling_realm: atmos
             original_name: 2T
             parent_experiment: pre-industrial control
             parent_experiment_id: piControl
             parent_experiment_rip: r1i1p1
             physics_version: 1
             product: output
             project_id: CMIP5
            realization: 1
             references: Model described by Hazeleger et al. (Bull. Amer. Meteor. Soc., 2010, 91,...
             table_id: Table Amon (26 July 2011) b26379e76858ab98b927917878a63d01
             title: EC-EARTH model output prepared for CMIP5 historical
        Cell methods:
             mean: time (3 hours)
             mean: clim_season

Extracting categoricals
^^^^^^^^^^^^^^^^^^^^^^^
Aggregates and extracts with a given constraint.

.. code-block:: python

   >>> cube
   <iris 'Cube' of air_temperature / (K) (time: 1919; latitude: 160; longitude: 320)>
   >>> tdelta_3mth = datetime.timedelta(hours=3*28*24.0)
   >>> spans_three_months = lambda t: (t.bound[1] - t.bound[0]) > tdelta_3mth
   >>> three_months_bound = iris.Constraint(time=spans_three_months)
   >>> annual_seasonal_mean = ch.extract_categorical(cube, 'annual_seasonal_mean', three_months_bound)
   >>> annual_seasonal_mean
   <iris 'Cube' of air_temperature / (K) (time: 639; latitude: 160; longitude: 320)>

