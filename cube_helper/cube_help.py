import iris
from cube_helper.cube_loader import CubeLoader
from cube_helper.cube_dataset import CubeSet
from cube_helper.cube_equaliser import remove_attributes, \
    equalise_time_units, equalise_attributes, equalise_data_type


class CubeHelp(object):
    """
    A wrapper class to implement methods provided by cube_equaliliser
    And cube_loader. To be used to manipulate cube datasets.


    Attributes:
            directory: a list of cubes or a chosen directory
            to operate on.

            filetype (optional): a string specifying the expected type
            of files found in the dataset

            constraints (optional): a string specifying any constraints
            you wish to load the dataset with.

            cube_dataset: a CubeList containing the datasets you wish to
            manipulate/analyse. An instance of the CubeSet object, which
            in itself is a custom CubeList
    """
    def __init__(self, directory, filetype=".nc", constraints=None):
        """
        Initialises the CubeHelp object, will automatically select the loading
        Strategy based on the Arguments passed to it.


        Args:
            directory: a list of cubes or a chosen
            directory to operate on.

            filetype (optional): a string specifying the
            expected type of files found in the dataset

            constraints (optional): a string specifying
            any constraints you wish to load the dataset with.

        Returns:
            All attributes attained from the given parameters

        """
        self.directory = directory
        self.filetype = filetype
        self.constraints = constraints
        if isinstance(directory, str):
            loaded_cubes = CubeLoader.load_from_dir(
                directory, constraints, filetype)
            if not loaded_cubes:
                print("No cubes found")
            else:
                self.cube_dataset = CubeSet(loaded_cubes)
        elif isinstance(directory, list):
            loaded_cubes = CubeLoader.load_from_filelist(
                directory, constraints, filetype)

            if not loaded_cubes:
                print("No cubes found")
            else:
                self.cube_dataset = CubeSet(loaded_cubes)

    def __repr__(self):
        """
        Prettifies the cube_dataset attribute and returns it.
        """
        return '{self.cube_dataset.cube_list}'.format(self=self)

    def equalise(self):
        """
        Equalises cubes for concatenation and merging, cycles through the cube_
        Dataset (CubeList) attribute and rectifies common differences in
        metadat and variables. Then cycles through and unifies the time units.

        Returns:
            Equalised cube_dataset to the CubeHelp class
        """
        equalise_attributes(self.cube_dataset.cube_list)
        equalise_time_units(self.cube_dataset.cube_list)

    def get_concatenated(self):
        """
        Gets a concatenated form of the cube_dataset object, This method DOES
        NOT Concatenate the cube_dataset itself but instead returns it's
        Concatenated form as a CubeList. This function makes use of iris'
        concatenate() function, as a result it will concatenate the
        cube_dataset into the Smallest CubeList possible. Not suitable for
        Cubes of only 2 dimensions.

        Returns:
            A concatenated CubeList of the cube_dataset
        """
        return self.cube_dataset.cube_list.concatenate()

    def get_concatenated_cube(self):
        """
        Gets a concatenated form of the cube_dataset object, This method DOES
        NOT concatenate the cube_dataset itself but instead returns it's
        Concatenated form as a Cube. This function makes use of iris'
        concatenate_cube() function, as a result it will concatenate the
        cube_dataset into a single Cube. Not suitable for cubes of only
        2 dimensions.

        Returns:
            A concatenated Cube of the cube_dataset
        """
        return self.cube_dataset.cube_list.concatenate_cube()

    def get_merged_cube(self):
        """
        Gets a merged form of the cube_dataset object, This method DOES
        NOT merge the cube_dataset itself but instead returns it's
        Merged form as a single Cube. This function makes use of iris'
        merge_cube() function, as a result it will Concatenate the
        cube_dataset into a single Cube if possible. Issues may arrise
        From concatenating cubes with mismatching metadata and time units.
        Not suitable for cubes with more than 2 dimensions.

        Returns:
            A merged Cube of the cube_dataset
        """
        return self.cube_dataset.cube_list.merge_cube()

    def get_merged(self):
        """
        Gets a merged form of the cube_dataset object, This method DOES
        NOT merge the cube_dataset itself but instead returns it's merged
        Form as a CubeList. This function makes use of iris' merge_cube()
        Function, as a result it will concatenate the cube_dataset into a
        CubeList, constucting a new dimension. Issues may arrise from
        Concatenating cubes with mismatching metadata And time units.
        Not suitable for cubes with more than 2 dimensions.

        Returns:
            A merged CubeList of the cube_dataset
        """
        return self.cube_dataset.cube_list.merge()

    def convert_units(self, unit):
        """
        Converts units of co-ordinates to an approved CF convention
        Units name.

        Args:
            unit: A string specifying unit you wish to convert to.

        Returns:
            The cube_dataset with it's units converted to those specified.
            Units MUST be of the CF convention, i.e No trying to convert
            'meters' into 'leagues'!
        """
        for cube in self.cube_dataset.cube_list:
            cube.convert_units(unit)

    def collapsed_dimension(self, dimension):
        """
        Collapses a given dimension with a mean average measurement.

        Args:
            dimension: The dimension of the cube you wish to collapse.

        Returns:
            The cube_dataset with the specified dimension collapsed.
        """
        for index, cube in enumerate(self.cube_dataset.cube_list):
            self.cube_dataset.cube_list[index] = cube.collapsed(
                dimension, iris.analysis.MEAN)

    def remove_attributes(self):
        """
        Removes all attributes from the cube_lists metadata, replaces
        Them with an empty string.

        Returns:
             The cube_dataset with all attributes stripped out of the
             Metadata.
        """
        remove_attributes(self.cube_dataset.cube_list)

    def equalise_data_type(self):
        """
        Unifies the datatype of the cube_dataset data to a common type.
        Datatype must be compatible for conversion, Currently only
        Converts to float32 but other datatypes to soon be supported.

        Returns:
            The cube_dataset with identical datatypes in each cube.

        """
        equalise_data_type(self.cube_dataset.cube_list)

    def reset(self, filetype='.nc', constraints=None):
        self.__init__(self.directory, filetype, constraints)