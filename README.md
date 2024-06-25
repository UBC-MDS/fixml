# FixML
[![Python 3.12.0+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Activity](https://img.shields.io/github/last-commit/ubc-mds/fixml/main.svg?style=flat)]()
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Documentation Status](https://readthedocs.org/projects/fixml/badge/?version=latest)](https://fixml.readthedocs.io/en/latest/?badge=latest)
![CI status check](https://github.com/UBC-MDS/fixml/actions/workflows/ci.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

<p align="center">
    <img src="https://raw.githubusercontent.com/UBC-MDS/fixml/main/img/logo.png?
raw=true" width="175" height="175">
</p>

A tool for providing context-aware evaluations using a checklist-based approach
on the Machine Learning project code bases.

## Motivation

Testing codes in Machine Learning project mostly revolves around ensuring the
findings are reproducible. To achieve this, currently it requires a lot of
manual efforts. It is because such projects usually have assumptions that are
hard to quantify in traditional software engineering approach i.e. code
coverage. One such example would be testing the model's performance, which will
not result in any errors, but we do expect this result to be reproducible by
others. Testing such codes, therefore, require us to not only quantitatively,
but also to qualitatively gauge how effective the tests are.

A common way to handle this currently is to utilize expertise from domain
experts in this area. Researches and guidelines have been done on how to
incorporate such knowledge through the use of checklists. However, this requires
manually validating the checklist items which usually results in poor
scalability and slow feedback loop for developers, which are incompatible with
today's fast-paced, competitive landscape in ML developments.

This tool aims to bridge the gap between these two different approaches, by
adding Large Language Models (LLMs) into the loop, given LLMs' recent
advancement in multiple areas including NLU tasks and code-related tasks. They
have been shown to some degrees the ability to analyze codes and to produce
context-aware suggestions. This tool simplifies such workflow by providing a
command line tool as well as a high-level API for developers and researchers
alike to quickly validate if their tests satisfy common areas that are required 
for reproducibility purposes.

Given LLMs' tendency to provide plausible but factually incorrect information,
extensive analyses have been done on ensuring the responses are aligned with
ground truths and human expectations both accurately and consistently. Based on
these analyses, we are also able to continuously refine our prompts and
workflows.

## Installation

This tool is on PyPI. To install, please run:

```bash
$ pip install fixml
```

## Usage

### CLI tool

Once installed, the tool offers a Command Line Interface (CLI) command `fixml`.
By using this command you will be able to evaluate your project code bases,
generate test function specifications, and perform various relevant tasks.

Run `fixml --help` for more details.

> [!IMPORTANT]
> By default, this tool uses OpenAI's `gpt3.5-turbo` for evaluation. To run any
command that requires calls to LLM (i.e. `fixml evaluate`, `fixml generate`),
an environment variable `OPENAI_API_KEY` needs to be set. To do so, either use
`export` to set the variable in your current session, or create a `.env` file
with a line `OPENAI_API_KEY={your-api-key}` saved in your working directory.

> [!TIP]
> Currently, only calls to OpenAI endpoints are supported. This tool is still in
ongoing development and integrations with other service providers and locally
hosted LLMs are planned.

#### Test Evaluator

The test evaluator command is used to evaluate the tests of your repository. It
generates an evaluation report and provides various options for customization,
such as specifying a checklist file, output format, and verbosity.

Example calls:
```bash
# Evaluate repo, and output the evalutions as a JSON file in working directory
$ fixml evaluate /path/to/your/repo

# Perform the above verbosely, and use the JSON file to export a HTML report
$ fixml evaluate /path/to/your/repo -e ./eval_report.html -v

# Perform the above, but use a custom checklist, and to overwrite existing report
$ fixml evaluate /path/to/your/repo -e ./eval_report.html -v -o -c checklist/checklist.csv

# Perform the above, and to use gpt-4o as the evaluation model
$ fixml evaluate /path/to/your/repo -e ./eval_report.html -v -o -c checklist/checklist.csv -m gpt-4o
```

#### Test Spec Generator

The test spec generator command is used to generate a test specification from a
checklist. It allows for the inclusion of an optional checklist file to guide
the test specification generation process.

Example calls:
```bash
# Generate test function specifications and to write them into a .py file
$ fixml generate test.py

# Perform the above, but to use a custom checklist
$ fixml generate test.py -c checklist/checklist.csv
```

### Package

Alternatively, you can use the package to import all components necessary for running the evaluation/generation workflows listed above.

The workflows used in the package have been designed to be fully modular. You
can easily switch between different prompts, models and checklists to use. You
can also write your own custom classes to extend the capability of this library.

Consult the API documentation on Readthedocs for more information and example calls.

## Development Build

If you are interested in helping the development of this tool, or you would like
to get the cutting-edge version of this tool, you can install this tool via
conda.

To do this, ensure you have Miniconda/Anaconda installed on your system. You can
download miniconda
on [their official website](https://docs.anaconda.com/miniconda/).


1. Clone this repository from GitHub:
```bash
$ git clone git@github.com:UBC-MDS/fixml.git
```

2. Create a conda environment:

```bash
$ conda env create -f environment.yaml
```

3. Activate the newly created conda environment (default name `fixml`):

```bash
$ conda activate fixml
```

4. Use `poetry` which is preinstalled in the conda environment to create a local package install:

```bash
$ poetry install
```

5. You now should be able to run `fixml`, try:
```bash
fixml --help
```

## Running the Tests

Navigate to the project root directory and use the following command in terminal
to run the test suite:

```bash
# skip integration tests
$ pytest -m "not integeration"

# run ALL tests, which requires OPENAI_API_KEY to be set
$ pytest
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note
that this project is released with a Code of Conduct. By contributing to this
project, you agree to abide by its terms.

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
