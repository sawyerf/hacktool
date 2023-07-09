from setuptools import setup, find_packages
from hacktool.version import __version__
from sys import platform

setup(
    name='hacktool',
    version=__version__,
    packages=find_packages(include=[
        'hacktool', 'hacktool.*',
    ]),
    entry_points={
        'console_scripts': [
            'resh=hacktool.resh:main',
            'httplog=hacktool.httplog:main',
        ]
    }
)
