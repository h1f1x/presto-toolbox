list:
    just --list

# setup python environment
init:
    pipenv install --dev

run:
    pipenv run python -m presto.query

# autolint with isort and black
lint:
    pipenv run isort .
    pipenv run black .
