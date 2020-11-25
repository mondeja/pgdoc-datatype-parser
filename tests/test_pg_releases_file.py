# -*- coding: utf-8 -*-

import json
import os
import tempfile

import pytest

from pgdoc_datatype_parser import (
    PG_RELEASES_JSON_FILEPATH,
    build_pg_releases_json_file
)
from tests.conftest import _asserter


def assert_pg_releases_file_content(content):
    for version, commit_hex in content.items():
        _asserter.version(version)
        _asserter.commit_hex(commit_hex)


def test_current_pg_releases_file():
    with open(PG_RELEASES_JSON_FILEPATH, "r", encoding="utf-8") as f:
        releases = json.loads(f.read())

    assert len(list(releases.keys())) > 400
    assert_pg_releases_file_content(releases)


def test_not_override_current_pg_releases_file():
    with pytest.raises(EnvironmentError):
        build_pg_releases_json_file(filepath=PG_RELEASES_JSON_FILEPATH)


def test_build_pg_releases_file():
    filepath = os.path.join(tempfile.gettempdir(), "pg-releases-test.json")
    if os.path.exists(filepath):
        os.remove(filepath)

    build_pg_releases_json_file(filepath=filepath)
    assert os.path.isfile(filepath)

    with open(filepath, "r", encoding="utf-8") as f:
        releases = json.loads(f.read())
    assert_pg_releases_file_content(releases)
