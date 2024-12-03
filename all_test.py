import os
import shutil
import subprocess

# Paths
TEST_DIR = "tests"
VALID_DIR = os.path.join(TEST_DIR, "valid")
INVALID_DIR = os.path.join(TEST_DIR, "invalid")
EXPECTED_DIR = os.path.join(TEST_DIR, "outputs/expected_outputs")
ACTUAL_DIR = os.path.join(TEST_DIR, "outputs/actual_outputs")
VENV_PYTHON = "/media/samantha/disk2/VYPa/Compiler_project/vyp_env/bin/python3"  # Adjust to your virtualenv's Python
INTERPRETER = "vypint-1.0.jar"  # Path to the interpreter

# Clean output directories
def clean_output_dirs():
    """Remove and recreate actual output directories."""
    if os.path.exists(ACTUAL_DIR):
        shutil.rmtree(ACTUAL_DIR)
    os.makedirs(ACTUAL_DIR, exist_ok=True)

# Ensure subdirectory structure matches
def ensure_output_dirs(test_file_path, base_dir, output_dir):
    """
    Ensure the corresponding output directory structure matches the test file path.
    """
    relative_path = os.path.relpath(test_file_path, base_dir)
    output_path = os.path.join(output_dir, os.path.dirname(relative_path))
    os.makedirs(output_path, exist_ok=True)
    return os.path.join(output_path, os.path.basename(test_file_path))

# Run test case
def run_test(test_file, is_valid):
    """
    Run a single test, compile to VYPcode, execute with the interpreter, and compare outputs.
    """
    test_name = os.path.splitext(os.path.basename(test_file))[0]
    test_input_file = os.path.splitext(test_file)[0] + ".in"  # Check for corresponding input file
    vypcode_file = ensure_output_dirs(test_file, VALID_DIR if is_valid else INVALID_DIR, ACTUAL_DIR) + ".vypcode"
    actual_output_file = ensure_output_dirs(test_file, VALID_DIR if is_valid else INVALID_DIR, ACTUAL_DIR) + ".out"
    expected_output_file = ensure_output_dirs(test_file, VALID_DIR, EXPECTED_DIR) + ".out"

    # Step 1: Compile to VYPcode
    compile_result = subprocess.run(
        [VENV_PYTHON, "main.py", test_file],
        #["main.py", test_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Save .vypcode file or handle compilation failure
    if compile_result.returncode != 0:
        print(f"[FAIL] {test_name}: Compilation error\n")
        print(f"stdout:\n{compile_result.stdout}")
        print(f"stderr:\n{compile_result.stderr}")
        print(f"return code: {compile_result.returncode}")
        print(f"tested .vyp code: {test_file}")
        print("=+=+=+==+=+=+==+=+=+==+=+=+==+=+=+==+=+=+==+=+=+=")

        return
    else:
        with open(vypcode_file, "w") as vf:
            vf.write(compile_result.stdout)
        print(f"[PASS] {test_name}: Compilation successful.\n")
        print("=+=+=+==+=+=+==+=+=+==+=+=+==+=+=+==+=+=+==+=+=+=")


    # Step 2: Execute with interpreter (valid cases only)
    input_redirection = open(test_input_file, "r") if os.path.exists(test_input_file) else None
    interpreter_result = subprocess.run(
        ["java", "-jar", INTERPRETER, vypcode_file],
        stdin=input_redirection,  # Redirect input from the .in file if it exists
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if input_redirection:
        input_redirection.close()

    # Save interpreter output
    with open(actual_output_file, "w") as af:
        af.write(interpreter_result.stdout)

    # Display Results
    print(f"stdin: {test_input_file if os.path.exists(test_input_file) else 'N/A'}")
    print(f"stdout:\n{interpreter_result.stdout}")
    print(f"return code: {interpreter_result.returncode}")
    print(f"tested .vyp code: {test_file}\n")

    # Step 3: Compare actual output with expected output
    if os.path.exists(expected_output_file):
        with open(expected_output_file, "r") as ef, open(actual_output_file, "r") as af:
            if ef.read().strip() == af.read().strip():
                print(f"[PASS] {test_name}: Output matches expected.\n")
                print("=+=+=+==+=+=+==+=+=+==+=+=+==+=+=+==+=+=+==+=+=+=")
            else:
                print(f"[FAIL] {test_name}: Output mismatch.\n")
                print("=+=+=+==+=+=+==+=+=+==+=+=+==+=+=+==+=+=+==+=+=+=")
    else:
        print(f"[FAIL] {test_name}: Missing expected output file.\n")
        print("=+=+=+==+=+=+==+=+=+==+=+=+==+=+=+==+=+=+==+=+=+=")

# Run all test cases
def run_tests_in_dir(base_dir, is_valid):
    """
    Recursively find and run all tests in a directory and its subfolders.
    """
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".vyp"):
                print(f"Running test case: {file}")
                run_test(os.path.join(root, file), is_valid)

# Main script execution
def run_all_tests():
    """
    Run all valid and invalid test cases.
    """
    # Step 1: Clean previous outputs
    clean_output_dirs()

    # Step 2: Run valid test cases
    print("Running valid test cases...")
    print("=+=+=+==+=+=+==+=+=+==+=+=+==+=+=+==+=+=+==+=+=+=")

    run_tests_in_dir(VALID_DIR, is_valid=True)
    print("End of valid test cases...")
    print("=+=+=+==+=+=+==+=+=+==+=+=+==+=+=+==+=+=+==+=+=+=")


    # Step 3: Run invalid test cases
    print("Running invalid test cases...")
    print("=+=+=+==+=+=+==+=+=+==+=+=+==+=+=+==+=+=+==+=+=+=")

    run_tests_in_dir(INVALID_DIR, is_valid=False)
    print("End of invalid test cases...")

if __name__ == "__main__":
    run_all_tests()
