from setuptools import setup, find_packages
from hacktool.version import __version__

setup(
    name='hacktool',
    version=__version__,
    packages=find_packages(include=[
        'hacktool', 'autocheck.*',
    ]),
    install_requires=[
        
    ]
    entry_points={
        'console_scripts': [
            'resh=hacktool.resh:main',
            'httplog=hacktool.httplog:main',
        ]
    }
)
