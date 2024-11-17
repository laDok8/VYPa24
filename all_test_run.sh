#!/bin/bash
# Activate Python Virtual Environment

source /media/samantha/disk2/VYPa/Compiler_project/vypa_env/bin/activate

# Paths
TEST_DIR="tests"
VALID_DIR="$TEST_DIR/valid"
INVALID_DIR="$TEST_DIR/invalid"
EXPECTED_DIR="outputs/valid"
ACTUAL_DIR="outputs/actual"
mkdir -p "$EXPECTED_DIR" "$ACTUAL_DIR"

# Colors for output
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
NC="\033[0m"  # No color

# Check required directories
if [ ! -d "$VALID_DIR" ] || [ ! -d "$INVALID_DIR" ]; then
    echo -e "${RED}One or more required directories (valid/invalid) are missing.${NC}"
    exit 1
fi

# Check for diff command
if ! command -v diff >/dev/null 2>&1; then
    echo -e "${RED}diff command not found. Please install it.${NC}"
    exit 1
fi

echo -e "${GREEN}Running valid test cases...${NC}"

# Valid tests
if [ -z "$(ls -A $VALID_DIR/*.vyp 2>/dev/null)" ]; then
    echo -e "${RED}No valid test cases found in $VALID_DIR.${NC}"
else
    for test_file in "$VALID_DIR"/*.vyp; do
        test_name=$(basename "$test_file" .vyp)
        expected_output="$EXPECTED_DIR/$test_name.out"
        actual_output="$ACTUAL_DIR/$test_name.out"

        # Check and generate expected output if missing
        if [ ! -f "$expected_output" ]; then
            echo -e "${YELLOW}[INFO] Generating missing expected output for $test_name...${NC}"
            python3 main.py "$test_file" > "$expected_output" 2>&1
            if [ $? -ne 0 ]; then
                echo -e "${RED}[FAIL] $test_name: Failed to generate expected output (compiler error).${NC}"
                continue
            fi
        fi

        # Run the compiler to generate actual output
        python3 main.py "$test_file" > "$actual_output" 2>&1
        if [ $? -eq 0 ]; then
            # Compare actual vs. expected output
            if diff -q "$expected_output" "$actual_output" >/dev/null 2>&1; then
                echo -e "${GREEN}[PASS] $test_name${NC}"
            else
                echo -e "${RED}[FAIL] $test_name: Output does not match expected.${NC}"
                echo "Differences:"
                diff "$expected_output" "$actual_output"
            fi
        else
            echo -e "${RED}[FAIL] $test_name: Compiler exited with an error.${NC}"
        fi
    done
fi

echo -e "${GREEN}Running invalid test cases...${NC}"

# Invalid tests
if [ -z "$(ls -A $INVALID_DIR/*.vyp 2>/dev/null)" ]; then
    echo -e "${RED}No invalid test cases found in $INVALID_DIR.${NC}"
else
    for test_file in "$INVALID_DIR"/*.vyp; do
        test_name=$(basename "$test_file" .vyp)

        # Run the compiler
        python3 main.py "$test_file" > /dev/null 2>&1
        if [ $? -ne 0 ]; then
            echo -e "${GREEN}[PASS] $test_name: Correctly failed to compile.${NC}"
        else
            echo -e "${RED}[FAIL] $test_name: Incorrectly compiled without errors.${NC}"
        fi
    done
fi

echo -e "${GREEN}Testing complete.${NC}"