from setuptools import setup, find_packages
from hacktool.version import __version__
from sys import platform

setup(
    name='hacktool',
    version=__version__,
    packages=find_packages(include=[
        'hacktool', 'hacktool.*',
    ]),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'hacksheet=hacktool.hacksheet:main',
            'hacktool=hacktool.hacktool:main',
            'httpctf=hacktool.httpctf:main',
            'httplog=hacktool.httplog:main',
            'resh=hacktool.resh:main',
        ]
    }
)
