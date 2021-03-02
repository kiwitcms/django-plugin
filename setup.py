#!/usr/bin/env python
from setuptools import setup

with open("README.rst") as readme:
    LONG_DESCRIPTION = readme.read()

REQUIREMENTS = open('requirements.txt').readlines()

setup(name='kiwitcms-django-plugin',
      version='10.0',
      packages=['tcms_django_plugin'],
      description='Django test runner plugin for Kiwi TCMS',
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/x-rst',
      author='Bryan Mutai',
      author_email='work@bryanmutai.co',
      maintainer='Kiwi TCMS',
      maintainer_email='info@kiwitcms.org',
      license='GPLv3',
      url='https://github.com/kiwitcms/django-plugin',
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
