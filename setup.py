from setuptools import setup

from sphinx.setup_command import BuildDoc

name='PSIO'
version='0.1'
release='dev'

setup(
    name='PSIO',
    version='0.1dev',
    author='Ch.Rosemann',
    author_email='christoph.rosemann@desy.de',
    packages=['psio','psio.test',],
    scripts=['bin/counting_bad_pixels.py',
        'bin/simple_file_viewer.py',
        'bin/simpleViewerG.ui',
        'bin/simpleViewerGUI.py',
        'bin/stupid_gisaxs-p03.py'],
    description='Module to facilitate access for photon science data in different formats.', 
    license='LICENSE',
    long_description=open('README').read(),
    data_files=[('.', ['COPYRIGHT','LICENCSE']), ],
    cmdclass={'build_sphinx': BuildDoc,},
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release)}},
)

