import iris
import iris.coord_categorisation
import six
from cube_helper.cube_loader import load_from_filelist, load_from_dir
from cube_helper.cube_dataset import CubeSet
from cube_helper.cube_equaliser import (remove_attributes, 
    equalise_time_units, equalise_attributes, equalise_data_type)


class CubeHelp(object):
    """
    A wrapper class to help load and work with Iris cubes loaded from typical
    climate data.
    and cube_loader. To be used to manipulate cube datasets.


    Attributes:
            directory: a list of filenames or a path to a directory
            to operate on. directory MUST start and end with forward
            slashes.

            filetype: a string specifying the expected type
            of files found in the dataset. Default value is .nc

            constraints: a string specifying any constraints
            you wish to load the dataset with.
        Returns:
            cube_dataset: a CubeList containing the datasets you wish to
            manipulate/analyse. An instance of the CubeSet object, which
            in itself is a custom CubeList
    """
    def __init__(self, directory, filetype=".nc", constraints=None):
        """
        Initialises the CubeHelp object, will automatically select the loading
        strategy based on the Arguments passed to it.
        """
        self.directory = directory
        self.filetype = filetype
        self.constraints = constraints        
        if isinstance(directory, six.string_types):
            loaded_cubes = load_from_dir(
                directory, filetype, constraints)
            if not loaded_cubes:
                print("No cubes found")
            else:
                self.cube_dataset = CubeSet(loaded_cubes)
        elif isinstance(directory, list):
            loaded_cubes = load_from_filelist(
                directory, filetype, constraints)

            if not loaded_cubes:
                print("No cubes found")
            else:
                self.cube_dataset = CubeSet(loaded_cubes)

    def __repr__(self):
        """
        Prettifies the cube_dataset attribute and returns it.
        """
        return '{}'.format(self.cube_dataset)

    def equalise(self):
        """
        Equalises Cubes for concatenation and merging, cycles through the cube_
        dataset (CubeList) attribute and rectifies common differences in
        metadata and attributes. Then cycles through and unifies the time units.

        Returns:
            Equalised cube_dataset to the CubeHelp class
        """
        equalise_attributes(self.cube_dataset)
        equalise_time_units(self.cube_dataset)

    def concatenate(self):
        self.cube_dataset.concatenate()

    def concatenate_cube(self):
        self.cube_dataset.concatenate_cube()

    def get_concatenated(self):
        """
        Gets a concatenated form of the cube_dataset object, This method DOES
        NOT Concatenate the cube_dataset itself but instead returns it's
        concatenated form as a CubeList. This function makes use of Iris'
        concatenate() function, as a result it will concatenate the
        cube_dataset into the Smallest CubeList possible. Not suitable for
        cubes of only 2 dimensions.

        Returns:
            A concatenated CubeList of the cube_dataset
        """
        return self.cube_dataset.concatenate()

    def get_concatenated_cube(self):
        """
        Gets a concatenated form of the cube_dataset object, This method DOES
        NOT concatenate the cube_dataset itself but instead returns it's
        concatenated form as a Cube. This function makes use of Iris'
        concatenate_cube() function, as a result it will concatenate the
        cube_dataset into a single Cube. Not suitable for cubes of only
        2 dimensions.

        Returns:
            A concatenated Cube of the cube_dataset
        """
        return self.cube_dataset.concatenate_cube()

    def get_merged_cube(self):
        """
        Gets a merged form of the cube_dataset object, This method DOES
        NOT merge the cube_dataset itself but instead returns it's
        merged form as a single Cube. This function makes use of iris'
        merge_cube() function, as a result it will Concatenate the
        cube_dataset into a single Cube if possible. Issues may arrise
        from concatenating cubes with mismatching metadata and time units.
        Not suitable for cubes with more than 2 dimensions.

        Returns:
            A merged Cube of the cube_dataset
        """
        return self.cube_dataset.merge_cube()

    def get_merged(self):
        """
        Gets a merged form of the cube_dataset object, This method DOES
        NOT merge the cube_dataset itself but instead returns it's merged
        form as a CubeList. This function makes use of iris' merge_cube()
        function, as a result it will concatenate the cube_dataset into a
        CubeList, constucting a new dimension. Issues may arrise from
        concatenating cubes with mismatching metadata And time units.
        Not suitable for cubes with more than 2 dimensions.

        Returns:
            A merged CubeList of the cube_dataset
        """
        return self.cube_dataset.merge()

    def convert_units(self, unit):
        """
        Converts units of co-ordinates to an approved CF convention
        units name.

        Args:
            unit: A string specifying unit you wish to convert to.

        Returns:
            The cube_dataset with its units converted to those specified.
            Units MUST be of the CF convention, i.e No trying to convert
            'meters' into 'leagues'!
        """
        for cube in self.cube_dataset:
            cube.convert_units(unit)

    def collapsed_dimension(self, dimension):
        """
        Collapses a given dimension with a mean average measurement.

        Args:
            dimension: A string specifying the dimension of the cube 
            you wish to collapse, for example 'time'.

        Returns:
            The cube_dataset with the specified dimension collapsed.
        """
        for index, cube in enumerate(self.cube_dataset):
            self.cube_dataset[index] = cube.collapsed(
                dimension, iris.analysis.MEAN)

    def remove_attributes(self):
        """
        Removes all attributes from the cube_datasets metadata, replaces
        them with an empty string.

        Returns:
             The cube_dataset with all attributes stripped out of the
             Metadata.
        """
        remove_attributes(self.cube_dataset)

    def equalise_data_type(self):
        """
        Unifies the datatype of the cube_dataset data to a common type.
        Datatype must be compatible for conversion, Currently only
        converts to float32 but other datatypes to soon be supported.

        Returns:
            The cube_dataset with identical datatypes in each cube.

        """
        equalise_data_type(self.cube_dataset)

    def reset(self, filetype='.nc', constraints=None):
        """
        Re-initialises the cube_dataset, using the directory originally given.
        
        Args:
            filetype: a string specifying the expected type
            of files found in the dataset. Default value is .nc .

            constraints: a string specifying any constraints
            you wish to load the dataset with.
            
        Returns:
            A re-initialised CubeHelp object.
        """
        self.__init__(self.directory, filetype, constraints)

    def get_cube(self, index):
        """
        Returns a single specified cube from cube_dataset.

        Args:
             index: an int index value specifying which cube out of
             cube_dataset you wish to return.

        Returns:
                A single Cube.
        """
        return self.cube_dataset[index]

    def remove_cube(self, index):
        """
        Removes a single specified cube from cube_dataset.

        Args:
             index: an int index value specifying which cube out of
             cube_dataset you wish to remove.

        Returns:

        """
        self.cube_dataset.pop(index)

    def aggragate(self, aggregation_list):
        """
        Aggregates data in cube_dataset by different catergories.

        Args:
             aggregation_list: a list containing the catergories to aggregate
             by. e.g ['clim_year','season_year']

        Returns:
             cube_dataset aggregated by specified catergories.
        """
        for cube in self.cube_dataset:
            cube.aggregated_by(aggregation_list, iris.analysis.MEAN)

    def extract(self, constraint):
        """
        Extracts a potion of data from cube_dataset within specified contraints.
        To be used when more detailed contraints other than phenomenon is needed.

        Args:
             constraint: An iris.constraint object

        Returns:
             constrained cube_dataset.
        """
        for cube in self.cube_dataset:
            cube.extract(constraint)

    def add_time_catergorical(self, name, coord='time'):
        """
        Adds a catergorical time coordinate.

        Args:
            name: a string specifying the time catergory to add.

            coords: a string specifying the coordinate to operate on.
            default value set to 'time'.


        Returns:
            The cube_dataset with the time category added to each cube.
        """

        if name == 'season_year':
            for cube in self.cube_dataset:
                iris.coord_categorisation.add_season_year(cube, coord,
                                                          name='season_year')
        elif name == 'season_membership':
            for cube in self.cube_dataset:
                iris.coord_categorisation.add_season_membership(cube, coord,
                                                          name='season_membership')
        elif name == 'season_number':
            for cube in self.cube_dataset:
                iris.coord_categorisation.add_season_number(cube, coord,
                                                          name='number')
        elif name == 'clim_season':
            for cube in self.cube_dataset:
                iris.coord_categorisation.add_season(cube, coord,
                                                     name='clim_season')
        elif name == 'year':
            for cube in self.cube_dataset:
                iris.coord_catergorisation.add_year(cube, coord,
                                                    name='year')
        elif name == 'month_number':
            for cube in self.cube_dataset:
                iris.coord_catergorisation.add_month_number(cube, coord,
                                                            name='month_number')
        elif name == 'month_fullname':
            for cube in self.cube_dataset:
                iris.coord_catergorisation.add_month_fullname(cube, coord,
                                                              name='month_fullname')
        elif name == 'month':
            for cube in self.cube_dataset:
                iris.coord_catergorisation.add_month(cube, coord,
                                                     name='month')
        elif name == 'day_of_the_month':
            for cube in self.cube_dataset:
                iris.coord_catergorisation.add_day_of_the_month(cube, coord,
                                                                name='day_of_the_month')
        elif name == 'day_of_the_year':
            for cube in self.cube_dataset:
                iris.coord_catergorisation.add_day_of_the_year(cube, coord,
                                                                name='day_of_the_year')
        elif name == 'weekday_number':
            for cube in self.cube_dataset:
                iris.coord_catergorisation.add_weekday_number(cube, coord,
                                                              name='weekday_number')
        elif name == 'weekday_fullname':
            for cube in self.cube_dataset:
                iris.coord_catergorisation.add_weekday_fullname(cube, coord,
                                                                name='weekday_fullname')
        elif name == 'weekday':
            for cube in self.cube_dataset:
                iris.coord_catergorisation.add_weekday(cube, coord,
                                                       name='weekday')
        elif name == 'hour':
            for cube in self.cube_dataset:
                iris.coord_catergorisation.add_hour(cube, coord,
                                                    name='hour')

