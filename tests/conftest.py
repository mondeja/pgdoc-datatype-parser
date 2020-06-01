# -*- coding: utf-8 -*-

import os
import re
import sys
from pkg_resources import parse_version
from pkg_resources.extern.packaging.version import Version

import pytest

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.dirname(TEST_DIR))

sys.path.append(ROOT)


class Asserter:
    def non_empty_string(self, value):
        assert isinstance(value, str)
        assert len(value) > 0

    def commit_hex(self, value):
        assert isinstance(value, str)
        assert len(value) == 40
        assert re.match(r'[a-f0-9]+', value)

    def version(self, value):
        self.non_empty_string(value)
        assert isinstance(parse_version(value), Version)


_asserter = Asserter()


@pytest.fixture
def asserter():
    yield _asserter
