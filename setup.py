from distutils.core import setup
setup(
  name = 'cube_helper',
  packages = ['cube_helper'],
  version = '2.0.8',
  license='BSD 3-Clause License',
  description = """Cube Helper is a package to make equalisation, 
  concatenation, and analysis of iris cubes easier.
  
  It is written with reasearchers in mind and provides a good 
  degree of abstraction from many iris functions and methods.""",
  author = 'Met Office',
  author_email = 'jon.seddon@metoffice.gov.uk',
  url = 'https://github.com/MetOffice/cube_helper',
  download_url = 'https://github.com/MetOffice/cube_helper/archive/v2.0.7.tar.gz',
  keywords = ['climate', 'cmip', 'iris', 'cubes', 'preprocessing'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.6',
  ],
)