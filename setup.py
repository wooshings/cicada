#!/usr/bin/env python
from setuptools import setup

setup(
    name='cicada',
    version='0.1.2',
    url='https://github.com/wooshdude/cicada',
    author='wooshings',
    description=(
        'Easy to use library for building Escape Game puzzles using MQTT.'
    ),
    long_description=open('README.md').read(),
    include_package_data=True,
    packages=['Cicada'],
    install_requires=['paho-mqtt','RPi.GPIO']
)
