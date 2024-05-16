import pprint
import logging

import fire

from repo import Repository


logger = logging.getLogger('code_analyzer')

ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(ch)


def print_packages_and_test_files(repo_path: str):
    """Example call to show how to use the repo object.

    Parameters
    ----------
    repo_path : str
        Path to the downloaded repository to be analyzed.
    """
    repo = Repository(repo_path)

    packages = repo.list_packages()
    print("\nPackages:")
    print(packages)

    testfiles = repo.list_test_files()
    print("\nTest Files:")
    pprint.pprint(testfiles)


if __name__ == '__main__':
    # Example call:
    # python example.py ../data/repos/boxer.ai
    fire.Fire(print_packages_and_test_files)
