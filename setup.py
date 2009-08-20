#!/usr/bin/env python

import sys
import os
try:
    import subprocess
    has_subprocess = True
except:
    has_subprocess = False
import shutil

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup
from setuptools import Feature
from distutils.cmd import Command
from distutils.command.build_ext import build_ext
from distutils.errors import CCompilerError
from distutils.errors import DistutilsPlatformError, DistutilsExecError
from distutils.core import Extension

import mongoobject

requirements = []
try:
    import pymongo
except ImportError:
    requirements.append("pymongo")

version = 0.1

f = open("README.md")
try:
    try:
        readme_content = f.read()
    except:
        readme_content = ""
finally:
    f.close()


class GenerateDoc(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        path = "doc/%s" % version

        shutil.rmtree("doc", ignore_errors=True)
        os.makedirs(path)

        if has_subprocess:
            subprocess.call(["epydoc", "--config", "epydoc-config", "-o", path])
        else:
            print """
`setup.py doc` is not supported for this version of Python.

Please ask in the user forums for help.
"""

# thanks to mike from mongodb for the setup.py template
setup(
    name="mongodbobject",
    version=version,
    description="Object wrapper for Pymongo",
    long_description=readme_content,
    author="Marc Boeker | ONchestra.com",
    author_email="marc.boeker@onchestra.com",
    url="http://github.com/marcboeker/mongodb-object",
    packages=["mongodbobject"],
    install_requires=requirements,
    license="Apache License, Version 2.0",
    #test_suite="nose.collector",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Database"],
    cmdclass={"doc": GenerateDoc})