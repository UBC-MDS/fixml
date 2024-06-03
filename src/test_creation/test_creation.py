#!/usr/bin/env python

import fire
from dotenv import load_dotenv

from test_creation.cli.checklist import ChecklistActions
from test_creation.cli.repository import RepositoryActions
from test_creation.cli.consistency import ConsistencyCheckingActions

load_dotenv()


class TestCreation(object):
    """Context-aware test suite evaluation and generation tool."""

    def __init__(self):
        self.repository = RepositoryActions()
        self.consistency = ConsistencyCheckingActions()
        self.checklist = ChecklistActions()

        self.evaluate = self.repository.evaluate
        self.generate = self.repository.generate

    def evaluate(self, checklist_path, repo_path, report_output_path):
        """Evaluate a given git repository. Alias to `repository evaluate`."""
        self.repository.evaluate(checklist_path, repo_path, report_output_path)


def main():
    """This is the CLI entry point."""
    fire.Fire(TestCreation)
