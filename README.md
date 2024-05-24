# test_creation

`test_creation` is a tool designed to improve the quality and reliability of machine learning (ML) systems through comprehensive testing. By utilizing a manually curated checklist and Large Language Models (LLM), test_creation provides test completeness evaluations, missing test recommendations, and test function specification generation for ML system source codes.

For more details, see the [Documentation](https://ubc-mds.github.io/test-creation/proposal.html).

## Installation

1. Create a conda envionment using `environment.yml` in the repo:

```bash
conda env create -f environment.yml
```

2. Activate the newly created conda environment (default name `test-creation`):
```bash
conda activate test-creation
```

3. add `.env` with API key attached:
```bash
echo "OPENAI_API_KEY=..." > .env
```

4. Enjoy!

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
