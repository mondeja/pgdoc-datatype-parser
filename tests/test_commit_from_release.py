import pytest

from pgdoc_datatype_parser import commit_from_release


@pytest.mark.parametrize(
    ("version", "error", "filepath"),
    [
        # Non existent version
        ("X.X.X", ValueError, None),
        # Latest version
        ("latest", None, None),
        # Valid versions
        ("13.1b", None, None),
        ("11.4", None, None),
        ("9.4.21", None, None),
        # Point not in version
        ("8", None, None),
        ("8.0", None, None),
        ("7", ValueError, None),
        # Non existent releases file
        ("9.4.21", ValueError, "/tmp/_pgdoc_datatype_parser_file"),
    ],
)
def test_commit_from_release(asserter, version, error, filepath):
    if error is not None:
        with pytest.raises(error):
            commit_from_release(version=version, pg_releases_filepath=filepath)
    else:
        commit_hex = commit_from_release(version=version, pg_releases_filepath=filepath)
        asserter.commit_hex(commit_hex)
