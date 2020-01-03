Quickstart
==========

A Quick starting guide to get you using ``cube_helper`` in a matter of minutes.

Loading a cube
^^^^^^^^^^^^^^
.. code-block:: python

   >>> import cube_helper as ch
   >>> cube = ch.load('/project/champ/data/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/piControl/r1i1p1f1/Amon/tasmin/gn/v20190628')

Loading a cube with constraints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

   >>> longitude_constraint = iris.Constraint(longitude = lamda cell : cell > 0 and cell < 180)
   >>> cube = ch.load('/project/champ/data/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/piControl/r1i1p1f1/Amon/tasmin/gn/v20190628', constraints=longitude_constraint)


Concatenating a cube
^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

   >>> cubes
   [<iris 'Cube' of air_temperature / (K) (time: 1200; latitude: 144; longitude: 192)>,
   <iris 'Cube' of air_temperature / (K) (time: 1200; latitude: 144; longitude: 192)>,
   <iris 'Cube' of air_temperature / (K) (time: 1200; latitude: 144; longitude: 192)>,
   <iris 'Cube' of air_temperature / (K) (time: 1200; latitude: 144; longitude: 192)>,
   <iris 'Cube' of air_temperature / (K) (time: 1200; latitude: 144; longitude: 192)>]

   >>> cube = ch.concatenate(cubes)
   Deleting creation_date attribute from cubes

   Deleting history attribute from cubes

   Deleting tracking_id attribute from cubes


   >>> cube
   <iris 'Cube' of air_temperature / (K) (time: 6000; latitude: 144; longitude: 192)>


