
Cube Helper: A Walkthrough guide
--------------------------------

This python module has been produced to mitigate the issues faced by
researchers whilst trying to manipulate multiple cubes.

The main class of interest for this module is the ``CubeHelp`` class. To
illustrate it’s usage, lets start by importing the module (and iris!)

.. code:: ipython3

    !export PYTHONPATH=/net/home/h01/jbedwell/Downloads/cube_helper

.. code:: ipython3

    import iris
    from cube_helper import CubeHelp

The ``CubeHelper`` object once instantiated loads the given dataset as
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
wraped iris ``concatenate_cube()`` function:

.. code:: ipython3

    dataset.get_concatenated_cube()


::


    ---------------------------------------------------------------------------

    ConcatenateError                          Traceback (most recent call last)

    <ipython-input-46-19eebc86616f> in <module>
    ----> 1 dataset.get_concatenated_cube()
    

    /net/home/h01/jbedwell/Downloads/cube_helper/cube_helper/cube_help.py in get_concatenated_cube(self)
        157             A concatenated Cube of the cube_dataset
        158         """
    --> 159         return self.cube_dataset.concatenate_cube()
        160 
        161     def get_merged_cube(self):


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

Here we can use the cube_helper function ``equalise()``, which cycles
through each cube, and removes attributes that are not uniform across
the dataset. Lets try it out:

.. code:: ipython3

    dataset.equalise()
    dataset.get_concatenated_cube()

As shown the function returns a concatenated cube after calling the
``equalise`` function. This functionality is not limited to equalising
and concatenating cubes. Functions are also provided for converting one
unit to another, below this is illustrated, with the argument
``'celsius'`` passed converting the dataset’s units:

.. code:: ipython3

    dataset.convert_units('celsius')
    print(dataset)

And back again into Kelvin (``'K'``)

.. code:: ipython3

    dataset.convert_units('K')
    print(dataset)

We can also access individual cubes in the dataset through an index with
``dataset.cube_dataset[index]``:

.. code:: ipython3

    dataset.cube_dataset[0]




.. raw:: html

    
    <style>
      a.iris {
          text-decoration: none !important;
      }
      table.iris {
          white-space: pre;
          border: 1px solid;
          border-color: #9c9c9c;
          font-family: monaco, monospace;
      }
      th.iris {
          background: #303f3f;
          color: #e0e0e0;
          border-left: 1px solid;
          border-color: #9c9c9c;
          font-size: 1.05em;
          min-width: 50px;
          max-width: 125px;
      }
      tr.iris :first-child {
          border-right: 1px solid #9c9c9c !important;
      }
      td.iris-title {
          background: #d5dcdf;
          border-top: 1px solid #9c9c9c;
          font-weight: bold;
      }
      .iris-word-cell {
          text-align: left !important;
          white-space: pre;
      }
      .iris-subheading-cell {
          padding-left: 2em !important;
      }
      .iris-inclusion-cell {
          padding-right: 1em !important;
      }
      .iris-panel-body {
          padding-top: 0px;
      }
      .iris-panel-title {
          padding-left: 3em;
      }
      .iris-panel-title {
          margin-top: 7px;
      }
    </style>
    <table class="iris" id="140068505525720">
        <tr class="iris">
    <th class="iris iris-word-cell">Air Temperature (K)</th>
    <th class="iris iris-word-cell">time</th>
    <th class="iris iris-word-cell">latitude</th>
    <th class="iris iris-word-cell">longitude</th>
    </tr>
        <tr class="iris">
    <td class="iris-word-cell iris-subheading-cell">Shape</td>
    <td class="iris iris-inclusion-cell">1200</td>
    <td class="iris iris-inclusion-cell">144</td>
    <td class="iris iris-inclusion-cell">192</td>
    </td>
        <tr class="iris">
        <td class="iris-title iris-word-cell">Dimension coordinates</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	time</td>
        <td class="iris-inclusion-cell">x</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">-</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	latitude</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">x</td>
        <td class="iris-inclusion-cell">-</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	longitude</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">x</td>
    </tr>
    <tr class="iris">
        <td class="iris-title iris-word-cell">Scalar coordinates</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	height</td>
        <td class="iris-word-cell" colspan="3">1.5 m</td>
    </tr>
    <tr class="iris">
        <td class="iris-title iris-word-cell">Attributes</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	Conventions</td>
        <td class="iris-word-cell" colspan="3">CF-1.7 CMIP-6.2</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	activity_id</td>
        <td class="iris-word-cell" colspan="3">CMIP</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	branch_method</td>
        <td class="iris-word-cell" colspan="3">standard</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	branch_time_in_child</td>
        <td class="iris-word-cell" colspan="3">0.0</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	branch_time_in_parent</td>
        <td class="iris-word-cell" colspan="3">267840.0</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	cmor_version</td>
        <td class="iris-word-cell" colspan="3">3.4.0</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	comment</td>
        <td class="iris-word-cell" colspan="3">minimum near-surface (usually, 2 meter) air temperature (add cell_method...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	creation_date</td>
        <td class="iris-word-cell" colspan="3">2019-06-25T23:09:47Z</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	cv_version</td>
        <td class="iris-word-cell" colspan="3">6.2.20.1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	data_specs_version</td>
        <td class="iris-word-cell" colspan="3">01.00.29</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	experiment</td>
        <td class="iris-word-cell" colspan="3">pre-industrial control</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	experiment_id</td>
        <td class="iris-word-cell" colspan="3">piControl</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	external_variables</td>
        <td class="iris-word-cell" colspan="3">areacella</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	forcing_index</td>
        <td class="iris-word-cell" colspan="3">1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	frequency</td>
        <td class="iris-word-cell" colspan="3">mon</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	further_info_url</td>
        <td class="iris-word-cell" colspan="3">https://furtherinfo.es-doc.org/CMIP6.MOHC.HadGEM3-GC31-LL.piControl.no...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	grid</td>
        <td class="iris-word-cell" colspan="3">Native N96 grid; 192 x 144 longitude/latitude</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	grid_label</td>
        <td class="iris-word-cell" colspan="3">gn</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	history</td>
        <td class="iris-word-cell" colspan="3">2019-06-25T23:09:47Z altered by CMOR: Treated scalar dimension: 'height'....</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	initialization_index</td>
        <td class="iris-word-cell" colspan="3">1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	institution</td>
        <td class="iris-word-cell" colspan="3">Met Office Hadley Centre, Fitzroy Road, Exeter, Devon, EX1 3PB, UK</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	institution_id</td>
        <td class="iris-word-cell" colspan="3">MOHC</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	license</td>
        <td class="iris-word-cell" colspan="3">CMIP6 model data produced by the Met Office Hadley Centre is licensed under...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	mip_era</td>
        <td class="iris-word-cell" colspan="3">CMIP6</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	mo_runid</td>
        <td class="iris-word-cell" colspan="3">u-ar766</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	nominal_resolution</td>
        <td class="iris-word-cell" colspan="3">250 km</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	original_name</td>
        <td class="iris-word-cell" colspan="3">mo: mon_mean_from_day((stash: m01s03i236, lbproc: 4096))</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_activity_id</td>
        <td class="iris-word-cell" colspan="3">CMIP</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_experiment_id</td>
        <td class="iris-word-cell" colspan="3">piControl-spinup</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_mip_era</td>
        <td class="iris-word-cell" colspan="3">CMIP6</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_source_id</td>
        <td class="iris-word-cell" colspan="3">HadGEM3-GC31-LL</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_time_units</td>
        <td class="iris-word-cell" colspan="3">days since 1850-01-01-00-00-00</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_variant_label</td>
        <td class="iris-word-cell" colspan="3">r1i1p1f1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	physics_index</td>
        <td class="iris-word-cell" colspan="3">1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	product</td>
        <td class="iris-word-cell" colspan="3">model-output</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	realization_index</td>
        <td class="iris-word-cell" colspan="3">1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	realm</td>
        <td class="iris-word-cell" colspan="3">atmos</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	source</td>
        <td class="iris-word-cell" colspan="3">HadGEM3-GC31-LL (2016):</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	aerosol</td>
        <td class="iris-word-cell" colspan="3">UKCA-GLOMAP-mode</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	atmos</td>
        <td class="iris-word-cell" colspan="3">MetUM-HadGEM3-GA7.1...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	source_id</td>
        <td class="iris-word-cell" colspan="3">HadGEM3-GC31-LL</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	source_type</td>
        <td class="iris-word-cell" colspan="3">AOGCM AER</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	sub_experiment</td>
        <td class="iris-word-cell" colspan="3">none</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	sub_experiment_id</td>
        <td class="iris-word-cell" colspan="3">none</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	table_id</td>
        <td class="iris-word-cell" colspan="3">Amon</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	table_info</td>
        <td class="iris-word-cell" colspan="3">Creation Date:(13 December 2018) MD5:2b12b5db6db112aa8b8b0d6c1645b121</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	title</td>
        <td class="iris-word-cell" colspan="3">HadGEM3-GC31-LL output prepared for CMIP6</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	tracking_id</td>
        <td class="iris-word-cell" colspan="3">hdl:21.14100/b1e2e59a-6313-4b49-8476-c7c961d2111c</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	variable_id</td>
        <td class="iris-word-cell" colspan="3">tasmin</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	variant_label</td>
        <td class="iris-word-cell" colspan="3">r1i1p1f1</td>
    </tr>
    <tr class="iris">
        <td class="iris-title iris-word-cell">Cell methods</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	mean</td>
        <td class="iris-word-cell" colspan="3">area</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	minimum within days</td>
        <td class="iris-word-cell" colspan="3">time</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	mean over days</td>
        <td class="iris-word-cell" colspan="3">time</td>
    </tr>
    </table>
            



Should the equalise function not work there is a function to completely
remove all attributes, demonstarted below:

.. code:: ipython3

    dataset.remove_attributes()
    dataset.cube_dataset[0]




.. raw:: html

    
    <style>
      a.iris {
          text-decoration: none !important;
      }
      table.iris {
          white-space: pre;
          border: 1px solid;
          border-color: #9c9c9c;
          font-family: monaco, monospace;
      }
      th.iris {
          background: #303f3f;
          color: #e0e0e0;
          border-left: 1px solid;
          border-color: #9c9c9c;
          font-size: 1.05em;
          min-width: 50px;
          max-width: 125px;
      }
      tr.iris :first-child {
          border-right: 1px solid #9c9c9c !important;
      }
      td.iris-title {
          background: #d5dcdf;
          border-top: 1px solid #9c9c9c;
          font-weight: bold;
      }
      .iris-word-cell {
          text-align: left !important;
          white-space: pre;
      }
      .iris-subheading-cell {
          padding-left: 2em !important;
      }
      .iris-inclusion-cell {
          padding-right: 1em !important;
      }
      .iris-panel-body {
          padding-top: 0px;
      }
      .iris-panel-title {
          padding-left: 3em;
      }
      .iris-panel-title {
          margin-top: 7px;
      }
    </style>
    <table class="iris" id="140068505525720">
        <tr class="iris">
    <th class="iris iris-word-cell">Air Temperature (K)</th>
    <th class="iris iris-word-cell">time</th>
    <th class="iris iris-word-cell">latitude</th>
    <th class="iris iris-word-cell">longitude</th>
    </tr>
        <tr class="iris">
    <td class="iris-word-cell iris-subheading-cell">Shape</td>
    <td class="iris iris-inclusion-cell">1200</td>
    <td class="iris iris-inclusion-cell">144</td>
    <td class="iris iris-inclusion-cell">192</td>
    </td>
        <tr class="iris">
        <td class="iris-title iris-word-cell">Dimension coordinates</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	time</td>
        <td class="iris-inclusion-cell">x</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">-</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	latitude</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">x</td>
        <td class="iris-inclusion-cell">-</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	longitude</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">x</td>
    </tr>
    <tr class="iris">
        <td class="iris-title iris-word-cell">Scalar coordinates</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	height</td>
        <td class="iris-word-cell" colspan="3">1.5 m</td>
    </tr>
    <tr class="iris">
        <td class="iris-title iris-word-cell">Attributes</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	Conventions</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	activity_id</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	branch_method</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	branch_time_in_child</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	branch_time_in_parent</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	cmor_version</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	comment</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	creation_date</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	cv_version</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	data_specs_version</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	experiment</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	experiment_id</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	external_variables</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	forcing_index</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	frequency</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	further_info_url</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	grid</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	grid_label</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	history</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	initialization_index</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	institution</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	institution_id</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	license</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	mip_era</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	mo_runid</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	nominal_resolution</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	original_name</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_activity_id</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_experiment_id</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_mip_era</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_source_id</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_time_units</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_variant_label</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	physics_index</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	product</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	realization_index</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	realm</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	source</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	source_id</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	source_type</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	sub_experiment</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	sub_experiment_id</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	table_id</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	table_info</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	title</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	tracking_id</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	variable_id</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	variant_label</td>
        <td class="iris-word-cell" colspan="3"></td>
    </tr>
    <tr class="iris">
        <td class="iris-title iris-word-cell">Cell methods</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	mean</td>
        <td class="iris-word-cell" colspan="3">area</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	minimum within days</td>
        <td class="iris-word-cell" colspan="3">time</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	mean over days</td>
        <td class="iris-word-cell" colspan="3">time</td>
    </tr>
    </table>
            



Functions can also be used to collapse a given dimension, below we can
see the ``time`` dimension being collapsed with a mean average (further
ways to collapse data sets such as over time periods and seasons etc.
will be added in later releases):

.. code:: ipython3

    dataset.collapsed_dimension('time')
    print(dataset)


.. parsed-literal::

    0: air_temperature / (K)               (latitude: 144; longitude: 192)
    1: air_temperature / (K)               (latitude: 144; longitude: 192)
    2: air_temperature / (K)               (latitude: 144; longitude: 192)
    3: air_temperature / (K)               (latitude: 144; longitude: 192)
    4: air_temperature / (K)               (latitude: 144; longitude: 192)


Should something go wrong and the dataset is altered, or rather the same
dataset is needed for a different purpose the dataset of cubes can be
reloaded with the ``reload()`` function. The original directory given to
specify datasets remains the same however the optional parameters can be
be passed. This can be demonstrated below:

.. code:: ipython3

    dataset.reset()
    print(dataset)


.. parsed-literal::

    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))
    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))


.. parsed-literal::

    0: air_temperature / (K)               (time: 1200; latitude: 144; longitude: 192)
    1: air_temperature / (K)               (time: 1200; latitude: 144; longitude: 192)
    2: air_temperature / (K)               (time: 1200; latitude: 144; longitude: 192)
    3: air_temperature / (K)               (time: 1200; latitude: 144; longitude: 192)
    4: air_temperature / (K)               (time: 1200; latitude: 144; longitude: 192)


.. parsed-literal::

    /opt/scitools/environments/experimental/current/lib/python3.6/site-packages/iris/fileformats/cf.py:798: UserWarning: Missing CF-netCDF measure variable 'areacella', referenced by netCDF variable 'tasmin'
      warnings.warn(message % (variable_name, nc_var_name))


And as shown it will reset everything (except where specified) to how it
was before:

.. code:: ipython3

    dataset.cube_dataset[0]




.. raw:: html

    
    <style>
      a.iris {
          text-decoration: none !important;
      }
      table.iris {
          white-space: pre;
          border: 1px solid;
          border-color: #9c9c9c;
          font-family: monaco, monospace;
      }
      th.iris {
          background: #303f3f;
          color: #e0e0e0;
          border-left: 1px solid;
          border-color: #9c9c9c;
          font-size: 1.05em;
          min-width: 50px;
          max-width: 125px;
      }
      tr.iris :first-child {
          border-right: 1px solid #9c9c9c !important;
      }
      td.iris-title {
          background: #d5dcdf;
          border-top: 1px solid #9c9c9c;
          font-weight: bold;
      }
      .iris-word-cell {
          text-align: left !important;
          white-space: pre;
      }
      .iris-subheading-cell {
          padding-left: 2em !important;
      }
      .iris-inclusion-cell {
          padding-right: 1em !important;
      }
      .iris-panel-body {
          padding-top: 0px;
      }
      .iris-panel-title {
          padding-left: 3em;
      }
      .iris-panel-title {
          margin-top: 7px;
      }
    </style>
    <table class="iris" id="140068460569376">
        <tr class="iris">
    <th class="iris iris-word-cell">Air Temperature (K)</th>
    <th class="iris iris-word-cell">time</th>
    <th class="iris iris-word-cell">latitude</th>
    <th class="iris iris-word-cell">longitude</th>
    </tr>
        <tr class="iris">
    <td class="iris-word-cell iris-subheading-cell">Shape</td>
    <td class="iris iris-inclusion-cell">1200</td>
    <td class="iris iris-inclusion-cell">144</td>
    <td class="iris iris-inclusion-cell">192</td>
    </td>
        <tr class="iris">
        <td class="iris-title iris-word-cell">Dimension coordinates</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	time</td>
        <td class="iris-inclusion-cell">x</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">-</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	latitude</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">x</td>
        <td class="iris-inclusion-cell">-</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	longitude</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">x</td>
    </tr>
    <tr class="iris">
        <td class="iris-title iris-word-cell">Scalar coordinates</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	height</td>
        <td class="iris-word-cell" colspan="3">1.5 m</td>
    </tr>
    <tr class="iris">
        <td class="iris-title iris-word-cell">Attributes</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	Conventions</td>
        <td class="iris-word-cell" colspan="3">CF-1.7 CMIP-6.2</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	activity_id</td>
        <td class="iris-word-cell" colspan="3">CMIP</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	branch_method</td>
        <td class="iris-word-cell" colspan="3">standard</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	branch_time_in_child</td>
        <td class="iris-word-cell" colspan="3">0.0</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	branch_time_in_parent</td>
        <td class="iris-word-cell" colspan="3">267840.0</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	cmor_version</td>
        <td class="iris-word-cell" colspan="3">3.4.0</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	comment</td>
        <td class="iris-word-cell" colspan="3">minimum near-surface (usually, 2 meter) air temperature (add cell_method...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	creation_date</td>
        <td class="iris-word-cell" colspan="3">2019-06-25T23:09:47Z</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	cv_version</td>
        <td class="iris-word-cell" colspan="3">6.2.20.1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	data_specs_version</td>
        <td class="iris-word-cell" colspan="3">01.00.29</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	experiment</td>
        <td class="iris-word-cell" colspan="3">pre-industrial control</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	experiment_id</td>
        <td class="iris-word-cell" colspan="3">piControl</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	external_variables</td>
        <td class="iris-word-cell" colspan="3">areacella</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	forcing_index</td>
        <td class="iris-word-cell" colspan="3">1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	frequency</td>
        <td class="iris-word-cell" colspan="3">mon</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	further_info_url</td>
        <td class="iris-word-cell" colspan="3">https://furtherinfo.es-doc.org/CMIP6.MOHC.HadGEM3-GC31-LL.piControl.no...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	grid</td>
        <td class="iris-word-cell" colspan="3">Native N96 grid; 192 x 144 longitude/latitude</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	grid_label</td>
        <td class="iris-word-cell" colspan="3">gn</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	history</td>
        <td class="iris-word-cell" colspan="3">2019-06-25T23:09:47Z altered by CMOR: Treated scalar dimension: 'height'....</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	initialization_index</td>
        <td class="iris-word-cell" colspan="3">1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	institution</td>
        <td class="iris-word-cell" colspan="3">Met Office Hadley Centre, Fitzroy Road, Exeter, Devon, EX1 3PB, UK</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	institution_id</td>
        <td class="iris-word-cell" colspan="3">MOHC</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	license</td>
        <td class="iris-word-cell" colspan="3">CMIP6 model data produced by the Met Office Hadley Centre is licensed under...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	mip_era</td>
        <td class="iris-word-cell" colspan="3">CMIP6</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	mo_runid</td>
        <td class="iris-word-cell" colspan="3">u-ar766</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	nominal_resolution</td>
        <td class="iris-word-cell" colspan="3">250 km</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	original_name</td>
        <td class="iris-word-cell" colspan="3">mo: mon_mean_from_day((stash: m01s03i236, lbproc: 4096))</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_activity_id</td>
        <td class="iris-word-cell" colspan="3">CMIP</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_experiment_id</td>
        <td class="iris-word-cell" colspan="3">piControl-spinup</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_mip_era</td>
        <td class="iris-word-cell" colspan="3">CMIP6</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_source_id</td>
        <td class="iris-word-cell" colspan="3">HadGEM3-GC31-LL</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_time_units</td>
        <td class="iris-word-cell" colspan="3">days since 1850-01-01-00-00-00</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_variant_label</td>
        <td class="iris-word-cell" colspan="3">r1i1p1f1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	physics_index</td>
        <td class="iris-word-cell" colspan="3">1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	product</td>
        <td class="iris-word-cell" colspan="3">model-output</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	realization_index</td>
        <td class="iris-word-cell" colspan="3">1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	realm</td>
        <td class="iris-word-cell" colspan="3">atmos</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	source</td>
        <td class="iris-word-cell" colspan="3">HadGEM3-GC31-LL (2016):</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	aerosol</td>
        <td class="iris-word-cell" colspan="3">UKCA-GLOMAP-mode</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	atmos</td>
        <td class="iris-word-cell" colspan="3">MetUM-HadGEM3-GA7.1...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	source_id</td>
        <td class="iris-word-cell" colspan="3">HadGEM3-GC31-LL</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	source_type</td>
        <td class="iris-word-cell" colspan="3">AOGCM AER</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	sub_experiment</td>
        <td class="iris-word-cell" colspan="3">none</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	sub_experiment_id</td>
        <td class="iris-word-cell" colspan="3">none</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	table_id</td>
        <td class="iris-word-cell" colspan="3">Amon</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	table_info</td>
        <td class="iris-word-cell" colspan="3">Creation Date:(13 December 2018) MD5:2b12b5db6db112aa8b8b0d6c1645b121</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	title</td>
        <td class="iris-word-cell" colspan="3">HadGEM3-GC31-LL output prepared for CMIP6</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	tracking_id</td>
        <td class="iris-word-cell" colspan="3">hdl:21.14100/b1e2e59a-6313-4b49-8476-c7c961d2111c</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	variable_id</td>
        <td class="iris-word-cell" colspan="3">tasmin</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	variant_label</td>
        <td class="iris-word-cell" colspan="3">r1i1p1f1</td>
    </tr>
    <tr class="iris">
        <td class="iris-title iris-word-cell">Cell methods</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	mean</td>
        <td class="iris-word-cell" colspan="3">area</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	minimum within days</td>
        <td class="iris-word-cell" colspan="3">time</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	mean over days</td>
        <td class="iris-word-cell" colspan="3">time</td>
    </tr>
    </table>
            



This shows some of cube_helpers more basic methods, but we can do more
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

    dataset.equalise()
    dataset.get_concatenated_cube()




.. raw:: html

    
    <style>
      a.iris {
          text-decoration: none !important;
      }
      table.iris {
          white-space: pre;
          border: 1px solid;
          border-color: #9c9c9c;
          font-family: monaco, monospace;
      }
      th.iris {
          background: #303f3f;
          color: #e0e0e0;
          border-left: 1px solid;
          border-color: #9c9c9c;
          font-size: 1.05em;
          min-width: 50px;
          max-width: 125px;
      }
      tr.iris :first-child {
          border-right: 1px solid #9c9c9c !important;
      }
      td.iris-title {
          background: #d5dcdf;
          border-top: 1px solid #9c9c9c;
          font-weight: bold;
      }
      .iris-word-cell {
          text-align: left !important;
          white-space: pre;
      }
      .iris-subheading-cell {
          padding-left: 2em !important;
      }
      .iris-inclusion-cell {
          padding-right: 1em !important;
      }
      .iris-panel-body {
          padding-top: 0px;
      }
      .iris-panel-title {
          padding-left: 3em;
      }
      .iris-panel-title {
          margin-top: 7px;
      }
    </style>
    <table class="iris" id="140068048656704">
        <tr class="iris">
    <th class="iris iris-word-cell">Air Temperature (K)</th>
    <th class="iris iris-word-cell">time</th>
    <th class="iris iris-word-cell">latitude</th>
    <th class="iris iris-word-cell">longitude</th>
    </tr>
        <tr class="iris">
    <td class="iris-word-cell iris-subheading-cell">Shape</td>
    <td class="iris iris-inclusion-cell">1080</td>
    <td class="iris iris-inclusion-cell">160</td>
    <td class="iris iris-inclusion-cell">320</td>
    </td>
        <tr class="iris">
        <td class="iris-title iris-word-cell">Dimension coordinates</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	time</td>
        <td class="iris-inclusion-cell">x</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">-</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	latitude</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">x</td>
        <td class="iris-inclusion-cell">-</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	longitude</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">x</td>
    </tr>
    <tr class="iris">
        <td class="iris-title iris-word-cell">Attributes</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	CDI</td>
        <td class="iris-word-cell" colspan="3">Climate Data Interface version 1.4.4 (http://code.zmaw.de/projects/cdi...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	CDO</td>
        <td class="iris-word-cell" colspan="3">Climate Data Operators version 1.4.4 (http://code.zmaw.de/projects/cdo...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	Conventions</td>
        <td class="iris-word-cell" colspan="3">CF-1.4</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	associated_files</td>
        <td class="iris-word-cell" colspan="3">baseURL: http://cmip-pcmdi.llnl.gov/CMIP5/dataLocation gridspecFile: gridspec_atmos_fx_EC-EARTH_rcp85_r0i0p0.nc...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	branch_time</td>
        <td class="iris-word-cell" colspan="3">2281.0</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	cmor_version</td>
        <td class="iris-word-cell" colspan="3">2.8.0</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	comment</td>
        <td class="iris-word-cell" colspan="3">Equilibrium reached after preindustrial spin-up after which data were output...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	contact</td>
        <td class="iris-word-cell" colspan="3">Alastair McKinstry <alastair.mckinstry@ichec.ie></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	experiment</td>
        <td class="iris-word-cell" colspan="3">RCP8.5</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	experiment_id</td>
        <td class="iris-word-cell" colspan="3">rcp85</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	forcing</td>
        <td class="iris-word-cell" colspan="3">Nat,Ant</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	frequency</td>
        <td class="iris-word-cell" colspan="3">mon</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	grid_type</td>
        <td class="iris-word-cell" colspan="3">gaussian</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	initialization_method</td>
        <td class="iris-word-cell" colspan="3">1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	institute_id</td>
        <td class="iris-word-cell" colspan="3">ICHEC</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	institution</td>
        <td class="iris-word-cell" colspan="3">EC-Earth (European Earth System Model)</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	model_id</td>
        <td class="iris-word-cell" colspan="3">EC-EARTH</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	modeling_realm</td>
        <td class="iris-word-cell" colspan="3">atmos</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	original_name</td>
        <td class="iris-word-cell" colspan="3">2T</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_experiment</td>
        <td class="iris-word-cell" colspan="3">historical</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_experiment_id</td>
        <td class="iris-word-cell" colspan="3">historical</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_experiment_rip</td>
        <td class="iris-word-cell" colspan="3">r1i1p1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	physics_version</td>
        <td class="iris-word-cell" colspan="3">1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	product</td>
        <td class="iris-word-cell" colspan="3">output</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	project_id</td>
        <td class="iris-word-cell" colspan="3">CMIP5</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	realization</td>
        <td class="iris-word-cell" colspan="3">1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	references</td>
        <td class="iris-word-cell" colspan="3">Model described by Hazeleger et al. (Bull. Amer. Meteor. Soc., 2010, 91,...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	table_id</td>
        <td class="iris-word-cell" colspan="3">Table Amon (26 July 2011) b26379e76858ab98b927917878a63d01</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	title</td>
        <td class="iris-word-cell" colspan="3">EC-EARTH model output prepared for CMIP5 RCP8.5</td>
    </tr>
    <tr class="iris">
        <td class="iris-title iris-word-cell">Cell methods</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	mean</td>
        <td class="iris-word-cell" colspan="3">time (3 hours)</td>
    </tr>
    </table>
            



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

    0: air_temperature / (K)               (time: 1080; latitude: 160; longitude: 320)



Now we can try and extract some data based on our specified constraints,
note that clim_season and season year are not auxillary coordinates.
This will ruin your day, as iris will conclude that NONE of the data
falls into these catergories, and remove ALL cubes from
``cube_dataset``:

.. code:: ipython3

    dataset.extract(future_constraint)
    dataset




.. parsed-literal::

    0: air_temperature / (K)               (time: 153; latitude: 160; longitude: 320)



So lets reset, and try that again. This time we will add time
catergoricals.

.. code:: ipython3

    dataset.reset()
    dataset.equalise()
    dataset.concatenate_cube()

Here we see no clim_season or season_year Auxillary coordinates:

.. code:: ipython3

    dataset.cube_dataset[0]




.. raw:: html

    
    <style>
      a.iris {
          text-decoration: none !important;
      }
      table.iris {
          white-space: pre;
          border: 1px solid;
          border-color: #9c9c9c;
          font-family: monaco, monospace;
      }
      th.iris {
          background: #303f3f;
          color: #e0e0e0;
          border-left: 1px solid;
          border-color: #9c9c9c;
          font-size: 1.05em;
          min-width: 50px;
          max-width: 125px;
      }
      tr.iris :first-child {
          border-right: 1px solid #9c9c9c !important;
      }
      td.iris-title {
          background: #d5dcdf;
          border-top: 1px solid #9c9c9c;
          font-weight: bold;
      }
      .iris-word-cell {
          text-align: left !important;
          white-space: pre;
      }
      .iris-subheading-cell {
          padding-left: 2em !important;
      }
      .iris-inclusion-cell {
          padding-right: 1em !important;
      }
      .iris-panel-body {
          padding-top: 0px;
      }
      .iris-panel-title {
          padding-left: 3em;
      }
      .iris-panel-title {
          margin-top: 7px;
      }
    </style>
    <table class="iris" id="140068505523928">
        <tr class="iris">
    <th class="iris iris-word-cell">Air Temperature (K)</th>
    <th class="iris iris-word-cell">time</th>
    <th class="iris iris-word-cell">latitude</th>
    <th class="iris iris-word-cell">longitude</th>
    </tr>
        <tr class="iris">
    <td class="iris-word-cell iris-subheading-cell">Shape</td>
    <td class="iris iris-inclusion-cell">1080</td>
    <td class="iris iris-inclusion-cell">160</td>
    <td class="iris iris-inclusion-cell">320</td>
    </td>
        <tr class="iris">
        <td class="iris-title iris-word-cell">Dimension coordinates</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	time</td>
        <td class="iris-inclusion-cell">x</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">-</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	latitude</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">x</td>
        <td class="iris-inclusion-cell">-</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	longitude</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">x</td>
    </tr>
    <tr class="iris">
        <td class="iris-title iris-word-cell">Attributes</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	CDI</td>
        <td class="iris-word-cell" colspan="3">Climate Data Interface version 1.4.4 (http://code.zmaw.de/projects/cdi...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	CDO</td>
        <td class="iris-word-cell" colspan="3">Climate Data Operators version 1.4.4 (http://code.zmaw.de/projects/cdo...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	Conventions</td>
        <td class="iris-word-cell" colspan="3">CF-1.4</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	associated_files</td>
        <td class="iris-word-cell" colspan="3">baseURL: http://cmip-pcmdi.llnl.gov/CMIP5/dataLocation gridspecFile: gridspec_atmos_fx_EC-EARTH_rcp85_r0i0p0.nc...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	branch_time</td>
        <td class="iris-word-cell" colspan="3">2281.0</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	cmor_version</td>
        <td class="iris-word-cell" colspan="3">2.8.0</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	comment</td>
        <td class="iris-word-cell" colspan="3">Equilibrium reached after preindustrial spin-up after which data were output...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	contact</td>
        <td class="iris-word-cell" colspan="3">Alastair McKinstry <alastair.mckinstry@ichec.ie></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	experiment</td>
        <td class="iris-word-cell" colspan="3">RCP8.5</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	experiment_id</td>
        <td class="iris-word-cell" colspan="3">rcp85</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	forcing</td>
        <td class="iris-word-cell" colspan="3">Nat,Ant</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	frequency</td>
        <td class="iris-word-cell" colspan="3">mon</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	grid_type</td>
        <td class="iris-word-cell" colspan="3">gaussian</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	initialization_method</td>
        <td class="iris-word-cell" colspan="3">1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	institute_id</td>
        <td class="iris-word-cell" colspan="3">ICHEC</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	institution</td>
        <td class="iris-word-cell" colspan="3">EC-Earth (European Earth System Model)</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	model_id</td>
        <td class="iris-word-cell" colspan="3">EC-EARTH</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	modeling_realm</td>
        <td class="iris-word-cell" colspan="3">atmos</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	original_name</td>
        <td class="iris-word-cell" colspan="3">2T</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_experiment</td>
        <td class="iris-word-cell" colspan="3">historical</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_experiment_id</td>
        <td class="iris-word-cell" colspan="3">historical</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_experiment_rip</td>
        <td class="iris-word-cell" colspan="3">r1i1p1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	physics_version</td>
        <td class="iris-word-cell" colspan="3">1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	product</td>
        <td class="iris-word-cell" colspan="3">output</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	project_id</td>
        <td class="iris-word-cell" colspan="3">CMIP5</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	realization</td>
        <td class="iris-word-cell" colspan="3">1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	references</td>
        <td class="iris-word-cell" colspan="3">Model described by Hazeleger et al. (Bull. Amer. Meteor. Soc., 2010, 91,...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	table_id</td>
        <td class="iris-word-cell" colspan="3">Table Amon (26 July 2011) b26379e76858ab98b927917878a63d01</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	title</td>
        <td class="iris-word-cell" colspan="3">EC-EARTH model output prepared for CMIP5 RCP8.5</td>
    </tr>
    <tr class="iris">
        <td class="iris-title iris-word-cell">Cell methods</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	mean</td>
        <td class="iris-word-cell" colspan="3">time (3 hours)</td>
    </tr>
    </table>
            



However we can add these with the following commands:

.. code:: ipython3

    dataset.add_time_catergorical('season_year')
    dataset.add_time_catergorical('clim_season')
    dataset.cube_dataset[0]

Now it’s been added we can safely filter data based on constrints:

.. code:: ipython3

    dataset.extract(future_constraint)

.. code:: ipython3

    dataset.cube_dataset[0]




.. raw:: html

    
    <style>
      a.iris {
          text-decoration: none !important;
      }
      table.iris {
          white-space: pre;
          border: 1px solid;
          border-color: #9c9c9c;
          font-family: monaco, monospace;
      }
      th.iris {
          background: #303f3f;
          color: #e0e0e0;
          border-left: 1px solid;
          border-color: #9c9c9c;
          font-size: 1.05em;
          min-width: 50px;
          max-width: 125px;
      }
      tr.iris :first-child {
          border-right: 1px solid #9c9c9c !important;
      }
      td.iris-title {
          background: #d5dcdf;
          border-top: 1px solid #9c9c9c;
          font-weight: bold;
      }
      .iris-word-cell {
          text-align: left !important;
          white-space: pre;
      }
      .iris-subheading-cell {
          padding-left: 2em !important;
      }
      .iris-inclusion-cell {
          padding-right: 1em !important;
      }
      .iris-panel-body {
          padding-top: 0px;
      }
      .iris-panel-title {
          padding-left: 3em;
      }
      .iris-panel-title {
          margin-top: 7px;
      }
    </style>
    <table class="iris" id="140068462063456">
        <tr class="iris">
    <th class="iris iris-word-cell">Air Temperature (K)</th>
    <th class="iris iris-word-cell">time</th>
    <th class="iris iris-word-cell">latitude</th>
    <th class="iris iris-word-cell">longitude</th>
    </tr>
        <tr class="iris">
    <td class="iris-word-cell iris-subheading-cell">Shape</td>
    <td class="iris iris-inclusion-cell">153</td>
    <td class="iris iris-inclusion-cell">160</td>
    <td class="iris iris-inclusion-cell">320</td>
    </td>
        <tr class="iris">
        <td class="iris-title iris-word-cell">Dimension coordinates</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	time</td>
        <td class="iris-inclusion-cell">x</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">-</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	latitude</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">x</td>
        <td class="iris-inclusion-cell">-</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	longitude</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">x</td>
    </tr>
    <tr class="iris">
        <td class="iris-title iris-word-cell">Auxiliary coordinates</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	clim_season</td>
        <td class="iris-inclusion-cell">x</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">-</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	season_year</td>
        <td class="iris-inclusion-cell">x</td>
        <td class="iris-inclusion-cell">-</td>
        <td class="iris-inclusion-cell">-</td>
    </tr>
    <tr class="iris">
        <td class="iris-title iris-word-cell">Attributes</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	CDI</td>
        <td class="iris-word-cell" colspan="3">Climate Data Interface version 1.4.4 (http://code.zmaw.de/projects/cdi...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	CDO</td>
        <td class="iris-word-cell" colspan="3">Climate Data Operators version 1.4.4 (http://code.zmaw.de/projects/cdo...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	Conventions</td>
        <td class="iris-word-cell" colspan="3">CF-1.4</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	associated_files</td>
        <td class="iris-word-cell" colspan="3">baseURL: http://cmip-pcmdi.llnl.gov/CMIP5/dataLocation gridspecFile: gridspec_atmos_fx_EC-EARTH_rcp85_r0i0p0.nc...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	branch_time</td>
        <td class="iris-word-cell" colspan="3">2281.0</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	cmor_version</td>
        <td class="iris-word-cell" colspan="3">2.8.0</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	comment</td>
        <td class="iris-word-cell" colspan="3">Equilibrium reached after preindustrial spin-up after which data were output...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	contact</td>
        <td class="iris-word-cell" colspan="3">Alastair McKinstry <alastair.mckinstry@ichec.ie></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	experiment</td>
        <td class="iris-word-cell" colspan="3">RCP8.5</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	experiment_id</td>
        <td class="iris-word-cell" colspan="3">rcp85</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	forcing</td>
        <td class="iris-word-cell" colspan="3">Nat,Ant</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	frequency</td>
        <td class="iris-word-cell" colspan="3">mon</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	grid_type</td>
        <td class="iris-word-cell" colspan="3">gaussian</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	initialization_method</td>
        <td class="iris-word-cell" colspan="3">1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	institute_id</td>
        <td class="iris-word-cell" colspan="3">ICHEC</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	institution</td>
        <td class="iris-word-cell" colspan="3">EC-Earth (European Earth System Model)</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	model_id</td>
        <td class="iris-word-cell" colspan="3">EC-EARTH</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	modeling_realm</td>
        <td class="iris-word-cell" colspan="3">atmos</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	original_name</td>
        <td class="iris-word-cell" colspan="3">2T</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_experiment</td>
        <td class="iris-word-cell" colspan="3">historical</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_experiment_id</td>
        <td class="iris-word-cell" colspan="3">historical</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	parent_experiment_rip</td>
        <td class="iris-word-cell" colspan="3">r1i1p1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	physics_version</td>
        <td class="iris-word-cell" colspan="3">1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	product</td>
        <td class="iris-word-cell" colspan="3">output</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	project_id</td>
        <td class="iris-word-cell" colspan="3">CMIP5</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	realization</td>
        <td class="iris-word-cell" colspan="3">1</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	references</td>
        <td class="iris-word-cell" colspan="3">Model described by Hazeleger et al. (Bull. Amer. Meteor. Soc., 2010, 91,...</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	table_id</td>
        <td class="iris-word-cell" colspan="3">Table Amon (26 July 2011) b26379e76858ab98b927917878a63d01</td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	title</td>
        <td class="iris-word-cell" colspan="3">EC-EARTH model output prepared for CMIP5 RCP8.5</td>
    </tr>
    <tr class="iris">
        <td class="iris-title iris-word-cell">Cell methods</td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
        <td class="iris-title"></td>
    </tr>
    <tr class="iris">
        <td class="iris-word-cell iris-subheading-cell">	mean</td>
        <td class="iris-word-cell" colspan="3">time (3 hours)</td>
    </tr>
    </table>
            



.. code:: ipython3

    dataset




.. parsed-literal::

    0: air_temperature / (K)               (time: 153; latitude: 160; longitude: 320)


