import pytest

from pgdoc_datatype_parser import pg_release_name_to_version, versions


class TestReleaseNameToVersionConverter:
    @classmethod
    def setup_class(cls):
        cls.versions = versions()

    @pytest.mark.parametrize(
        "release_name,expected_version",
        [
            ("REL_13_BETA1", "13.1b"),
            ("REL_12_3", "12.3"),
            ("REL9_5_22", "9.5.22"),
            ("REL_12_RC1", "12.1rc"),
            ("REL9_6_RC1", "9.6.1rc"),
            ("REL9_6_BETA4", "9.6.4b"),
            ("REL9_0_ALPHA5", "9.0.5a"),
        ],
    )
    def test_pg_release_name_to_version(self, release_name, expected_version):
        version = pg_release_name_to_version(release_name)
        assert version == expected_version
        assert version in self.versions
