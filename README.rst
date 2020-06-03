Django Test Runner plugin for Kiwi TCMS
=======================================

When you run ./manage.py test, Django looks at the TEST_RUNNER setting to determine what to do.
By default, TEST_RUNNER points to 'django.test.runner.DiscoverRunner'.

This package provides an overriden version of the default django test runner (DiscoverRunner)
that on top of its expected functionality reports the test results to Kiwi TCMS via the Kiwi TCMS API.

INSTALLATION
------------
First, install the following package using the command:

::

    pip install tcms-django-plugin


Configuration and Environment
-----------------------------
To add reporting from tests to Kiwi TCMS via this plugin's test runner, in your django settings.py,
add the following setting to change from the default test runner.

::

    TEST_RUNNER = 'tcms_django_plugin.TestRunner'


A minimal config file ~/.tcms.conf is required to set up communication with the TCMS API:

::

    [tcms]
    url = https://tcms.server/xml-rpc/
    username = your-username
    password = your-password


The tcms-api depends on various environment variables to configure and report
information about the test plans/cases/runs and executions back to Kiwi TCMS server.

For product information use one of the following environment variables:

- TCMS_PRODUCT
- TRAVIS_REPO_SLUG
- JOB_NAME

For version information use one of the following environment variables:

- TCMS_PRODUCT_VERSION
- TRAVIS_COMMIT
- TRAVIS_PULL_REQUEST_SHA
- GIT_COMMIT

For build information use one of the following environment variables:

- TCMS_BUILD
- TRAVIS_BUILD_NUMBER
- BUILD_NUMBER


For more information about the tcms-api visit https://github.com/kiwitcms/tcms-api
 