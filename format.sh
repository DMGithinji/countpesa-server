#!/bin/bash

# Format code with black
echo "Formatting code with black..."
black app/

# Check if there are still flake8 errors
echo "Checking for remaining issues with flake8..."
flake8 app/

if [ $? -eq 0 ]; then
    echo "✅ All issues fixed! Your code is now formatted and passes linting."
else
    echo "⚠️ Some issues couldn't be fixed automatically. Please fix them manually."
    exit 1
fi