# -*- coding: utf-8 -*-

from pkg_resources import parse_version

from pgdoc_datatype_parser import (
    latest_version,
    versions,
)


def test_latest_version(asserter):
    latest = parse_version(latest_version())

    for version in versions()[1:]:
        asserter.version(version)
        assert parse_version(version) < latest
