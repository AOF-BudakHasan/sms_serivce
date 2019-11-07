#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sms-service",
    version="0.0.5",
    author="Hasan Budak",
    author_email="budak.hasan.apc@gmail.com",
    description="Send text as SMS with Callturk adapter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AOF-BudakHasan/sms_service",
    packages=setuptools.find_packages(exclude=['tests', 'test.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='Sms sender, Callturk sms sender adapter',
    package_dir={"sms_service": "sms_service"},
    python_requires='>=3.0',
    test_suite='sms_service/tests/test.py',
    setup_requires=['wheel'],
    install_requires=[
        'requests>=2.0',
    ],
    include_package_data=True
)
