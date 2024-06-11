from typing import Union

from quarto import render

from ..mixins import RenderableMixin


class ResponseRenderer(RenderableMixin):
    def __init__(self, response_json, qmd_template):
        self._response_json = response_json
        self._qmd_template = qmd_template

