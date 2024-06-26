#!/usr/bin/env python

import fire
from dotenv import load_dotenv

from .checklist import ChecklistActions
from .repository import RepositoryActions
from .export import ExportActions

load_dotenv()


class TestCreation:
    """Context-aware test suite evaluation and generation tool."""

    def __init__(self):
        self.repository = RepositoryActions()
        self.checklist = ChecklistActions()
        self.export = ExportActions()

        self.evaluate = self.repository.evaluate
        self.generate = self.repository.generate


def main():
    """This is the CLI entry point."""
    fire.Fire(TestCreation)
