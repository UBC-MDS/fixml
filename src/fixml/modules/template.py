from typing import Union, Optional
from pathlib import Path

from jinja2 import Environment, PackageLoader, Template, meta


class TemplateLoader:
    """Static wrapper class for setting states for Jinja2's Environment."""

    template_exts = ["jinja", "j2"]
    env = Environment(
        loader=PackageLoader("fixml.data", "templates")
    )
    template_aliases = {
        "evaluation": "eval_report.md.jinja",
        "checklist": "checklist.md.jinja",
    }

    def __new__(cls):
        raise TypeError("This static class cannot be instantiated.")

    @classmethod
    def load(cls, template_name: str) -> Template:
        candidates = [template_name, cls.template_aliases.get(template_name)]
        candidates = [x for x in candidates if x is not None]
        return cls.env.select_template(candidates)

    @classmethod
    def load_from_external(cls, ext_template_path: Union[str, Path],
                           validate_template: Optional[str] = None) -> Template:
        """Load template from external file.

        Return the source as a Jinja2 Template when given a path.

        Parameters
        ----------
        ext_template_path : str or pathlib.Path
            Path to the external template file.
        validate_template : str, optional
            If provided, the external template source will be compared with the
            referred internal template to confirm all variables are present.
        """
        with open(ext_template_path, "r") as f:
            source = f.read()

        if validate_template:
            vars_external = cls._get_vars_from_source(source)
            vars_internal = cls.list_vars_in_template(validate_template)
            diff = set(vars_internal).difference(vars_external)
            if diff:
                raise ValueError(f"The external template does not contain all "
                                 f"variables present in the internal template "
                                 f"{validate_template}. Missing variables: "
                                 f"{diff}")
        return Template(source)

    @classmethod
    def _get_vars_from_source(cls, source: str) -> set[str]:
        ast = cls.env.parse(source)
        return meta.find_undeclared_variables(ast)

    @classmethod
    def list(cls) -> list[str]:
        return cls.env.list_templates(extensions=cls.template_exts)

    @classmethod
    def list_vars_in_template(cls, template_name: str) -> set[str]:
        """List all variables present in template."""
        template = cls.load(template_name)
        source = cls.env.loader.get_source(cls.env, template.name)[0]
        return cls._get_vars_from_source(source)