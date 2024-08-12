try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    from importlib_metadata import (  # type: ignore[import-not-found, no-redef]
        PackageNotFoundError,
        version,
    )

UNINSTALLED = "uninstalled"

try:
    VERSION = version("org.vuepy.core")
except PackageNotFoundError:
    VERSION = UNINSTALLED


def get_semver_version(_version: str) -> str:
    """
    https://semver.org/

    :param version:
    :return:
    """
    if _version == UNINSTALLED:
        return _version

    split = _version.split(".", maxsplit=2)
    patch = split[2] if len(split) == 3 else ''
    is_pre_release = "a" in patch or "b" in patch
    if is_pre_release:
        return ".".join(split)

    return "~" + ".".join([split[0], split[1], "*"])


SEMVER_VERSION = get_semver_version(VERSION)
