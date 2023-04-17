@list:
    just --list
    echo "Run pipenv run bin/toolbox for command line client."

# setup python environment
init:
    pipenv install --dev

run:
    @echo "please exwecute: pipenv run bin/toolbox"

# autolint with isort and black
lint:
    pipenv run isort .
    pipenv run black .

test:
    pipenv run pytest -v


