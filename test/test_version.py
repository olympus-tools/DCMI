import re
from importlib.metadata import version


def test_package_version_is_present_and_semver_like() -> None:
    package_version = version("dcmi")
    assert re.fullmatch(r"\d+\.\d+\.\d+(?:[.+-][0-9A-Za-z.+-]+)?", package_version)
