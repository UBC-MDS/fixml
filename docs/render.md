# Rendering Documentations

This project comes with both reports rendered using Quarto, and API 
documentations rendered using Sphinx (the one you're reading right now!)

This page will guide through you the rendering process if you're interested 
in rendering them locally.

## Quarto reports

This includes the proposal, final report, and the human evaluations reports.
To render this, You must have Quarto installed in your system. You can 
obtain a copy of Quarto on [their official website](https://quarto.org).

After go to the project root folder and run this command: 
```bash
make clean && make all
````

The rendered reports will be located in `report/docs/`.

## Sphinx documentations

This includes the installation and quickstart guides, changelogs, API 
references and all other things related to the tool as a package.

To render this, you need to install the development build of this tool. The 
dependencies will only be installed when you use development build, but not 
the regular version of the package.

Refer to [the related documentation](contributing.md#get-started) for how to
install a development build of FixML.

After installing the build, run this to render the documentations in HTML:
```bash
cd docs/
make clean && make html
```

The rendered website will be located in `docs/_build/html/`.
