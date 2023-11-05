# OrcaFlex .yml Generator

Generates OrcaFlex simulation model text files with diverse input parameters.

## Installation Instructions

### Poetry

https://python-poetry.org/docs/#installation

### Repository
In your terminal, type the following:

```sh
git clone https://github.com/timiancam/orcaflex_yml_generator
cd orcaflex_yml_generator
poetry shell
poetry install # Check that your terminal is in the correct virtual environment
```

## Usage Instructions

Run the .py file.

## To do:

* Final check
* Charlotte check
* Better Format / Spacing / Indentation control for text - replaces spaces with \t?
* Potential efficiency gain? - remove for loop in def get_user_support_length_text()
  * similarly for get_support_arclengths()?
  * similarly for get_support_text_part1()?
  * similarly for get_support_text_part2()?
  * similarly for nested for loop?
  * https://stackoverflow.com/questions/42098527/print-a-nested-lists-line-by-line-without-for-loop
