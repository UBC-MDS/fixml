# FixML
[![Python 3.12.0+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Release](https://img.shields.io/github/release/ubc-mds/fixml.svg?style=flat)]()
[![PyPI - Version](https://img.shields.io/pypi/v/fixml)](https://pypi.org/project/fixml/)
[![GitHub Activity](https://img.shields.io/github/last-commit/ubc-mds/fixml/main.svg?style=flat)]()
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Documentation Status](https://readthedocs.org/projects/fixml/badge/?version=latest)](https://fixml.readthedocs.io/en/latest/?badge=latest)
![CI status check](https://github.com/UBC-MDS/fixml/actions/workflows/ci.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

<p align="center">
    <img src="https://raw.githubusercontent.com/UBC-MDS/fixml/main/img/logo.png?raw=true" width="175" height="175">
</p>

A tool for providing context-aware evaluations using a checklist-based approach
on the Machine Learning project code bases.

## Documentations

- Guides and API documentations: [https://fixml.readthedocs.org](https://fixml.readthedocs.org)
- Reports and proposals: [https://ubc-mds.github.io/fixml](https://ubc-mds.github.io/fixml)

## Installation

```bash
pip install fixml

# For unix-like systems e.g. Linux, macOS 
export OPENAI_API_KEY={your-openai-api-key}

# For windows systems
set OPENAI_API_KEY={your-openai-api-key}
```

For more detailed installation guide,
visit [the related page on ReadtheDocs](https://fixml.readthedocs.io/en/latest/installation.html).

## Usage

### CLI tool

FixML offers a CLI command to quick and easy way to evaluate existing tests and
generate new ones.

#### Test Evaluator

Here is an example command to evaluate a local repo:

```bash
fixml evaluate /path/to/your/repo \
  --export_report_to=./eval_report.html --verbose
```

#### Test Spec Generator

Here is an example command to evaluate a local repo
```bash
fixml generate test.py
```

> [!TIP]
> Run command `fixml {evaluate|generate} --help` for more information and all
> available options.
>
> You can also refer
> to [our Quickstart guide](https://fixml.readthedocs.io/en/latest/quickstart.html)
> on more detailed walkthrough on how to use the CLI tool.

### Package

Alternatively, you can use the package to import all components necessary for
running the evaluation/generation workflows listed above.

Consult [our documentation on using the API](https://fixml.readthedocs.io/en/latest/using-the-api.html)
for more information and example calls.

## Development Build

Please refer to [the related page in our documentation](https://fixml.readthedocs.io/en/latest/install_devel_build.html).

## Rendering Documentations

Please refer to [the related page in our documentation](https://fixml.readthedocs.io/en/latest/render.html).

## Contributing

Interested in contributing? Check out
the [contributing guidelines](CONTRIBUTING.md). Please note that this project is
released with a [Code of Conduct](CONDUCT.md). By contributing to this project,
you agree to abide by its terms.

## License

`fixml` was created by John Shiu, Orix Au Yeung, Tony Shum, and Yingzi Jin as a
deliverable product during our capstone project of the UBC-MDS program in
collaboration with Dr. Tiffany Timbers and Dr. Simon Goring. It is licensed
under the terms of the MIT license for software code. Reports and instructional
materials are licensed under the terms of the CC-BY 4.0 license.

## Citation

If you use fixml in your work, please cite:

```
@misc{mds2024fixml,
  author =       {John Shiu, Orix Au Yeung, Tony Shum, and Yingzi Jin},
  title =        {fixml: A Comprehensive Tool for Test Evaluation and Specification Generation},
  howpublished = {\url{https://https://github.com/UBC-MDS/fixml}},
  year =         {2024}
}
```

## Acknowledgements
We'd like to thank everyone who has contributed to the development of
the `fixml` package. This is a new project aimed at enhancing the robustness and
reproducibility of applied machine learning software. It is meant to be a
research tool and is currently hosting on GitHub as an open source project. We
welcome it to be read, revised, and supported by data scientists, machine
learning engineers, educators, practitioners, and hobbyists alike. Your
contributions and feedback are invaluable in making this package a reliable
resource for the community. 

Special thanks to the University of British Columbia (UBC) and the University of
Wisconsin-Madison for their support and resources. We extend our gratitude to
Dr. Tiffany Timbers and Dr. Simon Goringfor their guidance and expertise, which
have been instrumental in the development of this project.
