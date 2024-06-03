# read version from installed package
from importlib.metadata import version

from .cli.main import main as cli_main

__version__ = version("test_creation")
