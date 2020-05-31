# Copyright (c) 2020 Alexander Todorov

# Licensed under the GPLv3: https://www.gnu.org/licenses/gpl.html

# from tap.line import Result, Diagnostic
# from tap.parser import Parser

from tcms_api.plugin_helpers import Backend
from django.test.runner import DiscoverRunner, DebugSQLTextTestResult
import io
from unittest import TextTestRunner, TextTestResult

try:
    import ipdb as pdb
except ImportError:
    import pdb


# BIG BIG PROBLEM WITH MISSING RPC METHOD: <Fault -32601: 'Method not found: "PlanType.create"'>


# class DebugSQLTextTestResult(unittest.TextTestResult):
#     def __init__(self, stream, descriptions, verbosity):
#         self.logger = logging.getLogger('django.db.backends')
#         self.logger.setLevel(logging.DEBUG)
#         super().__init__(stream, descriptions, verbosity)

#     def startTest(self, test):
#         self.debug_sql_stream = StringIO()
#         self.handler = logging.StreamHandler(self.debug_sql_stream)
#         self.logger.addHandler(self.handler)
#         super().startTest(test)

#     def stopTest(self, test):
#         super().stopTest(test)
#         self.logger.removeHandler(self.handler)
#         if self.showAll:
#             self.debug_sql_stream.seek(0)
#             self.stream.write(self.debug_sql_stream.read())
#             self.stream.writeln(self.separator2)

#     def addError(self, test, err):
#         super().addError(test, err)
#         self.debug_sql_stream.seek(0)
#         self.errors[-1] = self.errors[-1] + (self.debug_sql_stream.read(),)

#     def addFailure(self, test, err):
#         super().addFailure(test, err)
#         self.debug_sql_stream.seek(0)
#         self.failures[-1] = self.failures[-1] + (self.debug_sql_stream.read(),)

#     def addSubTest(self, test, subtest, err):
#         super().addSubTest(test, subtest, err)
#         if err is not None:
#             self.debug_sql_stream.seek(0)
#             errors = self.failures if issubclass(err[0], test.failureException) else self.errors
#             errors[-1] = errors[-1] + (self.debug_sql_stream.read(),)

#     def printErrorList(self, flavour, errors):
#         for test, err, sql_debug in errors:
#             self.stream.writeln(self.separator1)
#             self.stream.writeln("%s: %s" % (flavour, self.getDescription(test)))
#             self.stream.writeln(self.separator2)
#             self.stream.writeln(err)
#             self.stream.writeln(self.separator2)
#             self.stream.writeln(sql_debug)


class DebugSQLTestResult(DebugSQLTextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream=stream, descriptions=descriptions, verbosity=verbosity)

    def startTest(self, test):
        super().startTest(test)
        # use plugin to start test if neccessary

    def stopTest(self, test):
        super().stopTest(test)
        # use plugin to stop test if neccessary

    def addError(self, test, err):
        super().addError(test, err)
        # use plugin to add err to the test run/exec

    def addFailure(self, test, err):
        super().addFailure(test, err)
        # use plugin to add failuer to the test run/exec

    def addSuccess(self, test):
        super().addSuccess(test)
        # use plugin to report success for the test run/exec

    # def addSkip(self, test, reason):
    #     super(TextTestResult, self).addSkip(test, reason)
    #     if self.showAll:
    #         self.stream.writeln("skipped {0!r}".format(reason))
    #     elif self.dots:
    #         self.stream.write("s")
    #         self.stream.flush()
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        # find a way to report skip and why it happened

    # def addExpectedFailure(self, test, err):
    #     super(TextTestResult, self).addExpectedFailure(test, err)
    #     if self.showAll:
    #         self.stream.writeln("expected failure")
    #     elif self.dots:
    #         self.stream.write("x")
    #         self.stream.flush()

    def addExpectedFailure(self, test, err):
        super().addExpectedFailure(test, err)
        # report the expected failure

    # def addUnexpectedSuccess(self, test):
    #     super(TextTestResult, self).addUnexpectedSuccess(test)
    #     if self.showAll:
    #         self.stream.writeln("unexpected success")
    #     elif self.dots:
    #         self.stream.write("u")
    #         self.stream.flush()
    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        # report the unexpected success

    # investigate what the hell a 'subtest' is

    def printErrorList(self, flavour, errors):
        super().printErrorList(flavour, errors)


# class TextTestResult(result.TestResult):
        #     """A test result class that can print formatted text results to a stream.
        #     Used by TextTestRunner.
        #     """
        #     separator1 = '=' * 70
        #     separator2 = '-' * 70

        #     def __init__(self, stream, descriptions, verbosity):
        #         super(TextTestResult, self).__init__(stream, descriptions, verbosity)
        #         self.stream = stream
        #         self.showAll = verbosity > 1
        #         self.dots = verbosity == 1
        #         self.descriptions = descriptions

        #     def getDescription(self, test):
        #         doc_first_line = test.shortDescription()
        #         if self.descriptions and doc_first_line:
        #             return '\n'.join((str(test), doc_first_line))
        #         else:
        #             return str(test)

        #     def startTest(self, test):
        #         super(TextTestResult, self).startTest(test)
        #         if self.showAll:
        #             self.stream.write(self.getDescription(test))
        #             self.stream.write(" ... ")
        #             self.stream.flush()

        #     def addSuccess(self, test):
        #         super(TextTestResult, self).addSuccess(test)
        #         if self.showAll:
        #             self.stream.writeln("ok")
        #         elif self.dots:
        #             self.stream.write('.')
        #             self.stream.flush()

        #     def addError(self, test, err):
        #         super(TextTestResult, self).addError(test, err)
        #         if self.showAll:
        #             self.stream.writeln("ERROR")
        #         elif self.dots:
        #             self.stream.write('E')
        #             self.stream.flush()

        #     def addFailure(self, test, err):
        #         super(TextTestResult, self).addFailure(test, err)
        #         if self.showAll:
        #             self.stream.writeln("FAIL")
        #         elif self.dots:
        #             self.stream.write('F')
        #             self.stream.flush()

        #     def addSkip(self, test, reason):
        #         super(TextTestResult, self).addSkip(test, reason)
        #         if self.showAll:
        #             self.stream.writeln("skipped {0!r}".format(reason))
        #         elif self.dots:
        #             self.stream.write("s")
        #             self.stream.flush()

        #     def addExpectedFailure(self, test, err):
        #         super(TextTestResult, self).addExpectedFailure(test, err)
        #         if self.showAll:
        #             self.stream.writeln("expected failure")
        #         elif self.dots:
        #             self.stream.write("x")
        #             self.stream.flush()

        #     def addUnexpectedSuccess(self, test):
        #         super(TextTestResult, self).addUnexpectedSuccess(test)
        #         if self.showAll:
        #             self.stream.writeln("unexpected success")
        #         elif self.dots:
        #             self.stream.write("u")
        #             self.stream.flush()

        #     def printErrors(self):
        #         if self.dots or self.showAll:
        #             self.stream.writeln()
        #         self.printErrorList('ERROR', self.errors)
        #         self.printErrorList('FAIL', self.failures)

        #     def printErrorList(self, flavour, errors):
        #         for test, err in errors:
        #             self.stream.writeln(self.separator1)
        #             self.stream.writeln("%s: %s" % (flavour,self.getDescription(test)))
        #             self.stream.writeln(self.separator2)
        #             self.stream.writeln("%s" % err)

class TestResult(TextTestResult):

    def __init__(self, stream=None, descriptions=None, verbosity=2, **kwargs):
        super().__init__(stream=stream, descriptions=descriptions, verbosity=verbosity, **kwargs)
        self.tcms_api_backend = Backend(prefix='[DJANGO ] ')
        self.test_case_id = 0
        self.comment = ''
        self.status_id = 0
        self.trace_back = ''
        self.skip_reason = ''
        self.test_execution_id = 0

    def startTestRun(self):
        print("Test Run has started===============================\n\n\n")
        self.tcms_api_backend.configure()

    def startTest(self, test):
        super().startTest(test)
        test_case, _ = self.tcms_api_backend.test_case_get_or_create(
            self.getDescription(test))
        test_case_id = test_case['id']
        self.test_case_id = test_case_id
        print("caseid:", self.test_case_id)
        print("runid:", self.tcms_api_backend.run_id)

        self.tcms_api_backend.add_test_case_to_plan(test_case_id,
                                                    self.tcms_api_backend.plan_id)

        test_execution_id = self.tcms_api_backend.add_test_case_to_run(
            test_case_id,
            self.tcms_api_backend.run_id)
        self.test_execution_id = test_execution_id

        # self.comment = 'Result recorded via Kiwi TCMS tap-plugin'

        print("test started:", test_case_id,
              "description:", self.getDescription(test))
        # use self.getDescription(test) to get test description to start the reporting
        # and mebbe comment.

    def addSuccess(self, test):
        super().addSuccess(test)
        print("test passed:", self.getDescription(test))
        self.status_id = self.tcms_api_backend.get_status_id('PASSED')
        self.comment = self.getDescription(test)
        # use self.getDescription(test) to get test description to report success
        # and mebbe comment.

    def addError(self, test, err):
        super().addError(test, err)
        self.status_id = self.tcms_api_backend.get_status_id('FAILED')
        self.comment = self.getDescription(self.errors[-1][0])
        self.trace_back = self.errors[-1][0]

        # Actually this is wrong, we should be getting the last error appended to the errors.
        # after all this is "add Error".
        for error in self.errors:
            print("the test", self.getDescription(
                error[0]), "had an error. The formatted traceback: ", error[1])
        # The default implementation appends a tuple (test, formatted_err) to the instance’s errors attribute,
        # where formatted_err is a formatted traceback derived from err.
        # report this to API

    def addFailure(self, test, err):
        super().addFailure(test, err)
        # try find better status id
        self.status_id = self.tcms_api_backend.get_status_id('FAILED')
        self.comment = self.getDescription(self.failures[-1][0])
        self.trace_back = self.failures[-1][0]
        # Actually this is wrong, we should be getting the last failure appended to the failures.
        # after all this is "add Failure".
        for failure in self.failures:
            print("the test", self.getDescription(
                failure[0]), "had a failure. The formatted traceback: ", failure[1])
        # The default implementation appends a tuple (test, formatted_err) to the instance’s failures attribute,
        # where formatted_err is a formatted traceback derived from err.
        # report this to the API

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.status_id = self.tcms_api_backend.get_status_id('WAIVED')
        self.comment = self.getDescription(test)
        self.skip_reason = "skipped {0!r}".format(reason)
        print(self.getDescription(test), "skipped {0!r}".format(reason))
        # report to API and use this for reason - "skipped {0!r}".format(reason)

    def addExpectedFailure(self, test, err):
        super().addExpectedFailure(test, err)
        # get the latest tuple(test, formatted_err) from the expectedFailures attribute
        print("expected failure:",
              self.expectedFailures[-1][0], self.expectedFailures[-1][1])
        # The default implementation appends a tuple (test, formatted_err) to the instance’s expectedFailures attribute,
        # where formatted_err is a formatted traceback derived from err.
        # report to the API

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        # get the latest test instance from the unexpectedSuccesses attribute
        print("unexpected success:", self.unexpectedSuccesses[-1])
        # report the unexpected success to the API

    def stopTest(self, test):
        self.tcms_api_backend.update_test_execution(self.test_execution_id,
                                                    self.status_id,
                                                    self.comment)

    def stopTestRun(self):
        self.tcms_api_backend.finish_test_run()
        print("\n\n\nTest run has ended========================")


# use the new TextTestResult, so it makes the API calls through super() before it
# jumps into debugging


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


class TestRunner(DiscoverRunner):  # pylint: disable=too-few-public-methods
    # test_output_stream = io.StringIO()
    # test_runner = TextTestRunner(stream=test_output_stream)

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
        # self.backend = Backend(prefix='[DJANGO ] ')

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
            # 'resultclass': TestResult,
            'verbosity': self.verbosity,
        }

    def run_suite(self, suite, **kwargs):
        test_output = io.StringIO()
        kwargs = self.get_test_runner_kwargs()
        runner = self.test_runner(stream=test_output, **kwargs)
        # runner = self.test_runner(**kwargs)
        results = runner.run(suite)
        test_output.seek(0)

        # print("stream output", test_output.getvalue())
        # print("the kwargs===>", kwargs)
        print("the errors===>", results.errors)
        print("the failures===>", results.failures)
        print("the skipped===>", results.skipped)
        print("num of tests run===>", results.testsRun)
        print("was Successful===>", results.wasSuccessful())
        print("the result class being used is", results.__class__)
        # for line in test_output:
        #     # each line is return "%s (%s)" % (self._testMethodName, strclass(self.__class__))
        #     if line[-3:] == 'ok\n':
        #         print(line)
        #         # status_id = self.backend.get_status_id('PASSED')
        #     elif line[-5:] == 'FAIL\n':
        #         print(line)
        #         # status_id = self.backend.get_status_id('FAILED')
        #     elif line[-6:] == 'ERROR\n':
        #         print(line)

        # parse test output
        # if results.failures:
        #     for test, err in results.failures:
        #         print("the test", test)
        #         print("the errir", err)
        #     # print(line)
        return results

    # possible approaches to try:
    # - Pass Stream to TextTestRunner before the runner starts, use the stream then pass to std.err/std.out
    # - Override  _makeResult() with own TextResult that can handle stuff from its hooks

    # def parse(self, tap_file, progress_cb=None):
        # self.backend.configure()

        # test_execution_id = None
        # trace_back = []
        # for line in Parser().parse_file(tap_file):
        #     if isinstance(line, Result):
        #         # before parsing the 'next' result line add
        #         # traceback as comment to the previous TE
        #         if test_execution_id and trace_back:
        #             self.backend.add_comment(test_execution_id,
        #                                      "\n" + "\n".join(trace_back))
        #         trace_back = []
        #     elif isinstance(line, Diagnostic):
        #         trace_back.append(line.text[2:])
        #         continue
        #     else:
        #         continue

        #     test_case, _ = self.backend.test_case_get_or_create(
        #         line.description)
        #     test_case_id = test_case['id']

        #     self.backend.add_test_case_to_plan(test_case_id,
        #                                        self.backend.plan_id)
        #     test_execution_id = self.backend.add_test_case_to_run(
        #         test_case_id,
        #         self.backend.run_id)
        #     comment = 'Result recorded via Kiwi TCMS tap-plugin'

        #     if line.ok:
        #         status_id = self.backend.get_status_id('PASSED')
        #     else:
        #         status_id = self.backend.get_status_id('FAILED')

        #     if line.skip:
        #         status_id = self.backend.get_status_id('WAIVED')
        #         comment = line.directive.text

        #     if line.todo:
        #         status_id = self.backend.get_status_id('PAUSED')
        #         comment = line.directive.text

        #     self.backend.update_test_execution(test_execution_id,
        #                                        status_id,
        #                                        comment)

        #     if progress_cb:
        #         progress_cb()

        # self.backend.finish_test_run()
