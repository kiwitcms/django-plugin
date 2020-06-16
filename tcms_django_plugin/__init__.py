# Copyright (c) 2020 Bryan Mutai , <work@bryanmutai.co>

# Licensed under the GPLv3: https://www.gnu.org/licenses/gpl.html


from django.test.runner import DiscoverRunner
from .result import TestResult


class TestRunner(DiscoverRunner):

    def get_resultclass(self):
        return TestResult
