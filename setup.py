from setuptools import setup, find_packages

from sphinx.setup_command import BuildDoc

from codecs import open
from os import path

with open(path.join('.', 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='psio',

    version='0.1.0dev',

    description='Module to facilitate access for photon science data in different formats.', 
    long_description=long_description,

    url='https://github.com/syncope/psio',

    author='Ch.Rosemann',
    author_email='christoph.rosemann@desy.de',
    
    license='GPLv2',
    
    classifiers = [
        'Development status :: 3 - Alpha',
        
        'Intended audience :: photon scientists',
        'Topic :: File IO',
        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='photon science file input output',
    
    packages=find_packages(),
    
    extras_require={
        'test': ['files']
        },
    #~ entry_points={
        #~ 'console_scripts': [
            #~ '',
        #~ ],

    #~ scripts=['bin/counting_bad_pixels.py',
        #~ 'bin/simple_file_viewer.py',
        #~ 'bin/simpleViewerG.ui',
        #~ 'bin/simpleViewerGUI.py',
        #~ 'bin/stupid_gisaxs-p03.py'],
    
    data_files=[('.', ['COPYRIGHT','LICENSE']), ],

    #~ cmdclass={'build_sphinx': BuildDoc,},
    #~ command_options={
        #~ 'build_sphinx': {
            #~ 'project': ('setup.py', name),
            #~ 'version': ('setup.py', version),
            #~ 'release': ('setup.py', release)}},
)

