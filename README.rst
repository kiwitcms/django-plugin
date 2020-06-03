Django Test Runner plugin for Kiwi TCMS
=======================================

This package provides an overriden version of the default django test runner (DiscoverRunner)
that on top of its expected functionality reports the test results to Kiwi TCMS via the Kiwi TCMS API.

INSTALLATION
------------

::

    pip install 


Configuration and Environment
-----------------------------
Minimal config file ~/.tcms.conf:

[tcms]
url = https://tcms.server/xml-rpc/
username = your-username
password = your-password


The tcms-api depends on various environment variables to configure and report
information about the test plans/cases/runs and executions back to Kiwi TCMS server.


Exception: Product name not defined, missing one of TCMS_PRODUCT, TRAVIS_REPO_SLUG or JOB_NAME
export TCMS_PRODUCT=tcms-django-plugin
Exception: Version value not defined, missing one of TCMS_PRODUCT_VERSION, TRAVIS_COMMIT, TRAVIS_PULL_REQUEST_SHA or GIT_COMMIT
export TCMS_PRODUCT_VERSION=0.1
Exception: Build number not defined, missing one of TCMS_BUILD, TRAVIS_BUILD_NUMBER or BUILD_NUMBER
export TCMS_BUILD=1
 