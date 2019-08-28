import iris


class CubeSet(iris.cube.CubeList):
    """
    A custome CubeList object that will be operated on as a dataset.
    """

    def __init__(self, loaded_cubes):
        """
        initialises class. inherits from CubeList.

        Attributes:
            cube_list: a CubeList of the iris data you wish to load
        """
        self.cube_list = iris.cube.CubeList(loaded_cubes)


    def __repr__(self):
        """
        prettify the set of cubes (CubeSet)
        """
        return '{}'.format(self.cube_list)


