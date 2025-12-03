#!/bin/bash

echo "Testing shell script approach..."

# Test what the shell script does
echo "Command: uv run gen-erdiagram src/linkml_coral/schema/linkml_coral.yaml --classes Location Sample"

mkdir -p test_shell_output

uv run gen-erdiagram src/linkml_coral/schema/linkml_coral.yaml \
  --classes Location Sample \
  > test_shell_output/test.mmd 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Shell approach works!"
    echo "Generated $(wc -l < test_shell_output/test.mmd) lines"
else
    echo "❌ Shell approach also fails:"
    cat test_shell_output/test.mmd
fi