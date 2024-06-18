# FixML

<p align="center">
    <img src="./img/logo.png?raw=true" width="175" height="175">
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

#### Test Evaluator

The test evaluator command is used to evaluate the test results of your
repository. It generates an evaluation report and provides various options for
customization, such as specifying a checklist file, output format, and
verbosity.

Example calls:
```bash
$ fixml

$ fixml evaluate /path/to/your/repo -e ./eval_report.html -v

$ fixml evaluate /path/to/your/repo -e ./eval_report.html -v -o -c checklist/checklist.csv
```

#### Test Spec Generator

The test spec generator command is used to generate a test specification from a
checklist. It allows for the inclusion of an optional checklist file to guide
the test specification generation process.

Example calls:
```bash
$ fixml generate test.py

$ fixml generate test.py -c checklist/checklist.csv
```

## Development Build

If you are interested in helping the development of this tool, or you would like
to get the cutting-edge version of this tool, you can install this tool via
conda.

To do this, ensure you have Miniconda/Anaconda installed on your system. You can
download miniconda
on [their official website](https://docs.anaconda.com/miniconda/).

### Step 1: Clone the Repository

Start by cloning the repository to your local machine. Open your terminal and
run the following command:


### Step 2: Create and Activate the Conda Environment
1. Create a conda environment using `environment.yml` in the repo:

Create a new Conda environment using the environment.yaml file provided in this
repository. This file contains all the necessary dependencies, including both
Python and Poetry versions.

```bash
$ git clone git@github.com:UBC-MDS/fixml.git
```

To create the environment, open your terminal and navigate to the directory
where the environment.yaml file is located. Then, run the following command:

2. Activate the newly created conda environment (default name `fixml`):

```bash
conda activate fixml
```

3. In the conda environment, `poetry` should be installed. Use Poetry to install
   the package:

```bash
poetry install
```

4. add `.env` with API key attached:

```bash
$ conda env create -f environment.yaml
$ conda activate fixml
```

### Step 3: Install the Package Using Poetry

With the Conda environment activated, you can now use Poetry to install the
package. Run the following command to install the package using Poetry:

```bash
$ poetry install
```

This command reads the pyproject.toml file in your project (if present) and
installs the dependencies listed there.

### Running the tests

Navigate to the project root directory and use the following command in terminal
to test the functions defined in the projects.

``` bash
$ pytest tests/*
```

### Troubleshooting

Environment Creation Issues: If you encounter problems while creating the Conda
environment, ensure that the environment.yaml file is in the correct directory
and that you have the correct version of Conda installed.

5. Enjoy! This package comes will an executable `fixml` and a bunch of scripts.
   Here are some examples:
```bash

# evaluate a repository and write a HTML report, display verbose messages
fixml evaluate $REPO_PATH ./report.html --verbose

# optional arguments to modify the default behaviour
# see `fixml evaluate --help`
fixml evaluate $REPO_PATH --test_dirs=./tests,./src/tests --model=gpt-4o

# export checklist items into a PDF, overwrite file if exists in the specified path
fixml checklist export ./checklist/checklist.csv/ checklist.pdf --overwrite
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