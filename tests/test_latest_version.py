# -*- coding: utf-8 -*-

from pkg_resources import parse_version

from pgdoc_datatype_parser import (
    latest_version,
    versions,
)


def test_latest_version(asserter):
    latest = parse_version(latest_version())

    for version in versions():
        asserter.version(version)
        parsed_version = parse_version(version)
        assert parsed_version < latest or parsed_version == latest
