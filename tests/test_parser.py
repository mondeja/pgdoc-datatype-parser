# -*- coding: utf-8 -*-

import time

import pytest

from pgdoc_datatype_parser import pgdoc_datatypes, versions
from tests.conftest import _asserter


def assert_datatype_name(value):
    _asserter.non_empty_string(value)


def assert_aliases(value):
    if value is not None:
        if isinstance(value, list):
            assert len(value) > 0
            for v in value:
                _asserter.non_empty_string(v)
        else:
            _asserter.non_empty_string(value)


def asser_description(value):
    _asserter.non_empty_string(value)


@pytest.mark.parametrize("version", versions())
def test_release(version):
    datatypes, max_attemps, attempts, err = (None, 10, 0, None)
    while max_attemps > attempts:
        try:
            datatypes = pgdoc_datatypes(version=version)
        except Exception as exception:
            attempts += 1
            err = exception
            time.sleep(1)
        else:
            err = None
            break
    if err:
        raise err
    for dtname, dtspec in datatypes.items():
        assert_datatype_name(dtname)
        assert_aliases(dtspec["aliases"])
        asser_description(dtspec["description"])
