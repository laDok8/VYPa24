import os
import shutil
import subprocess

# Paths
TEST_DIR = "tests"
VALID_DIR = os.path.join(TEST_DIR, "valid")
INVALID_DIR = os.path.join(TEST_DIR, "invalid")
EXPECTED_DIR = "outputs/expected-valid"
ACTUAL_DIR = "outputs/actual"

# Clean output directories
def clean_output_dirs():
    """Remove and recreate output directories."""
    if os.path.exists(ACTUAL_DIR):
        shutil.rmtree(ACTUAL_DIR)
    if os.path.exists(EXPECTED_DIR):
        shutil.rmtree(EXPECTED_DIR)
    os.makedirs(ACTUAL_DIR, exist_ok=True)
    os.makedirs(EXPECTED_DIR, exist_ok=True)

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
    Run a single test, compile to VYPcode, and execute with the interpreter if valid.
    """
    test_name = os.path.splitext(os.path.basename(test_file))[0]
    vypcode_file = ensure_output_dirs(test_file, VALID_DIR if is_valid else INVALID_DIR, ACTUAL_DIR) + ".vypcode"
    actual_output_file = ensure_output_dirs(test_file, VALID_DIR if is_valid else INVALID_DIR, ACTUAL_DIR) + ".out"
    expected_output_file = ensure_output_dirs(test_file, VALID_DIR, EXPECTED_DIR) + ".out"

    # Step 1: Compile to VYPcode
    
    #venv_python = "/media/samantha/disk2/VYPa/Compiler_project/vyp_env/bin/python3"
    compile_result = subprocess.run(
        #[venv_python, "main.py", test_file],
        ["python3", "src/main.py", test_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Save .vypcode file or handle compilation failure
    if compile_result.returncode != 0:
        if is_valid:
            print(f"[FAIL] {test_name}: Compilation error\n{compile_result.stderr}")
        else:
            print(f"[PASS] {test_name}: Correctly failed to compile.")
        return
    else:
        if not is_valid:
            print(f"[FAIL] {test_name}: Incorrectly compiled.")
            return
        with open(vypcode_file, "w") as vf:
            vf.write(compile_result.stdout)
        print(f"[PASS] {test_name}: Compilation successful.")

    # Step 2: Execute with interpreter (valid cases only)
    interpreter_result = subprocess.run(
        ["java", "-jar", "vypint-1.0.jar", vypcode_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Save interpreter output
    with open(actual_output_file, "w") as af:
        af.write(interpreter_result.stdout)

    # Step 3: Generate expected output if missing
    if not os.path.exists(expected_output_file):
        with open(expected_output_file, "w") as ef:
            ef.write(interpreter_result.stdout)
        print(f"[INFO] Generated expected output for {test_name}")

# Run all test cases
def run_tests_in_dir(base_dir, is_valid):
    """
    Recursively find and run all tests in a directory and its subfolders.
    """
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".vyp"):
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
    run_tests_in_dir(VALID_DIR, is_valid=True)

    # Step 3: Run invalid test cases
    print("Running invalid test cases...")
    run_tests_in_dir(INVALID_DIR, is_valid=False)

if __name__ == "__main__":
    run_all_tests()
