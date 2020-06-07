from io import StringIO
import logging

from unittest import TextTestResult
from tcms_api.plugin_helpers import Backend


class TestResult(TextTestResult):
    # pylint: disable=too-many-instance-attributes
    def __init__(self, stream=None, descriptions=None, verbosity=2, **kwargs):
        super().__init__(stream=stream, descriptions=descriptions,
                         verbosity=verbosity, **kwargs)
        self.backend = Backend(prefix='[DJANGO ] ')
        self.test_case_id = 0
        self.comment = '''
        Result recorded via Kiwi TCMS Django test runner reporting plugin
        '''
        self.status_id = 0
        self.trace_back = ''
        self.skip_reason = ''
        self.expected_failure_comment = ''
        self.unexpected_success_comment = ''
        self.test_execution_id = 0
        self.failed_subtest = False

    def startTestRun(self):
        self.backend.configure()

    def startTest(self, test):
        super().startTest(test)
        test_case, _ = self.backend.test_case_get_or_create(
            self.getDescription(test))
        test_case_id = test_case['id']
        self.test_case_id = test_case_id
        self.backend.add_test_case_to_plan(
            test_case_id,
            self.backend.plan_id)
        test_execution_id = self.backend.add_test_case_to_run(
            test_case_id,
            self.backend.run_id)
        self.test_execution_id = test_execution_id

    def addSuccess(self, test):
        super().addSuccess(test)
        self.status_id = self.backend.get_status_id('PASSED')

    def addError(self, test, err):
        super().addError(test, err)
        self.status_id = self.backend.get_status_id('FAILED')
        self.trace_back = self.errors[-1][1]

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.status_id = self.backend.get_status_id('FAILED')
        self.trace_back = self.failures[-1][1]

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.status_id = self.backend.get_status_id('WAIVED')
        self.skip_reason = 'Reason test was skipped: {0!r}'.format(reason)

    def addExpectedFailure(self, test, err):
        super().addExpectedFailure(test, err)
        self.status_id = self.backend.get_status_id('FAILED')
        self.expected_failure_comment = 'Test failed as expected'
        self.trace_back = self.expectedFailures[-1][1]

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        self.unexpected_success_comment = 'Test unexpectedly passed.'

    def addSubTest(self, test, subtest, err):
        if err is not None:
            self.failed_subtest = True
            if issubclass(err[0], test.failureException):
                self.backend.update_test_execution(
                    self.test_execution_id,
                    self.backend.get_status_id('FAILED'),
                    "Subtest failure:{0}".format(
                        self._exc_info_to_string(err, test)))
            else:
                self.backend.update_test_execution(
                    self.test_execution_id,
                    self.backend.get_status_id('FAILED'),
                    "Subtest error:{0}".format(
                        self._exc_info_to_string(err, test)))

        super().addSubTest(test, subtest, err)

    def stopTest(self, test):
        if self.failed_subtest:
            self.failed_subtest = False
            return

        self.backend.update_test_execution(self.test_execution_id,
                                           self.status_id,
                                           self.comment)
        if self.trace_back != '':
            self.backend.add_comment(
                self.test_execution_id, self.trace_back)
            self.trace_back = ''
            if self.expected_failure_comment != '':
                self.backend.add_comment(
                    self.test_execution_id, self.expected_failure_comment)
                self.expected_failure_comment = ''
        elif self.skip_reason != '':
            self.backend.add_comment(
                self.test_execution_id, self.skip_reason)
            self.skip_reason = ''
        elif self.unexpected_success_comment != '':
            self.backend.add_comment(
                self.test_execution_id, self.unexpected_success_comment)
            self.unexpected_success_comment = ''

    def stopTestRun(self):
        self.backend.finish_test_run()


class DebugSQLTestResult(TestResult):
    def __init__(self, stream, descriptions, verbosity, **kwargs):
        self.logger = logging.getLogger('django.db.backends')
        self.logger.setLevel(logging.DEBUG)
        self.debug_sql_stream = StringIO()
        self.handler = logging.StreamHandler(self.debug_sql_stream)
        super().__init__(stream=stream, descriptions=descriptions,
                         verbosity=2, **kwargs)

    def startTest(self, test):
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
