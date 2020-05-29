# -*- coding: utf-8 -*-

__version__ = "0.0.1"
__version_info__ = tuple([int(i) for i in __version__.split(".")])
__title__ = "pgdoc-datatype-parser"
__description__ = "PostgreSQL documentation data types parser."

PG_GH_RELEASES_URL = "https://api.github.com/repos/postgres/postgres/tags"
PG_RELEASES_JSON_FILENAME = "pg-releases.json"
PG_DT_DOC_FILE_URLSCHEMA = "https://raw.githubusercontent.com/postgres/" \
                         + "postgres/{commit_id}/doc/src/sgml/datatype.sgml"

import collections
import json
import os
import re
try:
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import Request, urlopen

def pg_release_name_to_version_number(release_name):
    mayor = re.search(r"REL_{0,1}(\d+)", release_name).group(1)

    minor_match = re.search(r"\d+_(\d+)_", release_name)
    if minor_match is not None:
        minor = minor_match.group(1)
    else:
        minor = None

    micro_match = re.search(r"(\d+)$", release_name)
    if micro_match is not None:
        micro = micro_match.group(1)
    else:
        micro = ""

    rc_match = re.search(r"_([A-Z]+)", release_name)
    if rc_match is not None:
        rc = rc_match.group(1)
        if len(rc) > 2:
            rc = rc[0].lower()
        else:
            rc = rc.lower()
    else:
        rc = ""

    if minor is None:
        return "%s.%s%s" % (mayor, micro, rc)
    else:
        return "%s.%s.%s%s" % (mayor, minor, micro, rc)

def build_pg_releases_json_file(filepath=None):
    if filepath is None:
        filepath = os.path.join(
            os.path.dirname(__file__), PG_RELEASES_JSON_FILENAME)
    if os.path.exists(filepath):
        raise EnvironmentError(
            "Previous PostgreSQL releases file '%s' exists." % filepath)

    github_token = os.environ.get("GITHUB_TOKEN")

    content = {}
    # Github API pagination
    _last_page, _current_page = (float("inf"), 1)
    while _current_page <= _last_page:
        url = "%s?per_page=100&page=%d" % (PG_GH_RELEASES_URL, _current_page)
        req = Request(url)
        if github_token:
            req.add_header("Authorization", "token %s" % github_token)

        res = urlopen(req)

        # Discover last page
        if _last_page == float("inf"):
            link_header = res.getheader("link")
            _last_page = int(re.search(
                r"[^_]page=(\d+)", link_header.split(",")[-1]).group(1))

        # Parse releases
        for release in json.loads(res.read()):
            if not release["name"].startswith("REL"):
                continue
            version = pg_release_name_to_version_number(release["name"])
            content[version] = release["commit"]["sha"][:7]
        _current_page += 1

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(json.dumps(content))
    return content

def commit_from_release_version(version="latest", pg_releases_filepath=None):
    if pg_releases_filepath is None:
        pg_releases_filepath = os.path.join(
            os.path.dirname(__file__), PG_RELEASES_JSON_FILENAME)
    if not os.path.exists(pg_releases_filepath):
        raise ValueError("PostgreSQL releases file '%s' does not exists." % (
            pg_releases_filepath))

    if version == "latest":
        decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
        with open(pg_releases_filepath, encoding="utf-8") as f:
            releases = decoder.decode(f.read())
        commit = releases[list(releases.keys())[0]]
    else:
        if "." not in version:
            version += ".0"
        with open(pg_releases_filepath, encoding="utf-8") as f:
            releases = json.loads(f.read())
        if version not in releases:
            raise ValueError(
                "Version '%s' is not a valid PostgreSQL release." % version)
        commit = releases[version]
    return commit

def parse_datatypes(sgml_content):
    _inside_datatypes_table, _inside_tbody, entry_n, _current_dt = (
        False, False, 0, None)
    response = {}

    lines = sgml_content.splitlines()
    for i, line in enumerate(lines):
        print(line)
        if not _inside_datatypes_table and "id=\"datatype-table\"" in line:
            _inside_datatypes_table = True
            continue
        elif not _inside_tbody and "<tbody>" in line:
            _inside_tbody = True
            continue
        elif _inside_tbody and "<entry>" in line:
            entry_n += 1
            if "</entry>" not in line and "</type>" not in line:
                line += lines[i+1]
            value_match = re.search(r"<type>(.*)</type>", line)
            if value_match is None:
                value_match = re.search(r"<entry>(.*)</entry>", line)

            # Remove XML tags, múltiple continue spaces...
            value, _inside_tag, _last_c_space = ("", False, False)
            for c in value_match.group(1):
                if c == "<":
                    _inside_tag = True
                    continue
                elif c == ">" and _inside_tag:
                    _inside_tag = False
                    continue
                else:
                    if not _inside_tag:
                        if c == " ":
                            if not _last_c_space:
                                value += c
                                _last_c_space = True
                            continue
                        value += c
                        _last_c_space = False

            # Order by data
            if entry_n == 1:
                response[value] = {}
                _current_dt = value
            elif entry_n == 2:
                aliases = value or None
                if aliases and "," in aliases and "[" not in aliases:
                    aliases = aliases.split(",")
                response[_current_dt]["aliases"] = aliases
            elif entry_n == 3:
                response[_current_dt]["description"] = value
                entry_n = 0
                _current_dt = None
        elif _inside_tbody and "</tbody>" in line:
            break
    return response

def pgdoc_datatypes(version="latest", pg_releases_filepath=None):
    commit = commit_from_release_version(
        version=version, pg_releases_filepath=pg_releases_filepath)

    # Get documentation data types file
    url = PG_DT_DOC_FILE_URLSCHEMA.replace("{commit_id}", commit)
    return parse_datatypes(urlopen(url).read().decode("utf-8"))

if __name__ == "__main__":
    from pprint import pprint
    pprint(pgdoc_datatypes())

# Search on Github all PostgreSQL releases
# For each release, get the commit id and version
# Save all PostgreSQL releases on a JSON document

# Test that PostgreSQL releases are available on Github
# Test new releases that doesn't have been added to JSON
#   -> Create a commit from TravisCI to add the new release inside JSON file

# Parse the file https://raw.githubusercontent.com/postgres/postgres/{commit_id}/doc/src/sgml/datatype.sgml
#   where all data types are documented.
