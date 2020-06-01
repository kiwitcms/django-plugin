# Copyright (c) 2020 Bryan Mutai , <work@bryanmutai.co>

# Licensed under the GPLv3: https://www.gnu.org/licenses/gpl.html


from tcms_api.plugin_helpers import Backend
from django.test.runner import DiscoverRunner, DebugSQLTextTestResult
from io import StringIO
import logging
from unittest import TextTestRunner, TextTestResult

try:
    import ipdb as pdb
except ImportError:
    import pdb


# BIG BIG PROBLEM WITH MISSING RPC METHOD: <Fault -32601: 'Method not found: "PlanType.create"'>
# Figure out subtests
class TestResult(TextTestResult):

    def __init__(self, stream=None, descriptions=None, verbosity=2, **kwargs):
        super().__init__(stream=stream, descriptions=descriptions, verbosity=verbosity, **kwargs)
        self.tcms_api_backend = Backend(prefix='[DJANGO ] ')
        self.test_case_id = 0
        self.comment = 'Result recorded via Kiwi TCMS Django test runner reporting plugin'
        self.status_id = 0
        self.trace_back = ''
        self.skip_reason = ''
        self.expected_failure_comment = ''
        self.unexpected_success_comment = ''
        self.test_execution_id = 0

    def startTestRun(self):
        self.tcms_api_backend.configure()
        self.stream.writeln(
            'TCMS API configured. Starting Test run...')

    def startTest(self, test):
        super().startTest(test)
        test_case, _ = self.tcms_api_backend.test_case_get_or_create(
            self.getDescription(test))
        test_case_id = test_case['id']
        self.test_case_id = test_case_id
        self.stream.writeln(
            '\nTCMS Test case ID: {0!r}'.format(self.test_case_id))
        self.stream.writeln('TCMS Test run ID: {0!r}'.format(
            self.tcms_api_backend.run_id))
        self.tcms_api_backend.add_test_case_to_plan(test_case_id,
                                                    self.tcms_api_backend.plan_id)
        test_execution_id = self.tcms_api_backend.add_test_case_to_run(
            test_case_id,
            self.tcms_api_backend.run_id)
        self.test_execution_id = test_execution_id

    def addSuccess(self, test):
        super().addSuccess(test)
        self.status_id = self.tcms_api_backend.get_status_id('PASSED')

    def addError(self, test, err):
        super().addError(test, err)
        self.status_id = self.tcms_api_backend.get_status_id('FAILED')
        self.trace_back = self.errors[-1][1]

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.status_id = self.tcms_api_backend.get_status_id('FAILED')
        self.trace_back = self.failures[-1][1]

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.status_id = self.tcms_api_backend.get_status_id('WAIVED')
        self.skip_reason = 'Reason test was skipped: {0!r}'.format(reason)

    def addExpectedFailure(self, test, err):
        super().addExpectedFailure(test, err)
        self.status_id = self.tcms_api_backend.get_status_id('FAILED')
        self.expected_failure_comment = 'Test failed as expected'
        self.trace_back = self.expectedFailures[-1][1]

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        self.unexpected_success_comment = 'Test unexpectedly passed.'

    def stopTest(self, test):
        self.tcms_api_backend.update_test_execution(self.test_execution_id,
                                                    self.status_id,
                                                    self.comment)
        if (self.trace_back != ''):
            self.tcms_api_backend.add_comment(
                self.test_execution_id, self.trace_back)
            self.trace_back = ''
            if(self.expected_failure_comment != ''):
                self.tcms_api_backend.add_comment(
                    self.test_execution_id, self.expected_failure_comment)
                self.expected_failure_comment = ''
        elif(self.skip_reason != ''):
            self.tcms_api_backend.add_comment(
                self.test_execution_id, self.skip_reason)
            self.skip_reason = ''
        elif(self.unexpected_success_comment != ''):
            self.tcms_api_backend.add_comment(
                self.test_execution_id, self.unexpected_success_comment)
            self.unexpected_success_comment = ''

    def stopTestRun(self):
        self.tcms_api_backend.finish_test_run()


class DebugSQLTestResult(TestResult):
    def __init__(self, stream, descriptions, verbosity, **kwargs):
        self.logger = logging.getLogger('django.db.backends')
        self.logger.setLevel(logging.DEBUG)
        super().__init__(stream=stream, descriptions=descriptions, verbosity=2, **kwargs)

    def startTest(self, test):
        self.debug_sql_stream = StringIO()
        self.handler = logging.StreamHandler(self.debug_sql_stream)
        self.logger.addHandler(self.handler)
        super().startTest(test)

    def stopTest(self, test):
        super().stopTest(test)
        self.logger.removeHandler(self.handler)
        if self.showAll:
            self.debug_sql_stream.seek(0)
            self.stream.write(self.debug_sql_stream.read())
            self.stream.writeln(self.separator2)

    def addError(self, test, err):
        super().addError(test, err)
        self.debug_sql_stream.seek(0)
        self.errors[-1] = self.errors[-1] + (self.debug_sql_stream.read(),)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.debug_sql_stream.seek(0)
        self.failures[-1] = self.failures[-1] + (self.debug_sql_stream.read(),)

    def printErrorList(self, flavour, errors):
        for test, err, sql_debug in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln("%s: %s" %
                                (flavour, self.getDescription(test)))
            self.stream.writeln(self.separator2)
            self.stream.writeln(err)
            self.stream.writeln(self.separator2)
            self.stream.writeln(sql_debug)


class PDBDebugResult(TestResult):
    def addError(self, test, err):
        super().addError(test, err)
        self.debug(err)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.debug(err)

    def debug(self, error):
        exc_type, exc_value, traceback = error
        print("\nOpening PDB: %r" % exc_value)
        pdb.post_mortem(traceback)


class TestRunner(DiscoverRunner):

    def __init__(self, pattern=None, top_level=None, verbosity=1,
                 interactive=True, failfast=False, keepdb=False,
                 reverse=False, debug_mode=False, debug_sql=False, parallel=0,
                 tags=None, exclude_tags=None, test_name_patterns=None,
                 pdb=False, buffer=False, **kwargs):
        super().__init__(pattern=pattern, top_level=top_level, verbosity=verbosity,
                         interactive=interactive, failfast=failfast, keepdb=keepdb,
                         reverse=reverse, debug_mode=debug_mode, debug_sql=debug_sql, parallel=parallel,
                         tags=tags, exclude_tags=exclude_tags, test_name_patterns=test_name_patterns,
                         pdb=pdb, buffer=buffer, **kwargs)

    def get_resultclass(self):
        if self.debug_sql:
            return DebugSQLTestResult
        elif self.pdb:
            return PDBDebugResult
        else:
            return TestResult

    def get_test_runner_kwargs(self):
        return {
            'failfast': self.failfast,
            'resultclass': self.get_resultclass(),
            'verbosity': self.verbosity,
        }

    def run_suite(self, suite, **kwargs):
        kwargs = self.get_test_runner_kwargs()
        runner = self.test_runner(**kwargs)
        results = runner.run(suite)
        return results
