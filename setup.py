#!/usr/bin/env python
import codecs
import os
import re
from setuptools import setup


def read(*parts):
    return codecs.open(os.path.join(os.path.dirname(__file__), *parts), encoding='utf8').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='dxr-cmd',
    description='Command-line tool for querying DXR.',
    long_description=read('README.rst'),
    version=find_version('dxr.py'),
    py_modules=['dxr'],
    author='Michael Kelly',
    author_email='me@mkelly.me',
    url='https://github.com/Osmose/dxr',
    license='MIT',
    install_requires=[
        'blessings>=1.6',
        'requests>=2.5.1',
        'docopt>=0.6.2',
        'pygments>=2.0.2',
        'pyopenssl>=0.13',
        'ndg-httpsclient>=0.3.2',
        'pyasn1>=0.1.6'
    ],
    include_package_data=True,
    entry_points={
      'console_scripts': [
          'dxr = dxr:main'
      ]
   }
)
