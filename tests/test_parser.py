# -*- coding: utf-8 -*-

import os
import json
import time

import pytest

from pgdoc_datatype_parser import (
    PG_RELEASES_JSON_FILEPATH,
    pgdoc_datatypes,
)

# Dirty synchronization with pytest-xdist
while not os.path.exists(PG_RELEASES_JSON_FILEPATH):
    time.sleep(1)

with open(PG_RELEASES_JSON_FILEPATH, "r", encoding="utf-8") as f:
    VERSIONS = list(json.loads(f.read()).keys())


def assert_non_empty_string(value):
    assert isinstance(value, str)
    assert len(value) > 0


def assert_datatype_name(value):
    assert_non_empty_string(value)


def assert_aliases(value):
    if value is not None:
        if isinstance(value, list):
            assert len(value) > 0
            for v in value:
                assert_non_empty_string(v)
        else:
            assert_non_empty_string(value)


def asser_description(value):
    assert_non_empty_string(value)


@pytest.mark.parametrize("version", VERSIONS)
def test_release(version):
    datatypes = pgdoc_datatypes(version=version)
    for dtname, dtspec in datatypes.items():
        assert_datatype_name(dtname)
        assert_aliases(dtspec["aliases"])
        asser_description(dtspec["description"])
