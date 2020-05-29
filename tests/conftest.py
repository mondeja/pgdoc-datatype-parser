# -*- coding: utf-8 -*-

import os
import sys

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.dirname(TEST_DIR))

TEST_MARKUP_FILEPATH = os.path.join(TEST_DIR, "markup.html")

sys.path.append(ROOT)

from pgdoc_datatype_parser import (  # noqa: E402
    PG_RELEASES_JSON_FILEPATH,
    build_pg_releases_json_file,
)

if os.path.exists(PG_RELEASES_JSON_FILEPATH):
    os.remove(PG_RELEASES_JSON_FILEPATH)
build_pg_releases_json_file()
