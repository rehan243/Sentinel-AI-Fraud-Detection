#!/bin/bash

# check if docker is running
if ! docker info > /dev/null 2>&1; then
    echo "docker is not running. please start docker and try again"
    exit 1
fi

# run linter
echo "running linter..."
flake8 src/ --max-line-length=88
if [ $? -ne 0 ]; then
    echo "linting failed, fix the issues above"
    exit 1
fi

# run tests
echo "running tests..."
pytest tests/
if [ $? -ne 0 ]; then
    echo "tests failed, fix the issues above"
    exit 1
fi

# build docker image
echo "building docker image..."
docker build -t fraud-detection .

# run docker container
echo "starting docker container..."
docker run --rm -p 5000:5000 fraud-detection

echo "dev setup complete, everything looks good"