import os
import csv
import copy
from importlib.resources import files
from pathlib import Path
from enum import Enum
from typing import Union
from abc import ABC, abstractmethod

from ruamel.yaml import YAML

from ..template import TemplateLoader
from ..mixins import ExportableMixin
from ..utils import get_extension


def filter_dict(d: dict, keys: list) -> dict:
    return {k: v for k, v in d.items() if k in keys}


class ChecklistFormat(Enum):
    YAML = 'yaml'
    CSV = 'csv'


class ChecklistIO(ABC):
    @abstractmethod
    def read(self, path: str) -> dict:
        pass

    @abstractmethod
    def write(self, path: str, data: dict) -> None:
        pass


class YamlChecklistIO(ChecklistIO):
    @classmethod
    def read(cls, path: str) -> dict:
        try:
            with open(path, "r") as f:
                content = YAML(typ="safe").load(f)
            return content
        except Exception as e:
            raise SyntaxError("Failed to parse the checklist. Make sure that it is a YAML 1.2 document.")

    @classmethod
    def write(cls, path: str, data: dict) -> None:
        yaml = YAML()
        yaml.indent(sequence=4, offset=2)
        yaml.default_flow_style = False
        with open(path, "w") as f:
            yaml.dump(data, f)


class CsvChecklistIO(ChecklistIO):
    overview_field_names_unnested = ["Title", "Description"]
    overview_field_name_nested = "Test Areas"
    topics_field_names_unnested = ["ID", "Topic", "Description"]
    topics_field_name_nested = "Tests"
    tests_field_names_unnested = ["ID", "Topic", "Title", "Requirement", "Explanation", "References"]
    tests_field_names_ignore = ["Topic"]
    overview_filename = "overview.csv"
    topics_filename = "topics.csv"
    tests_filename = "tests.csv"

    @staticmethod
    def _read_file(path: str) -> list:
        with open(path, "r") as f:
            reader = csv.DictReader(f)
            results = list(reader)
        return results

    @staticmethod
    def _write_file(path: str, items: list, field_names: list) -> None:
        with open(path, "w") as f:
            w = csv.DictWriter(f, fieldnames=field_names, extrasaction='ignore')
            w.writeheader()
            for item in items:
                w.writerow(item)

    @classmethod
    def read(cls, path: str) -> dict:
        try:
            if not os.path.isdir(path):
                raise NotADirectoryError("Checklist path is not a directory.")
            ov_filepath = os.path.join(path, cls.overview_filename)
            to_filepath = os.path.join(path, cls.topics_filename)
            te_filepath = os.path.join(path, cls.tests_filename)
            if not os.path.isfile(ov_filepath) or not os.path.isfile(to_filepath) or not os.path.isfile(te_filepath):
                raise FileNotFoundError("All three CSV files must be present in the directory.")

            overview = cls._read_file(ov_filepath)
            topics = cls._read_file(to_filepath)
            tests = cls._read_file(te_filepath)

            for topic in topics:
                topic_id = topic["ID"]
                # matches all tests with ID that starts with the same as current topic ID
                # this assumes that the test item ID would contain a dot i.e. `.` and
                # follows the format `{topic-id}.{test-number}`, where the `{test-number}
                # is an incremental number to indicate the ordering of the test within
                # a topic.
                topic_tests = [test for test in tests if test["ID"].split(".")[0] == topic_id]
                topic[cls.topics_field_name_nested] = topic_tests

            for test in tests:
                # convert the references back into a list from its joined string representation
                test['References'] = test['References'].split(',')
                test['References'] = [x.strip(' ') for x in test['References']]

                # remove keys to be ignored (i.e. not included) in the constructed dictionary
                for key in cls.tests_field_names_ignore:
                    test.pop(key, None)

            content = overview[0]
            content[cls.overview_field_name_nested] = topics
            return content

        except Exception as e:
            raise SyntaxError("Failed to parse the checklist. Make sure that it is a directory containing CSV files.")

    @classmethod
    def write(cls, path: str, data: dict) -> None:
        os.makedirs(path, exist_ok=True)
        overview = [filter_dict(data, cls.overview_field_names_unnested)]
        topics = [filter_dict(area, cls.topics_field_names_unnested) for area in data["Test Areas"]]

        # change the representation of tests:
        # 1. Add `Topic` from the parent Topic
        # 2. Change references representation from list to string
        tests = []
        for area in data["Test Areas"]:
            new_tests = copy.deepcopy(area["Tests"])
            for test in new_tests:
                test["Topic"] = area["Topic"]
                test["References"] = ', '.join(test["References"])
            tests += new_tests

        cls._write_file(os.path.join(path, cls.overview_filename), overview, cls.overview_field_names_unnested)
        cls._write_file(os.path.join(path, cls.topics_filename), topics, cls.topics_field_names_unnested)
        cls._write_file(os.path.join(path, cls.tests_filename), tests, cls.tests_field_names_unnested)


class Checklist(ExportableMixin):
    def __init__(self, checklist_path: str = None):
        super().__init__()
        self.ext_io_map = {
            'csv': CsvChecklistIO,
            'yaml': YamlChecklistIO,
            'yml': YamlChecklistIO
        }
        if not checklist_path:
            checklist_path = files("fixml.data.checklist") / "checklist.csv"
        ext = get_extension(checklist_path)
        self.__check_ext_is_valid(ext)
        self.path = checklist_path
        if not os.path.exists(self.path):
            raise FileNotFoundError("Checklist file not found.")
        self.content = self.ext_io_map[ext].read(self.path)
        self.test_areas = set([x["Topic"] for x in self.content["Test Areas"]])
        self.export_template = TemplateLoader.load("checklist")

    def __check_ext_is_valid(self, ext: str) -> bool:
        if ext not in self.ext_io_map:
            raise ValueError(
                f"Invalid input format(s) provided. The acceptable formats "
                f"are {list(self.ext_io_map.keys())}."
            )
        return True

    def get_tests_by_areas(self, areas: Union[list, str, set], keys: Union[list, None] = None) -> list:
        tests = []

        if isinstance(areas, str):
            areas = [areas]
        areas_set = set(areas)
        if not areas_set.issubset(self.test_areas):
            raise KeyError("The provided areas has one or more items that is not present in the checklist.")

        areas = [x for x in self.content["Test Areas"] if x["Topic"] in areas]
        for area in areas:
            for test in area["Tests"]:
                if test['Is Evaluator Applicable'] == '1':
                    if keys:
                        tests.append(filter_dict(test, keys))
                    else:
                        tests.append(test)
        return tests

    def get_all_tests(self, keys=None) -> list:
        return self.get_tests_by_areas(self.test_areas, keys=keys)

    def get_test_areas(self) -> set:
        return self.test_areas

    def write_to(self, output_path: Union[str, Path], exist_ok=False) -> None:
        """Write the checklist to a file.

        This is a simple wrapper to automatically write checklist into
        appropriate format determined by the extension given in the specified
        output path.
        """
        ext = get_extension(output_path)
        self.__check_ext_is_valid(ext)
        if ext == 'yaml':
            self.to_yaml(output_path, no_preserve_format=True, exist_ok=exist_ok)
        elif ext == 'csv':
            self.to_csv(output_path, exist_ok=exist_ok)

    def to_yaml(self, output_path: Union[str, Path], no_preserve_format: bool = False, exist_ok: bool = False):
        if not no_preserve_format:
            raise NotImplementedError(
                "Roundtripping is not yet implemented. If you want to dump the YAML file disregarding the original "
                "formatting, use `no_preserve_format=True`."
            )
        self._filedump_check(output_path, exist_ok)
        YamlChecklistIO.write(output_path, self.content)

    def to_csv(self, output_path: Union[str, Path], exist_ok: bool = False):
        """Dump the checklist to a directory containing three separate CSV files."""
        self._filedump_check(output_path, exist_ok, expects_directory_if_exists=True)
        CsvChecklistIO.write(output_path, self.content)

    def as_markdown(self, add_quarto_header: bool = False):
        vars = {
            "checklist": self.content,
            "quarto_header": add_quarto_header,
            "template_path": self.export_template.filename
        }
        return self.export_template.render(**vars)

    def as_quarto_markdown(self):
        return self.as_markdown(add_quarto_header=True)
