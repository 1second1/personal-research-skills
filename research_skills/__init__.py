"""Runtime support for composing personal research Skills."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("personal-research-skills")
except PackageNotFoundError:  # Source checkout before installation.
    __version__ = "0+unknown"
