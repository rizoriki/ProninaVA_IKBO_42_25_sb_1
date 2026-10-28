#!/bin/bash
# Real OS script to test the emulator with various VFS configurations

echo "=== Test 1: Minimal VFS ==="
./run.sh --vfs tests/test_vfs_minimal.json --script tests/test_script1.sh

echo -e "\n=== Test 2: Complex VFS (3 levels) ==="
./run.sh --vfs tests/test_vfs_complex.json --script tests/test_script2.sh

echo -e "\n=== Test 3: VFS Load Error (File not found) ==="
./run.sh --vfs tests/nonexistent.json

echo -e "\n=== Test 4: VFS Load Error (Invalid format) ==="
echo "invalid json {" > tests/invalid.json
./run.sh --vfs tests/invalid.json
rm -f tests/invalid.json

echo -e "\n=== All tests completed ==="
