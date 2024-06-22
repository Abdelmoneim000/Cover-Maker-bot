#!/bin/bash
# This script is used to check installed packages for the project.
MODULES=$(grep -h import main.py | cut -d " " -f 2)
echo $MODULES

# Clear the requirements.txt file
> requirements.txt

for module in $MODULES; do
    # Try to show the package information
    output=$(pip show $module)
    if [ -z "$output" ]; then
        # If not found, try with .py suffix
        module_with_py="$module.py"
        output=$(pip show "$module_with_py")
    else
        module_with_py=$module
    fi

    # Extract the version field and append to requirements.txt
    if [ -n "$output" ]; then
        version=$(echo "$output" | awk '/^Version: / {print $2}')
        echo "$module_with_py==$version" >> requirements.txt
    else
        echo "Package $module not found"
    fi
done
