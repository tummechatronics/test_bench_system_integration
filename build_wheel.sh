#!/bin/bash

# Stop on first error
set -e

echo "Checking versions..."
hatch --version
hatch run ruff --version
hatch run pytest --version

echo "Building package..."
hatch build

echo "Running linter..."
hatch run lint


echo "All tasks completed successfully."
