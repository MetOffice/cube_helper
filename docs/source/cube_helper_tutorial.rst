
cube_helper Tutorial
--------------------

This tutorial is a step by step guide to using the ``cube_helper``
module. ``cube_helper`` is useful for concatenating, comparing, and
equalising cubes in large datasets. ``cube_helper`` is designed to give
a certain degree of abstraction to the user from issues in iris cube
meta-data and coordinate information. Start by pointing your python
Environment to the new ``cube_helper`` module:

.. code:: ipython3

    !export PYTHONPATH=/net/home/h01/jbedwell/Downloads/cube_helper

Next, import the new ``cube_helper`` methods.

.. code:: ipython3

    import cube_helper as ch

``load`` will load data into a single cube by ignoring certain
attributes and meta-data that causes common problems with concatenation.
Here we load a HadGem3 model, and ``load`` takes care of the rest:

.. code:: ipython3

    cube = ch.load('/project/champ/data/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/piControl/r1i1p1f1/Amon/tasmin/gn/v20190628')


.. parsed-literal::

    /opt/scitools/environments/default/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/default/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/default/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/default/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/default/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/default/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/default/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/default/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))


.. parsed-literal::

    
    cube dim coordinates differ: 
    
    	latitude coords inconsistent
    
    	longitude coords inconsistent
    
    cube attributes differ: 
    
    	creation_date attribute inconsistent
    
    	history attribute inconsistent
    
    	tracking_id attribute inconsistent
    
    Deleting creation_date attribute from cubes
    
    Deleting history attribute from cubes
    
    Deleting tracking_id attribute from cubes
    
    New time origin set to days since 1850-01-01
    
    New time calender set to 360_day
    


.. parsed-literal::

    /opt/scitools/environments/default/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/default/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))


Here we see some output describing the process it’s gong through. The
first statement states the attributes differ, it therefor deletes the
uncommon attributes across the cubes. This then returns a concatenated
iris cube:

.. code:: ipython3

    print(cube)


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


``cube_helper`` can also still load from a list of files:

.. code:: ipython3

    import glob
    filenames = glob.glob('/net/home/h03/frpt/EC-EARTH_rcp85/*.nc')
    filenames_2 = glob.glob('/project/champ/data/cmip5/output1/ICHEC/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/v20131231/tas/*.nc')
    filenames.extend(filenames_2)

.. code:: ipython3

    cube = ch.load(filenames)


.. parsed-literal::

    
    cube dim coordinates differ: 
    
    	latitude coords inconsistent
    
    	longitude coords inconsistent
    
    	time coords inconsistent
    
    cube attributes differ: 
    
    	history attribute inconsistent
    
    	experiment_id attribute inconsistent
    
    	parent_experiment_id attribute inconsistent
    
    	branch_time attribute inconsistent
    
    	tracking_id attribute inconsistent
    
    	experiment attribute inconsistent
    
    	creation_date attribute inconsistent
    
    	title attribute inconsistent
    
    	parent_experiment attribute inconsistent
    
    	associated_files attribute inconsistent
    
    cube time coordinates differ: 
    
    	time start date inconsistent
    
    Deleting history attribute from cubes
    
    Deleting experiment_id attribute from cubes
    
    Deleting parent_experiment_id attribute from cubes
    
    Deleting branch_time attribute from cubes
    
    Deleting tracking_id attribute from cubes
    
    Deleting experiment attribute from cubes
    
    Deleting creation_date attribute from cubes
    
    Deleting title attribute from cubes
    
    Deleting parent_experiment attribute from cubes
    
    Deleting associated_files attribute from cubes
    
    New time origin set to days since 1850-01-01 00:00:00
    
    New time calender set to gregorian
    


Here we see even more messages regarding what changes have been made to
the cube, in particular the time units it’s been converted to. A
concatenated cube is returned which we can view:

.. code:: ipython3

    print(cube)


.. parsed-literal::

    air_temperature / (K)               (time: 2999; latitude: 160; longitude: 320)
         Dimension coordinates:
              time                           x               -               -
              latitude                       -               x               -
              longitude                      -               -               x
         Attributes:
              CDI: Climate Data Interface version 1.4.4 (http://code.zmaw.de/projects/cdi...
              CDO: Climate Data Operators version 1.4.4 (http://code.zmaw.de/projects/cdo...
              Conventions: CF-1.4
              cmor_version: 2.8.0
              comment: Equilibrium reached after preindustrial spin-up after which data were output...
              contact: Alastair McKinstry <alastair.mckinstry@ichec.ie>
              forcing: Nat,Ant
              frequency: mon
              grid_type: gaussian
              initialization_method: 1
              institute_id: ICHEC
              institution: EC-Earth (European Earth System Model)
              model_id: EC-EARTH
              modeling_realm: atmos
              original_name: 2T
              parent_experiment_rip: r1i1p1
              physics_version: 1
              product: output
              project_id: CMIP5
              realization: 1
              references: Model described by Hazeleger et al. (Bull. Amer. Meteor. Soc., 2010, 91,...
              table_id: Table Amon (26 July 2011) b26379e76858ab98b927917878a63d01
         Cell methods:
              mean: time (3 hours)


This version of ``cube_helper`` will try every possible action when
trying to concatenate a cube, when it runs into a problem that is best
to solve manually, it will print out a message. We can demonstrate this
using a historical and future dataset which were found to be
incompatible:

.. code:: ipython3

    filenames = glob.glob('/project/champ/data/cmip5/output1/ICHEC/EC-EARTH/rcp85/mon/atmos/Amon/r1i1p1/v20171115/tas/*.nc')
    filenames_2 = glob.glob('/project/champ/data/cmip5/output1/ICHEC/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/v20131231/tas/*.nc')
    filenames.extend(filenames_2)

.. code:: ipython3

    cube = ch.load(filenames)


.. parsed-literal::

    /opt/scitools/environments/default/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tas'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/default/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tas'
      warnings.warn(message % (variable_name, nc_var_name))


.. parsed-literal::

    
    cube aux coordinates differ: 
    
    	height coords inconsistent
    
    
    cube dim coordinates differ: 
    
    	latitude coords inconsistent
    
    	longitude coords inconsistent
    
    	time coords inconsistent
    
    cube attributes differ: 
    
    	CDI attribute inconsistent
    
    	history attribute inconsistent
    
    	experiment_id attribute inconsistent
    
    	parent_experiment_id attribute inconsistent
    
    	branch_time attribute inconsistent
    
    	tracking_id attribute inconsistent
    
    	experiment attribute inconsistent
    
    	creation_date attribute inconsistent
    
    	title attribute inconsistent
    
    	parent_experiment attribute inconsistent
    
    	CDO attribute inconsistent
    
    	associated_files attribute inconsistent
    
    	grid_type attribute inconsistent
    
    	source attribute inconsistent
    
    cube time coordinates differ: 
    
    	time start date inconsistent
    
    Removing height coords from cube
    
    Deleting CDI attribute from cubes
    
    Deleting history attribute from cubes
    
    Deleting experiment_id attribute from cubes
    
    Deleting parent_experiment_id attribute from cubes
    
    Deleting branch_time attribute from cubes
    
    Deleting tracking_id attribute from cubes
    
    Deleting experiment attribute from cubes
    
    Deleting creation_date attribute from cubes
    
    Deleting title attribute from cubes
    
    Deleting parent_experiment attribute from cubes
    
    Deleting CDO attribute from cubes
    
    Deleting associated_files attribute from cubes
    
    Deleting grid_type attribute from cubes
    
    Deleting source attribute from cubes
    
    New time origin set to days since 1850-01-01 00:00:00
    
    New time calender set to gregorian
    
    
    Oops, there was an error in concatenation
    
    
    The time coordinates overlap at cube 15 and cube 16
    
    These cubes are: 
    	/project/champ/data/cmip5/output1/ICHEC/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/v20131231/tas/tas_Amon_EC-EARTH_historical_r1i1p1_200001-200911.nc
    	/project/champ/data/cmip5/output1/ICHEC/EC-EARTH/rcp85/mon/atmos/Amon/r1i1p1/v20171115/tas/tas_Amon_EC-EARTH_rcp85_r1i1p1_200601-200912.nc
    
    The time coordinates overlap at cube 16 and cube 15
    
    These cubes are: 
    	/project/champ/data/cmip5/output1/ICHEC/EC-EARTH/rcp85/mon/atmos/Amon/r1i1p1/v20171115/tas/tas_Amon_EC-EARTH_rcp85_r1i1p1_200601-200912.nc
    	/project/champ/data/cmip5/output1/ICHEC/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/v20131231/tas/tas_Amon_EC-EARTH_historical_r1i1p1_200001-200911.nc


Here we see the time coordinates for cube 15 and 16 overlap, We can
therefore manually remove this from the list, and try again:

.. code:: ipython3

    filenames.remove('/project/champ/data/cmip5/output1/ICHEC/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/v20131231/tas/tas_Amon_EC-EARTH_historical_r1i1p1_200001-200911.nc')

And then we try to load it again:

.. code:: ipython3

    cube = ch.load(filenames)


.. parsed-literal::

    /opt/scitools/environments/default/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tas'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/default/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tas'
      warnings.warn(message % (variable_name, nc_var_name))


.. parsed-literal::

    
    cube aux coordinates differ: 
    
    	height coords inconsistent
    
    
    cube dim coordinates differ: 
    
    	latitude coords inconsistent
    
    	longitude coords inconsistent
    
    	time coords inconsistent
    
    cube attributes differ: 
    
    	CDI attribute inconsistent
    
    	history attribute inconsistent
    
    	experiment_id attribute inconsistent
    
    	parent_experiment_id attribute inconsistent
    
    	branch_time attribute inconsistent
    
    	tracking_id attribute inconsistent
    
    	experiment attribute inconsistent
    
    	creation_date attribute inconsistent
    
    	title attribute inconsistent
    
    	parent_experiment attribute inconsistent
    
    	CDO attribute inconsistent
    
    	associated_files attribute inconsistent
    
    	grid_type attribute inconsistent
    
    	source attribute inconsistent
    
    cube time coordinates differ: 
    
    	time start date inconsistent
    
    Removing height coords from cube
    
    Deleting CDI attribute from cubes
    
    Deleting history attribute from cubes
    
    Deleting experiment_id attribute from cubes
    
    Deleting parent_experiment_id attribute from cubes
    
    Deleting branch_time attribute from cubes
    
    Deleting tracking_id attribute from cubes
    
    Deleting experiment attribute from cubes
    
    Deleting creation_date attribute from cubes
    
    Deleting title attribute from cubes
    
    Deleting parent_experiment attribute from cubes
    
    Deleting CDO attribute from cubes
    
    Deleting associated_files attribute from cubes
    
    Deleting grid_type attribute from cubes
    
    Deleting source attribute from cubes
    
    New time origin set to days since 1850-01-01 00:00:00
    
    New time calender set to gregorian
    


This now seems to have worked, Lets have a look:

.. code:: ipython3

    print(cube)


.. parsed-literal::

    air_temperature / (K)               (time: 2940; latitude: 160; longitude: 320)
         Dimension coordinates:
              time                           x               -               -
              latitude                       -               x               -
              longitude                      -               -               x
         Attributes:
              Conventions: CF-1.4
              cmor_version: 2.8.0
              comment: Equilibrium reached after preindustrial spin-up after which data were output...
              contact: Alastair McKinstry <alastair.mckinstry@ichec.ie>
              forcing: Nat,Ant
              frequency: mon
              initialization_method: 1
              institute_id: ICHEC
              institution: EC-Earth (European Earth System Model)
              model_id: EC-EARTH
              modeling_realm: atmos
              original_name: 2T
              parent_experiment_rip: r1i1p1
              physics_version: 1
              product: output
              project_id: CMIP5
              realization: 1
              references: Model described by Hazeleger et al. (Bull. Amer. Meteor. Soc., 2010, 91,...
              table_id: Table Amon (26 July 2011) b26379e76858ab98b927917878a63d01
         Cell methods:
              mean: time (3 hours)


Success!
