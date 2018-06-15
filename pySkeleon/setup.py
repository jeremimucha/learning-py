# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()


setup(
    name='NAME',
    version='0.1.0',
    description='short description',
    long_description=readme,
    author='Jeremi Mucha',
    author_email='jeremi.mucha@',
    url='',
    license='No license',
    packages=find_packages(exclude=('tests', 'docs', 'etc', 'bin'))
)
