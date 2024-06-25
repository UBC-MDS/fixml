from os.path import getmtime
from typing import Union, Optional
from pathlib import Path

from jinja2 import (Environment, PackageLoader, Template, meta, BaseLoader,
                    TemplateNotFound)


class ExternalFileLoader(BaseLoader):
    """A dumber FileSystemLoader which does not accept path and thus allows
    arbitrary file locations as valid template path."""
    def __init__(self):
        pass

    def get_source(self, environment: Environment, path: Union[str, Path]):
        resolved_path = Path(path).resolve()
        if not resolved_path.is_file():
            raise TemplateNotFound(path)
        mtime = getmtime(path)
        with open(path) as f:
            source = f.read()
        return source, resolved_path, lambda: mtime == getmtime(path)


class TemplateLoader:
    """Static wrapper class for setting states for Jinja2's Environment."""

    template_exts = ["jinja", "j2"]
    env = Environment(loader=PackageLoader("fixml.data", "templates"))
    ext_env = Environment(loader=ExternalFileLoader())
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

        Returns
        -------
        jinja2.Template
            Source file loaded as a Jinja2 Template.
        """
        template = cls.ext_env.get_template(ext_template_path)
        if validate_template:
            source = cls.ext_env.loader.get_source(cls.ext_env,
                                                   ext_template_path)[0]
            vars_external = cls._get_vars_from_source(source)
            vars_internal = cls.list_vars_in_template(validate_template)
            diff = set(vars_internal).difference(vars_external)
            if diff:
                raise ValueError(f"The external template does not contain all "
                                 f"variables present in the internal template "
                                 f"{validate_template}. Missing variables: "
                                 f"{diff}")

        return template

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