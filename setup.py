from setuptools import setup

from codecs import open
from os import path
from sphinx.setup_command import BuildDoc

with open(path.join('.', 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

name = 'psio'
version = '0.2'
release = '0.2.11'

setup(
    name=name,
    version=release,

    description='Library to facilitate access for photon science data in different formats; including a viewer.',
    long_description=long_description,

    test_suite="tests",

    url='https://github.com/syncope/psio',

    author='Ch.Rosemann',
    author_email='christoph.rosemann@desy.de',

    license='GPLv2',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='photon science file input output',

    packages=['psio', ],

    package_dir={'psio': 'psio', },

    include_package_data=True,

    cmdclass={'build_sphinx': BuildDoc, },
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'source_dir': ('setup.py', 'doc')}},
)
