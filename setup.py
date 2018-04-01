"""Setup script for itrack"""
from setuptools import setup

setup(

    name='itrack',

    version='0.0.1',

    packages=[
        'itrack'
    ],

    package_dir={'': 'src'},

    package_data={
        'itrack': ['config.json']
    },

    author='Vincent Moret',

    author_email='moret.vincent@gmail.com',

    url='https://github.com/vmoret/itrack',

    install_requires=[
        'requests',
        'xlrd',
        'numpy',
        'pandas'
    ]
)
