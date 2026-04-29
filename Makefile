# makefile for managing dev tasks

.PHONY: lint test docker local-run

# run linting on the codebase
lint:
    # using flake8 for linting
    flake8 src/

# run tests with pytest
test:
    # make sure to include coverage
    pytest --cov=src/ tests/

# build and run docker container
docker:
    # build the docker image
    docker build -t fraud-detector .

    # run the docker container
    docker run -p 5000:5000 fraud-detector

# run the application locally
local-run:
    # make sure to set up the virtual environment first
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    # start the app
    python src/main.py