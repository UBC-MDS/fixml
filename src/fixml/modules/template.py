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
    def list(cls) -> list[str]:
        return cls.env.list_templates(extensions=cls.template_exts)

    @classmethod
    def list_vars_in_template(cls, template_name: str) -> set[str]:
        """List all variables present in template."""
        template = cls.load(template_name)
        source = cls.env.loader.get_source(cls.env, template.name)[0]
        ast = cls.env.parse(source)
        return meta.find_undeclared_variables(ast)