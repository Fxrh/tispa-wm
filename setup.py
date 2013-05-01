#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name="tispa",
    version="0.5",
    description="A pure-Python dbus controllable tiling window manager.",
    classifiers=[
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GPL3 License",
        "Development Status :: 1 - Alpha",
        "Programming Language :: Python",
        "Operating System :: Unix",
        "Topic :: Desktop Environment :: Window Managers",
    ],
    author="Felix Rohrbach",
    author_email="fxrh@gmx.de",
    license="GPL3",
    include_package_data=True,
    packages=find_packages(),
    scripts=[
        "bin/qsh",
        "bin/tispa",
        "bin/tispa-session"
    ],
)
