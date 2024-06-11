# test_creation

A package for creating and managing software tests for applied machine learning code.

![](img/logo.jpg)

In the field of applied machine learning, robustness and reproducibility are crucial for building trustworthy software. Ensuring that machine learning code is reliable and produces consistent results is essential for the advancement of the field. The test-creation package addresses this need by providing a comprehensive system for creating and managing software tests specifically tailored for applied machine learning code.

## Why We Need the test-creation Package

The test-creation package is designed to enhance the robustness and reliability of applied machine learning software by:

- Reducing Errors: By following a structured checklist, common errors in data handling, model training, and evaluation can be minimized.
- Ensuring Data Quality: It includes tests for data presence, quality, and ingestion, ensuring that the input data meets the required standards before analysis begins.
- Validating Model Performance: Tests for model fitting and evaluation help in verifying that models are trained correctly and perform as expected.
- Verifying Artifacts: Ensuring the presence and quality of artifacts produced during the analysis, such as model outputs and reports.
- Promoting Best Practices: By incorporating widely recognized best practices from the scholarly literature and common pitfalls identified in machine learning workflows, it guides users in writing reliable and reproducible tests.

This package is particularly useful for data scientists and machine learning engineers who need to ensure the reliability of their code, as well as for generating reproducible test data and software tests.

## Package Summary
The `test-creation` package aims to facilitate the creation of robust and reproducible software tests for applied machine learning code. It includes functionalities to ensure the presence, quality, and proper ingestion of data at the beginning of the analysis, the correct fitting and evaluation of models, and the integrity of artifacts generated during the analysis.

## Installation

### Install from PyPI

Run this command to install the package

```bash
$ pip install test-creation
```

### Install from GitHub

Before proceeding with this installation, ensure you have Miniconda/Anaconda installed on your system. These tools provide support for creating and managing Conda environments.

#### Step 1: Clone the Repository

Start by cloning the repository to your local machine. Open your terminal and run the following command:

```bash
$ git clone git@github.com:UBC-MDS/test-creation.git
```

#### Step 2: Create and Activate the Conda Environment

Create a new Conda environment using the environment.yaml file provided in this repository. This file contains all the necessary dependencies, including both Python and Poetry versions.

To create the environment, open your terminal and navigate to the directory where the environment.yaml file is located. Then, run the following command:

```bash
$ conda env create -f environment.yaml
$ conda activate test-creation
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

```console
$ python ./src/test_creation/analyze.py <path-to-your-checklist> <path-to-your-repo>
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`test_creation` was created by John Shiu, Orix Au Yeung, Tony Shum, and Yingzi Jin. It is licensed under the terms of the MIT license for software code. Reports and instructional materials are licensed under the terms of the CC-BY 4.0 license.

## Credits

`test_creation` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

## Acknowledgements

We'd like to thank everyone who has contributed to the development of the `test-creation` package. This is a new project aimed at enhancing the robustness and reproducibility of applied machine learning software. It will be subsequently developed openly on GitHub and we welcome it to be read, revised, and supported by data scientists, machine learning engineers, educators, practitioners, and hobbyists. Your contributions and feedback are invaluable in making this package a reliable resource for the community.