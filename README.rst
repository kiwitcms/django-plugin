Django Test Runner plugin for Kiwi TCMS
=======================================

.. image:: https://tidelift.com/badges/package/pypi/kiwitcms-django-plugin
    :target: https://tidelift.com/subscription/pkg/kiwitcms-django-plugin?utm_source=pypi-kiwitcms-django-plugin&utm_medium=github&utm_campaign=readme
    :alt: Tidelift

.. image:: https://img.shields.io/twitter/follow/KiwiTCMS.svg
    :target: https://twitter.com/KiwiTCMS
    :alt: Kiwi TCMS on Twitter


This package provides a Django test runner that reports the test results to
`Kiwi TCMS <https://kiwitcms.org>`_.


Installation
------------

::

    pip install kiwitcms-django-plugin


Configuration and environment
-----------------------------


Minimal config file ``~/.tcms.conf``::

    [tcms]
    url = https://tcms.server/xml-rpc/
    username = your-username
    password = your-password

For more info see `tcms-api docs <https://tcms-api.readthedocs.io>`_.

Usage
-----

In ``settings.py`` add the following::

    TEST_RUNNER = 'tcms_django_plugin.TestRunner'

When you run ``./manage.py test`` Django looks at the ``TEST_RUNNER`` setting
to determine what to do.


Changelog
---------

v1.1.2 (25 June 2020)
~~~~~~~~~~~~~~~~~~~~~

- Update to tcms-api v8.4.0


v1.1.1 (25 June 2020)
~~~~~~~~~~~~~~~~~~~~~

- Initial release, thanks to Bryan Mutai
