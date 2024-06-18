from jinja2 import Environment, PackageLoader, Template, meta


class TemplateLoader:
    """Wrapper object for setting states for Jinja2's Environment."""

    def __init__(self):
        self.template_exts = ["jinja", "j2"]
        self.env = Environment(
            loader=PackageLoader("test_creation.data", "templates")
        )
        self.template_aliases = {
            "evaluation": "eval_report.md.jinja",
            "checklist": "checklist.md.jinja",
        }

    def load(self, template_name: str) -> Template:
        candidates = [template_name, self.template_aliases.get(template_name)]
        candidates = [x for x in candidates if x is not None]
        return self.env.select_template(candidates)

    def list(self) -> list[str]:
        return self.env.list_templates(extensions=self.template_exts)

    def list_vars_in_template(self, template_name: str) -> set[str]:
        """List all variables present in template."""
        template = self.load(template_name)
        source = self.env.loader.get_source(self.env, template.name)[0]
        ast = self.env.parse(source)
        return meta.find_undeclared_variables(ast)