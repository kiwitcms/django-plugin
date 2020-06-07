from io import StringIO
import logging

from unittest import TextTestResult
from tcms_api.plugin_helpers import Backend


class TestResult(TextTestResult):
    def __init__(self, stream=None, descriptions=None, verbosity=2, **kwargs):
        super().__init__(stream=stream, descriptions=descriptions,
                         verbosity=verbosity, **kwargs)
        self.backend = Backend(prefix='[DJANGO ] ')
        self.comment = ''
        self.status_id = 0
        self.test_execution_id = 0
        self.failed_subtest = False

    def startTestRun(self):
        super().startTestRun()
        self.backend.configure()

    def startTest(self, test):
        super().startTest(test)
        test_case, _ = self.backend.test_case_get_or_create(
            self.getDescription(test))
        self.backend.add_test_case_to_plan(
            test_case['id'],
            self.backend.plan_id)
        self.test_execution_id = self.backend.add_test_case_to_run(
            test_case['id'],
            self.backend.run_id)

    def addSuccess(self, test):
        super().addSuccess(test)
        self.status_id = self.backend.get_status_id('PASSED')

    def addError(self, test, err):
        super().addError(test, err)
        self.status_id = self.backend.get_status_id('FAILED')
        self.comment = self.errors[-1][1]

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.status_id = self.backend.get_status_id('FAILED')
        self.comment = self.failures[-1][1]

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.status_id = self.backend.get_status_id('WAIVED')
        self.comment = reason

    def addExpectedFailure(self, test, err):
        super().addExpectedFailure(test, err)
        self.status_id = self.backend.get_status_id('FAILED')
        self.comment = "Test failed as expected.\n\n{0}".format(
            self.expectedFailures[-1][1])

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        self.comment = 'Test unexpectedly passed.'

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
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

    def stopTest(self, test):
        super().stopTest(test)
        if self.failed_subtest:
            self.failed_subtest = False
            return

        self.backend.update_test_execution(self.test_execution_id,
                                           self.status_id,
                                           self.comment)
        self.comment = ''

    def stopTestRun(self):
        super().stopTestRun()
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
