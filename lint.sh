#!/bin/bash

# Run flake8 linting
echo "Running Flake8 linting..."
flake8 app/

# Check exit code
if [ $? -eq 0 ]; then
    echo "✅ Linting passed!"
else
    echo "❌ Linting failed. Please fix the issues above."
    exit 1
fi
