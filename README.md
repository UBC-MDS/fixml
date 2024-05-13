# test_creation

To be filled

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

### code_analyzer

This is used to analyze and extract information from a downloaded repo.

There is a file containing the example calls. Run:

```console
$ python ./src/code_analyzer/example.py <path-to-your-repo>
```


## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`test_creation` was created by John Shiu, Orix Au Yeung, Tony Shum, Yingzi Jin. It is licensed under the terms of the MIT license.

## Credits

`test_creation` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
