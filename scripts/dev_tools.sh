#!/bin/bash

# this is a simple dev tools script
# it'll help with linting and running tests

set -e  # exit immediately if a command exits with a non-zero status

# function to run flake8 for linting
run_lint() {
    echo "running linter..."
    flake8 src/  # linting the src directory
}

# function to run tests
run_tests() {
    echo "running tests..."
    pytest tests/  # running tests from the tests directory
}

# function to build and run docker container
run_docker() {
    echo "building and running docker container..."
    docker-compose up --build  # build and start the container
}

# check command line arguments
if [ "$#" -eq 0 ]; then
    echo "please provide a command: lint, test, or docker"
    exit 1
fi

# handle commands
case "$1" in
    lint)
        run_lint
        ;;
    test)
        run_tests
        ;;
    docker)
        run_docker
        ;;
    *)
        echo "unknown command: $1"
        echo "valid commands: lint, test, docker"
        exit 1
        ;;
esac

# TODO: consider adding more commands like format or build