# Copyright (c) 2020 Bryan Mutai , <work@bryanmutai.co>

# Licensed under the GPLv3: https://www.gnu.org/licenses/gpl.html


from django.test.runner import DiscoverRunner
from .result import TestResult, DebugSQLTestResult, PDBDebugResult

# TODO RPC METHOD: <Fault -32601: 'Method not found: "PlanType.create"'>


class TestRunner(DiscoverRunner):

    def get_resultclass(self):
        if self.debug_sql:
            return DebugSQLTestResult

        if self.pdb:
            return PDBDebugResult

        return TestResult
