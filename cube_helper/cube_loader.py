import os
import iris


class CubeLoader(object):

    @staticmethod
    def load_from_dir(directory, constraint=None, filetype='.nc'):
        """
        Loads a set of cubes from a given directory, single cubes are loaded
        and returned as a CubeList.

        Args:
            directory: a chosen directory
            to operate on.

            filetype (optional): a string specifying the expected type
            Of files found in the dataset

            constraints (optional): a string specifying any constraints
            You wish to load the dataset with.

        Returns:
            iris.cube.CubeList(loaded_cubes), a CubeList of the loaded
            Cubes.
        """
        if constraint is None:
            loaded_cubes = []
            for path in os.listdir(directory):
                full_path = os.path.join(directory, path)
                if os.path.isfile(full_path):
                    if full_path.endswith(filetype):
                        loaded_cubes.append(iris.load_cube(full_path))
            return iris.cube.CubeList(loaded_cubes)
        else:
            loaded_cubes = []
            for path in os.listdir(directory):
                full_path = os.path.join(directory, path)
                if os.path.isfile(full_path):
                    if full_path.endswith(filetype):
                        loaded_cubes.append(iris.load_cube(full_path,
                                                           constraint))
            return iris.cube.CubeList(loaded_cubes)

    @staticmethod
    def load_from_filelist(data_filelist, constraint=None,
                           filetype='.nc'):
        """
        Loads the specified files. Individual files are
        Loaded and appended into an iterable as well as being loaded into a
        CubeList.

        Args:
            data_filelist: a chosen list of filenames to operate on.

            filetype (optional): a string specifying the expected type
            Of files found in the dataset

            constraints (optional): a string specifying any constraints
            You wish to load the dataset with.

        Returns:
            iris.cube.CubeList(loaded_cubes), a CubeList of the loaded
            Cubes.
        """
        loaded_cubes = []
        for filename in data_filelist:
            if filename.endswith(filetype):
                break
            else:
                print('\n\nThe selected filetype is '
                      'not present in data_filelist\n\n')

        for filename in data_filelist:
            if constraint is None:
                loaded_cubes.append(iris.load_cube(filename))

            else:

                loaded_cubes.append(iris.load_cube(filename, constraint))

        return iris.cube.CubeList(loaded_cubes)
