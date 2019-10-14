#!/usr/bin/env python
from setuptools import setup

with open('README', 'r') as tldr:
    long_description = tldr.read()
    setup(
        name='getweather',
        version='1.0',
        description='API calls to OpeanWeather.org',
        long_description=long_description,
        author='Yuri Neves',
        author_email='pisces.period@gmail.com',
        packages=['getweather'],
        install_requires[
            'pyown'
        ]
    )
