#!/usr/bin/env python
import os
import sys
from setuptools import setup


def get_version():
    version = open(os.path.join('tcms_django_plugin', 'version.py')).read()
    return version.replace(
        ' ', ''
    ).replace('__version__=', '').strip().strip("'").strip('"')


with open("README.rst") as readme:
    LONG_DESCRIPTION = readme.read()

REQUIREMENTS = open('requirements.txt').readlines()

setup(name='tcms-django-plugin',
      version=get_version(),
      packages=['tcms_django_plugin'],
      description='Django test runner plugin for Kiwi TCMS',
      long_description=LONG_DESCRIPTION,
      long_description_content_type="text/x-rst",
      maintainer='Kiwi TCMS',
      maintainer_email='info@kiwitcms.org',
      license='GPLv3',
      url='https://github.com/brymut/tcms-django-plugin',
      python_requires='>=3.6',
      install_requires=REQUIREMENTS,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.7',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Software Development :: Testing',
      ])
