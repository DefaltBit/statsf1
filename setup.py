# !/usr/bin/python3
# coding: utf_8

""" Setups library and install dependencies """

from setuptools import setup, find_packages

LITTLE_DESCRIPTION = "Bot that explores db and predicts future races"
DESCRIPTION = \
    "STATSF1\n" + LITTLE_DESCRIPTION + "\n\
    Install\n\
    - $ pip3 install . --upgrade --force-reinstall, from the source\n\
    Questions and issues\n\
    The Github issue tracker is only for bug reports and feature requests."
VERSION = open("VERSION").readlines()[0]
VERSION_NUMBER = VERSION.split(" ")[0]

setup(
    name="statsf1",
    version=VERSION_NUMBER,
    author="sirfoga",
    author_email="sirfoga@protonmail.com",
    description=LITTLE_DESCRIPTION,
    long_description=DESCRIPTION,
    keywords="f1 scikit-learn mongodb",
    url="https://github.com/sirfoga/statsf1",
    packages=find_packages(exclude=["tests"]),
    test_suite="tests"
)
