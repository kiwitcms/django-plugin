from unittest.mock import MagicMock
import pathlib
import django
from tcms_django_plugin import TestRunner
from testapp.tests import (TestAppAboutPageTest, TestAppMissingPageTest,
                           TestAppContactPageTest, TestAppIndexPageTest,
                           TestAppBooleanPageTest)


def setup(test_case, method_name):
    django.setup()
    runner = TestRunner()
    suite = runner.test_suite()
    suite.addTest(test_case(methodName=method_name))
    resultclass = runner.get_resultclass()
    resultclass.backend = MagicMock()
    resultclass.backend.plan_id = 1
    resultclass.backend.run_id = 7000
    resultclass.backend.test_case_get_or_create.return_value = [
        {'id': 1000}, True]
    resultclass.backend.add_test_case_to_run.return_value = 3000
    resultclass.backend.get_status_id.return_value = 4000
    results = runner.test_runner(
        resultclass=resultclass,
    ).run(suite)
    return results


def test_when_test_case_passes():
    '''
    assert appropriate API calls were made for a passing testcase
    '''
    results = setup(TestAppAboutPageTest, 'test_about_page')
    results.backend.configure.assert_called_once()
    results.backend.test_case_get_or_create.assert_called_once_with(
        'test_about_page (testapp.tests.TestAppAboutPageTest)')
    results.backend.add_test_case_to_plan.assert_called_once_with(
        1000, 1)
    results.backend.add_test_case_to_run.assert_called_once_with(
        1000, 7000)
    results.backend.get_status_id.assert_called_once_with(
        "PASSED")
    results.backend.update_test_execution.assert_called_once_with(
        3000, 4000, '\n        Result recor\
ded via Kiwi TCMS Django test runner reporting plugin\n        ')
    results.backend.finish_test_run.assert_called_once()


def test_when_test_case_fails():
    '''
    assert appropriate API calls were made for a failing testcase
    '''
    results = setup(TestAppMissingPageTest, 'test_missing_page')
    results.backend.configure.assert_called_once()
    results.backend.test_case_get_or_create.assert_called_once_with(
        'test_missing_page (testapp.tests.TestAppMissingPageTest)')
    results.backend.add_test_case_to_plan.assert_called_once_with(
        1000, 1)
    results.backend.add_test_case_to_run.assert_called_once_with(
        1000, 7000)
    results.backend.get_status_id.assert_called_once_with(
        "FAILED")
    results.backend.update_test_execution.assert_called_once_with(
        3000, 4000, '\n        Result recor\
ded via Kiwi TCMS Django test runner reporting plugin\n        ')
    results.backend.finish_test_run.assert_called_once()


def test_when_test_case_has_error():
    '''
    assert appropriate API calls were made for a testcase with an error
    '''
    results = setup(TestAppContactPageTest, 'test_contact_page')
    results.backend.configure.assert_called_once()
    results.backend.test_case_get_or_create.assert_called_once_with(
        'test_contact_page (testapp.tests.TestAppContactPageTest)')
    results.backend.add_test_case_to_plan.assert_called_once_with(
        1000, 1)
    results.backend.add_test_case_to_run.assert_called_once_with(
        1000, 7000)
    results.backend.get_status_id.assert_called_once_with(
        "FAILED")
    results.backend.update_test_execution.assert_called_once_with(
        3000, 4000, '\n        Result recor\
ded via Kiwi TCMS Django test runner reporting plugin\n        ')
    results.backend.finish_test_run.assert_called_once()


def test_when_test_case_is_skipped():
    '''
    assert appropriate API calls were made for a skipped testcase
    '''
    results = setup(TestAppIndexPageTest, 'test_nothing')
    results.backend.configure.assert_called_once()
    results.backend.test_case_get_or_create.assert_called_once_with(
        'test_nothing (testapp.tests.TestAppIndexPageTest)')
    results.backend.add_test_case_to_plan.assert_called_once_with(
        1000, 1)
    results.backend.add_test_case_to_run.assert_called_once_with(
        1000, 7000)
    results.backend.get_status_id.assert_called_once_with(
        "WAIVED")
    results.backend.update_test_execution.assert_called_once_with(
        3000, 4000, '\n        Result recor\
ded via Kiwi TCMS Django test runner reporting plugin\n        ')
    results.backend.finish_test_run.assert_called_once()


def test_when_test_case_fails_as_expected():
    '''
    assert appropriate API calls were made
    for a failing testcase that fails as expected
    '''
    results = setup(TestAppMissingPageTest, 'test_fail')
    results.backend.configure.assert_called_once()
    results.backend.test_case_get_or_create.assert_called_once_with(
        'test_fail (testapp.tests.TestAppMissingPageTest)')
    results.backend.add_test_case_to_plan.assert_called_once_with(
        1000, 1)
    results.backend.add_test_case_to_run.assert_called_once_with(
        1000, 7000)
    results.backend.get_status_id.assert_called_once_with(
        "FAILED")
    results.backend.update_test_execution.assert_called_once_with(
        3000, 4000, '\n        Result recor\
ded via Kiwi TCMS Django test runner reporting plugin\n        ')
    results.backend.finish_test_run.assert_called_once()


def test_when_test_case_passes_unexpectedly():
    '''
    assert appropriate API calls were made
    for a failing testcase that passes unexpectedly
    '''
    results = setup(TestAppMissingPageTest, 'test_unexpected_success')
    results.backend.configure.assert_called_once()
    results.backend.test_case_get_or_create.assert_called_once_with(
        'test_unexpected_success (testapp.tests.TestAppMissingPageTest)')
    results.backend.add_test_case_to_plan.assert_called_once_with(
        1000, 1)
    results.backend.add_test_case_to_run.assert_called_once_with(
        1000, 7000)
    results.backend.get_status_id.assert_called_once_with(
        "FAILED")
    results.backend.update_test_execution.assert_called_once_with(
        3000, 4000, '\n        Result recor\
ded via Kiwi TCMS Django test runner reporting plugin\n        ')
    results.backend.finish_test_run.assert_called_once()


def test_when_test_case_has_subtests():
    '''
     assert appropriate API calls were made
     for a testcase that has 2 passing subtests and 1 failing subtest
    '''
    results = setup(TestAppBooleanPageTest, 'test_get_correct_boolean')
    results.backend.configure.assert_called_once()
    results.backend.test_case_get_or_create.assert_called_once_with(
        'test_get_correct_boolean (testapp.tests.TestAppBooleanPageTest)')
    results.backend.add_test_case_to_plan.assert_called_once_with(
        1000, 1)
    results.backend.add_test_case_to_run.assert_called_once_with(
        1000, 7000)
    results.backend.get_status_id.assert_called_once_with(
        "FAILED")
    results.backend.update_test_execution.assert_called_once_with(
        3000, 4000, 'Subtest failure:Traceback (most recent call last):\
\n  File "{0}/testapp/tests.py",\
 line 56, in test_get_correct_boolean\n    self.assertEqual\
(invalid_response.content, b\'invalid\')\nAssertionError: \
b\'invald\' != b\'invalid\'\n'.format(pathlib.Path().absolute()))
    results.backend.finish_test_run.assert_called_once()


if __name__ == '__main__':
    test_when_test_case_passes()
    test_when_test_case_fails()
    test_when_test_case_has_error()
    test_when_test_case_is_skipped()
    test_when_test_case_fails_as_expected()
    test_when_test_case_passes_unexpectedly()
    test_when_test_case_has_subtests()
