import iris


class CubeSet(iris.cube.CubeList):
    """
    A custome CubeList object that will be operated on as a dataset.
    """

    def __init__(self, loaded_cubes):
        """
        initialises class. inherits from CubeList.

        Args:
            loaded_cubes: a list of Cubes data you wish to load
        """
        super().__init__(loaded_cubes)
