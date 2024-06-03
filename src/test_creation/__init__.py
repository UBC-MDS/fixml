# read version from installed package
from importlib.metadata import version

from .test_creation import main
__version__ = version("test_creation")
