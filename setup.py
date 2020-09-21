#!/usr/bin/env python
from codecs import open
import os
from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Plugins",
    "Intended Audience :: Developers",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "License :: OSI Approved :: Apache Software License",
    "Topic :: Software Development :: Testing",
]

filepath = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(filepath, "genbip", "__version__.py"), "r", "utf-8") as f:
    exec(f.read(), about)

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=None,
    classifiers=classifiers,
    keywords="bi-partite graph generation python",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    license=about["__license__"],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=["numpy>=1.19.0"],
    entry_points={"console_scripts": ["codecov=codecov:main"]},
)
