# -*- coding: utf-8 -*-

import collections
import hashlib
import json
import os
import sys


SCRIPTS_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.dirname(SCRIPTS_DIR))
PULL_REQUEST_MESSAGE = '--pull-request' in sys.argv

sys.path.append(ROOT)

from pgdoc_datatype_parser import (  # noqa: E402
    PG_RELEASES_JSON_FILEPATH,
    build_pg_releases_json_file
)


def pg_releases_file_md5(pg_releases_filepath):
    decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
    with open(pg_releases_filepath, encoding="utf-8") as f:
        releases = decoder.decode(f.read())
    return hashlib.md5(str(releases).encode("utf-8")).hexdigest()


def pg_releases_from_file(pg_releases_filepath):
    decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
    with open(pg_releases_filepath, encoding="utf-8") as f:
        releases = decoder.decode(f.read())
    return list(releases.keys())


def build_pr_message_from_releases(previous_releases, new_releases):
    new_releases_md_list = ''
    removed_releases_md_list = ''

    for new_release in new_releases:
        if new_release not in previous_releases:
            new_releases_md_list += '- v%s\n' % new_release
    for prev_release in previous_releases:
        if prev_release not in new_releases:
            removed_releases_md_list += '- v%s\n' % prev_release

    response = ''
    if new_releases_md_list:
        response += '### New releases\n\n%s\n' % new_releases_md_list
    if removed_releases_md_list:
        response += '### Removed releases\n\n%s\n' % removed_releases_md_list

    return response


def main():
    previous_pg_releases_file_md5 = pg_releases_file_md5(
        PG_RELEASES_JSON_FILEPATH)

    new_releases_filepath = os.path.abspath(
        os.path.join(os.path.dirname(PG_RELEASES_JSON_FILEPATH),
                     "_new-pg-releases.json"))

    err = None

    try:
        build_pg_releases_json_file(filepath=new_releases_filepath)
        new_pg_releases_file_md5 = pg_releases_file_md5(new_releases_filepath)
        if new_pg_releases_file_md5 != previous_pg_releases_file_md5:
            if PULL_REQUEST_MESSAGE:
                previous_releases = pg_releases_from_file(
                    PG_RELEASES_JSON_FILEPATH)
                new_releases = pg_releases_from_file(new_releases_filepath)
                sys.stdout.write(
                    build_pr_message_from_releases(
                        previous_releases, new_releases)
                )
            os.remove(PG_RELEASES_JSON_FILEPATH)
            os.rename(new_releases_filepath, PG_RELEASES_JSON_FILEPATH)
            if PULL_REQUEST_MESSAGE:
                return 0
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
