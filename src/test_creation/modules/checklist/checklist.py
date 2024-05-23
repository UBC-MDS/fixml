import os
import csv
import copy
from enum import Enum
from typing import Union
from abc import ABC, abstractmethod

import fire
import pypandoc
from ruamel.yaml import YAML


def filter_dict(d: dict, keys: list) -> dict:
    return {k: v for k, v in d.items() if k in keys}


class ChecklistFormat(Enum):
    YAML = 1
    CSV = 2


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


class Checklist:
    def __init__(self, checklist_path: str, checklist_format: ChecklistFormat):
        if not os.path.exists(checklist_path):
            raise FileNotFoundError("Checklist file not found.")
        if checklist_format == ChecklistFormat.YAML:
            self.content = YamlChecklistIO.read(checklist_path)
        elif checklist_format == ChecklistFormat.CSV:
            self.content = CsvChecklistIO.read(checklist_path)
        else:
            raise NotImplementedError(f"Format {checklist_format} is not supported.")

        self.test_areas = set([x["Topic"] for x in self.content["Test Areas"]])

    def get_tests_by_areas(self, areas: Union[list, str, set], keys: Union[list, None] = None) -> list:
        tests = []

        if isinstance(areas, str):
            areas = [areas]
        areas_set = set(areas)
        if not areas_set.issubset(self.test_areas):
            raise KeyError("The provided areas has one or more items that is not present in the checklist.")

        areas = [x for x in self.content["Test Areas"] if x["Topic"] in areas]
        for area in areas:
            if keys:
                tests += [filter_dict(x, keys) for x in area["Tests"]]
            else:
                tests += area["Tests"]
        return tests

    def get_all_tests(self, keys=None) -> list:
        return self.get_tests_by_areas(self.test_areas, keys=keys)

    def get_test_areas(self) -> set:
        return self.test_areas

    def to_yaml(self, output_path: str, no_preserve_format: bool = False, exist_ok: bool = False):
        if not no_preserve_format:
            raise NotImplementedError(
                "Roundtripping is not yet implemented. If you want to dump the YAML file disregarding the original "
                "formatting, use `no_preserve_format=True`."
            )
        self.__filedump_check(output_path, exist_ok)
        YamlChecklistIO.write(output_path, self.content)

    def to_csv(self, output_path: str, exist_ok: bool = False):
        """Dump the checklist to a directory containing three separate CSV files."""
        self.__filedump_check(output_path, exist_ok)
        CsvChecklistIO.write(output_path, self.content)

    def as_markdown(self):
        return self._get_md_representation(self.content, curr_level=1)

    def _get_md_representation(self, content: dict, curr_level: int):
        repeated_col = [k for k, v in content.items() if isinstance(v, list)]

        # print out header for each item
        md_repr = '#' * curr_level
        if 'ID' in content.keys():
            md_repr += f" {content['ID']}"
        if 'Title' in content.keys():
            md_repr += f" {content['Title']}\n\n"
        elif 'Topic' in content.keys():
            md_repr += f" {content['Topic']}\n\n"

        # print out non-title, non-repeated items
        for k, v in content.items():
            if k not in repeated_col and k not in ['Title', 'Topic', 'ID']:
                md_repr += f'**{k}**: {v.replace("'", "\\'")}\n\n'

        # handle repeated columns and references
        for k in repeated_col:
            if k != 'References':
                for item in content[k]:
                    md_repr += self._get_md_representation(item, curr_level=curr_level + 1)
            else:
                md_repr += '**References:**\n\n' + '\n'.join(f'  - {item}' for item in content['References']) + '\n\n'

        return md_repr

    @staticmethod
    def __filedump_check(output_path: str, exist_ok: bool):
        if not exist_ok and os.path.exists(output_path):
            raise FileExistsError("Output file already exists. Use `exist_ok=True` to overwrite.")
        return True

    def export_html(self, output_path: str, exist_ok: bool = False):
        self.__filedump_check(output_path, exist_ok)
        pypandoc.convert_text(self.as_markdown(), 'html', format='md', outputfile=output_path)

    def export_pdf(self, output_path: str, exist_ok: bool = False):
        self.__filedump_check(output_path, exist_ok)
        pypandoc.convert_text(self.as_markdown(), 'pdf', format='md', outputfile=output_path,
                              extra_args=['--pdf-engine=tectonic'])

    def export_quarto(self, output_path: str, exist_ok: bool = False):
        self.__filedump_check(output_path, exist_ok)
        header = f'---\ntitle: "{self.content['Title']}"\nformat:\n  html:\n  code-fold: true\n---\n\n'
        qmd_repr = header + self.as_markdown()
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(qmd_repr)


if __name__ == "__main__":
    def example(checklist_path: str):
        """Example calls. To be removed later.

        Example:
        python src/test_creation/modules/checklist/checklist.py ./checklist/test-dump-csv

        Note that the supplied path must be a directory containing 3 CSV files:
        1. `overview.csv`
        2. `topics.csv`
        3. `tests.csv`
        """
        checklist = Checklist(checklist_path, checklist_format=ChecklistFormat.CSV)
        print(checklist.as_markdown())
        checklist.export_html("checklist.html", exist_ok=True)


    fire.Fire(example)
