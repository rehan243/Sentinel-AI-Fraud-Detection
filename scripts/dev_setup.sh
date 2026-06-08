#!/bin/bash

# this script sets up the development environment
# it runs linting and tests for the project

set -e  # exit on error

# function to run linters
run_linters() {
    echo "running linters..."
    flake8 src/  # check for python style issues
    black --check src/  # check for proper formatting
}

# function to run tests
run_tests() {
    echo "running tests..."
    pytest tests/  # execute tests in the tests folder
}

# main function to drive the script
main() {
    echo "setting up development environment"
    
    run_linters  # check for code quality
    run_tests  # make sure tests pass

    echo "dev setup complete"
}

# run the main function
main "$@"

# TODO: consider adding options for docker build and local run in the future