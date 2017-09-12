# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='discfit',
    version='0.1.3',
    description='Disc permeameter fitting program',
    long_description=long_description,
    url='https://github.com/sekika/discfit',
    author='Katsutoshi Seki',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='Disc permeameter',
    packages=['discfit'],
    install_requires=['numpy', 'scipy'],
    entry_points={  
        'console_scripts':  
            'discfit = discfit.main:main'  
    },
)
