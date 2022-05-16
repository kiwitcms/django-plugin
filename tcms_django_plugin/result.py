from unittest import TextTestResult
from django.test.runner import DebugSQLTextTestResult as DjangoDebugSQLResult
from tcms_api import plugin_helpers

from .version import __version__


class Backend(plugin_helpers.Backend):
    name = "kiwitcms-django-plugin"
    version = __version__


class KiwiTCMSIntegrationMixin:  # pylint: disable=invalid-name
    prefix = ''

    def __init__(self, stream, descriptions, verbosity, **kwargs):
        super().__init__(stream, descriptions, verbosity, **kwargs)
        self.backend = Backend(prefix=self.prefix)
        self.comment = ''
        self.status_id = 0
        self.test_executions = []
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
        self.test_executions = self.backend.add_test_case_to_run(
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
        expected_failure = self.expectedFailures[-1][1]
        self.comment = f'Expected failure:\n\n{expected_failure}'

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        self.status_id = self.backend.get_status_id('FAILED')
        self.comment = 'Test unexpectedly passed.'

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err:
            self.failed_subtest = True
            exception_info = self._exc_info_to_string(err, test)

            if issubclass(err[0], test.failureException):
                status_id = self.backend.get_status_id('FAILED')
                for execution in self.test_executions:
                    self.backend.update_test_execution(
                        execution["id"],
                        status_id,
                        f"Subtest failure:{exception_info}")
            else:
                status_id = self.backend.get_status_id('ERROR')
                for execution in self.test_executions:
                    self.backend.update_test_execution(
                        execution["id"],
                        status_id,
                        f"Subtest error:{exception_info}")

    def stopTest(self, test):
        super().stopTest(test)
        if self.failed_subtest:
            self.failed_subtest = False
            return

        for execution in self.test_executions:
            self.backend.update_test_execution(execution["id"],
                                               self.status_id,
                                               self.comment)
        self.comment = ''

    def stopTestRun(self):
        super().stopTestRun()
        self.backend.finish_test_run()


class TestResult(KiwiTCMSIntegrationMixin, TextTestResult):
    prefix = '[DJANGO]'


class DebugSQLTestResult(KiwiTCMSIntegrationMixin, DjangoDebugSQLResult):
    prefix = '[DJANGO --debug-sql]'

    def addError(self, test, err):
        super().addError(test, err)
        self.debug_sql_stream.seek(0)
        for execution in self.test_executions:
            self.backend.add_comment(execution["id"],
                                     self.debug_sql_stream.read())

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.debug_sql_stream.seek(0)
        for execution in self.test_executions:
            self.backend.add_comment(execution["id"],
                                     self.debug_sql_stream.read())

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err:
            self.debug_sql_stream.seek(0)
            for execution in self.test_executions:
                self.backend.add_comment(execution["id"],
                                         self.debug_sql_stream.read())
