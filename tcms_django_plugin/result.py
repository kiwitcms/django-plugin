from unittest import TextTestResult
from django.test.runner import DebugSQLTextTestResult as DjangoDebugSQLResult

from tcms_api.plugin_helpers import Backend


class KiwiTCMSIntegrationMixin:  # pylint: disable=invalid-name
    prefix = ''

    def __init__(self, stream, descriptions, verbosity, **kwargs):
        super().__init__(stream, descriptions, verbosity, **kwargs)
        self.backend = Backend(prefix=self.prefix)
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
        self.status_id = self.backend.get_status_id('ERROR')
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
        self.status_id = self.backend.get_status_id('PASSED')
        self.comment = 'Expected failure:\n\n{0}'.format(
            self.expectedFailures[-1][1])

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        self.status_id = self.backend.get_status_id('FAILED')
        self.comment = 'Test unexpectedly passed.'

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err:
            self.failed_subtest = True
            if issubclass(err[0], test.failureException):
                status_id = self.backend.get_status_id('FAILED')
                self.backend.update_test_execution(
                    self.test_execution_id,
                    status_id,
                    "Subtest failure:{0}".format(
                        self._exc_info_to_string(err, test)))
            else:
                status_id = self.backend.get_status_id('ERROR')
                self.backend.update_test_execution(
                    self.test_execution_id,
                    status_id,
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


class TestResult(KiwiTCMSIntegrationMixin, TextTestResult):
    prefix = '[DJANGO] '


class DebugSQLTestResult(KiwiTCMSIntegrationMixin, DjangoDebugSQLResult):
    prefix = '[DJANGO --debug-sql] '

    def addError(self, test, err):
        super().addError(test, err)
        self.debug_sql_stream.seek(0)
        self.backend.add_comment(self.test_execution_id,
                                 self.debug_sql_stream.read())

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.debug_sql_stream.seek(0)
        self.backend.add_comment(self.test_execution_id,
                                 self.debug_sql_stream.read())

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err:
            self.debug_sql_stream.seek(0)
            self.backend.add_comment(self.test_execution_id,
                                     self.debug_sql_stream.read())
