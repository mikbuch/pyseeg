#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-


__author__ = 'Mikolaj Buchwald, mikolaj.buchwald@gmail.com'


from setuptools import setup, find_packages


setup(
    name="PysEEG",
    version="0.0.1",
    description="PysEEG is tool for simple EEG analysis and BCI utility.",
    license="BSD",
    keywords="EEG BCI filtering plotting online realtime",
    url="http://mikbuch.github.io/pyseeg",
    packages=find_packages(exclude=['examples', 'docs']),
    include_package_data=True,
    # test_suite='pymri.tests.runtests.make_test_suite',
    install_requires = ["scipy"],
)
