# -*- coding: utf-8 -*-

import collections
import hashlib
import json
import os
import sys

SCRIPTS_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.dirname(SCRIPTS_DIR))

sys.path.append(ROOT)

from pgdoc_datatype_parser import (  # noqa: E402
    PG_RELEASES_JSON_FILEPATH,
    build_pg_releases_json_file,
)


def pg_releases_file_md5(pg_releases_filepath=None):
    pg_releases_filepath = pg_releases_filepath if pg_releases_filepath \
        else PG_RELEASES_JSON_FILEPATH
    decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
    with open(pg_releases_filepath, encoding="utf-8") as f:
        releases = decoder.decode(f.read())
    return hashlib.md5(str(releases).encode("utf-8")).hexdigest()


def main():
    previous_pg_releases_file_md5 = pg_releases_file_md5()

    new_releases_filepath = os.path.abspath(
        os.path.join(os.path.dirname(PG_RELEASES_JSON_FILEPATH),
                     "_new-pg-releases.json"))
    err = None

    try:
        build_pg_releases_json_file(filepath=new_releases_filepath)
        new_pg_releases_file_md5 = pg_releases_file_md5(
            pg_releases_filepath=new_releases_filepath)
        if new_pg_releases_file_md5 != previous_pg_releases_file_md5:
            os.remove(PG_RELEASES_JSON_FILEPATH)
            os.rename(new_releases_filepath, PG_RELEASES_JSON_FILEPATH)
            sys.stdout.write(
                "'pgdoc_datatype_parser/pg-releases.json' file updated.\n")
            return 1
    except Exception as _err:
        err = _err
    finally:
        if os.path.exists(new_releases_filepath):
            os.remove(new_releases_filepath)
    if err:
        raise err
    return 0


if __name__ == "__main__":
    sys.exit(main())
