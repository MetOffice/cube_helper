# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.
import os
import setuptools


def get_long_description():
    """Use the contents of README.md as the long description"""
    with open("README.md", "r") as fh:
        return fh.read()


def extract_version():
    """
    Retrieve version information from the  __init__.py module.
    """
    version = ''
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'cube_helper', '__init__.py')

    with open(filename) as fd:
        for line in fd:
            line = line.strip()
            if line.startswith('__version__'):
                try:
                    version = line.split('=')[1].strip(' "\'')
                except Exception:
                    pass
                break

    if not version:
        print('WARNING: Unable to parse version information from '
              'file: {}'.format(filename))
        version = '0.0.0'

    return version


setuptools.setup(
    name='cube_helper',
    packages=['cube_helper'],
    version=extract_version(),
    license='BSD 3-Clause License',
    description=('Cube Helper is a package to make equalisation, '
                 'concatenation, and analysis of Iris cubes easier.'),
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author='Met Office',
    author_email='jon.seddon@metoffice.gov.uk',
    url='https://github.com/MetOffice/cube_helper',
    download_url='https://github.com/MetOffice/cube_helper/releases',
    keywords=['climate', 'cmip', 'iris', 'cubes', 'preprocessing'],
    install_requires=[
        'scitools-iris'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
