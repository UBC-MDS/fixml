# fixml

<p align="center">
    <img src="./img/logo.png?raw=true" width="175" height="175">
</p>


A system for evaluating the test quality per each important test area in ML and generating test specifications specifically.

## Why We Need the test-creation Package

This package is particularly useful for data scientists and machine learning engineers who need to ensure the reliability of their code, as well as for generating reproducible test data and software tests.

## Installation

### Install from PyPI

Run this command to install the package

```bash
$ pip install fixml
```

### Install from GitHub

Before proceeding with this installation, ensure you have Miniconda/Anaconda installed on your system. These tools provide support for creating and managing Conda environments.

#### Step 1: Clone the Repository

Start by cloning the repository to your local machine. Open your terminal and run the following command:

```bash
$ git clone git@github.com:UBC-MDS/fixml.git
```

#### Step 2: Create and Activate the Conda Environment

Create a new Conda environment using the environment.yaml file provided in this repository. This file contains all the necessary dependencies, including both Python and Poetry versions.

To create the environment, open your terminal and navigate to the directory where the environment.yaml file is located. Then, run the following command:

```bash
$ conda env create -f environment.yaml
$ conda activate fixml
```

#### Step 3: Install the Package Using Poetry

With the Conda environment activated, you can now use Poetry to install the package. Run the following command to install the package using Poetry:

```bash
$ poetry install
```

This command reads the pyproject.toml file in your project (if present) and installs the dependencies listed there.

#### Running the tests
Navigate to the project root directory and use the following command in terminal to test the functions defined in the projects. 

``` bash
$ pytest tests/*
```

#### Troubleshooting
Environment Creation Issues: If you encounter problems while creating the Conda environment, ensure that the environment.yaml file is in the correct directory and that you have the correct version of Conda installed.

## Usage

### Test Evaluator

#### Description
The test evaluator command is used to evaluate the test results of your repository. It generates an evaluation report and provides various options for customization, such as specifying a checklist file, output format, and verbosity.

#### Example

```bash
$ fixml evaluate /path/to/your/repo -e ./eval_report.html -v -o -c checklist/checklist.csv
```

or
```bash
$ fixml evaluate /path/to/your/repo -e ./eval_report.html -v
```

### Test Spec Generator

#### Description
The test spec generator command is used to generate a test specification from a checklist. It allows for the inclusion of an optional checklist file to guide the test specification generation process.


#### Example
```bash
$ fixml generate test.py -c checklist/checklist.csv
```

or
```bash
$ fixml generate test.py

```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`fixml` was created by John Shiu, Orix Au Yeung, Tony Shum, and Yingzi Jin. It is licensed under the terms of the MIT license for software code. Reports and instructional materials are licensed under the terms of the CC-BY 4.0 license.

## Credits

`fixml` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

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

We'd like to thank everyone who has contributed to the development of the `fixml` package. This is a new project aimed at enhancing the robustness and reproducibility of applied machine learning software. It will be subsequently developed openly on GitHub and we welcome it to be read, revised, and supported by data scientists, machine learning engineers, educators, practitioners, and hobbyists. Your contributions and feedback are invaluable in making this package a reliable resource for the community.