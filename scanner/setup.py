#!/usr/bin/env python
from setuptools import setup

with open("README, 'r') as tldr:
    long_description=tldr.read()

setup(
	name='scanner',
	version='1.0',
	description='NMAP Port Scanner',
    long_description=long_description,
	author='Yuri Neves',
	author_email='pisces.period@gmail.com',
	packages=['scanner'],
	install_requires[
		'nmap'
	]
)