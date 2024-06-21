from importlib.resources import files

import pytest
from jinja2 import Template, TemplateNotFound
from fixml.modules.template import TemplateLoader


@pytest.mark.parametrize(
    "template_name",
    ["evaluation", "checklist", "eval_report.md.jinja", "checklist.md.jinja"]
)
def test_template_can_load(template_name):
    t = TemplateLoader.load(template_name)
    assert type(t) == Template


@pytest.mark.parametrize(
    "template_name",
    ["evaluation123" "eval_report.md",
     "./src/fixml/data/templates/checklist.md.jinja"]
)
def test_errors_will_return_when_no_templates_can_be_found(template_name):
    with pytest.raises(TemplateNotFound):
        t = TemplateLoader.load(template_name)


def test_all_templates_can_be_listed():
    template_data_dir = files("fixml.data.templates")
    internal_templates = [x.name for x in template_data_dir.iterdir()]
    assert internal_templates == TemplateLoader.list()


@pytest.mark.parametrize(
    "template_path, template_name",
    [
        ("./src/fixml/data/templates/checklist.md.jinja", "checklist"),
        ("./src/fixml/data/templates/eval_report.md.jinja", "evaluation"),
    ]
)
def test_templates_valid_themselves_when_loaded_externally(template_path,
                                                           template_name):
    TemplateLoader.load_from_external(template_path,
                                      validate_template=template_name)


@pytest.mark.parametrize(
    "template_path, template_name",
    [
        ("README.md", "checklist"),
        ("./src/fixml/data/templates/checklist.md.jinja", "evaluation"),
    ]
)
def test_external_templates_fail_validation_when_vars_dont_match(template_path,
                                                                 template_name):
    with pytest.raises(ValueError):
        TemplateLoader.load_from_external(template_path,
                                          validate_template=template_name)
