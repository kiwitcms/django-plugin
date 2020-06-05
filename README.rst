Django Test Runner plugin for Kiwi TCMS
=======================================

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