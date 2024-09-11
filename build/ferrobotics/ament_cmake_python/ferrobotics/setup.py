from setuptools import find_packages
from setuptools import setup

setup(
    name='ferrobotics',
    version='0.0.0',
    packages=find_packages(
        include=('ferrobotics', 'ferrobotics.*')),
)
