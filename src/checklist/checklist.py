import os
from typing import Union

import fire
from ruamel.yaml import YAML


class Checklist:
    def __init__(self, checklist_path: str):
        if not os.path.exists(checklist_path):
            raise FileNotFoundError("Checklist file not found.")
        try:
            with open(checklist_path, "r") as f:
                self.content = YAML(typ="safe").load(f)
            self.test_areas = set([x["Topic"] for x in self.content["Test Areas"]])
        except Exception as e:
            raise SyntaxError("Failed to parse the checklist. Make sure that it is a YAML 1.2 document.")

    def get_tests_by_areas(self, areas: Union[list, str, set], requirements_only: bool = False):
        tests = []

        if isinstance(areas, str):
            areas = [areas]
        areas_set = set(areas)
        if not areas_set.issubset(self.test_areas):
            raise KeyError("The provided areas has one or more items that is not present in the checklist.")

        areas = [ x for x in self.content["Test Areas"] if x["Topic"] in areas ]
        for area in areas:
            if requirements_only:
                tests += [x.get("Requirement") for x in area["Tests"]]
            else:
                tests += area["Tests"]
        return tests

    def get_all_tests(self, requirements_only: bool = False):
        return self.get_tests_by_areas(self.test_areas, requirements_only)

    def get_test_areas(self):
        return self.test_areas


if __name__ == "__main__":
    def example(checklist_path: str):
        """Example calls. To be removed later."""
        checklist = Checklist(checklist_path)
        # tests = checklist.get_tests_by_areas("General", requirements_only=False)
        tests = checklist.get_all_tests()
        print(tests)

    fire.Fire(example)
