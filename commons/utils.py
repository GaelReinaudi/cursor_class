"""
Utility functions for the commons package.
Includes pytest_this_file for making test files executable.
"""
import subprocess
import sys
from pathlib import Path


def pytest_this_file() -> None:
    """
    Run pytest on the current file.
    This function is called from the if __name__ == "__main__" block
    in test files to make them easily executable/debuggable.
    """
    # Get the file that called this function
    import inspect
    frame = inspect.currentframe()
    if frame is None:
        print("Error: Cannot determine calling file")
        return
    
    caller_frame = frame.f_back
    if caller_frame is None:
        print("Error: Cannot determine calling file")
        return
    
    caller_file = caller_frame.f_globals.get("__file__")
    if caller_file is None:
        print("Error: Cannot determine calling file")
        return
    
    file_path = Path(caller_file)
    
    # Run pytest with verbose output and coverage if available
    cmd = [
        sys.executable, "-m", "pytest",
        str(file_path),
        "-v",
        "--tb=short"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"✅ Tests passed for {file_path.name}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed for {file_path.name} with exit code {e.returncode}")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("❌ pytest not found. Please install with: uv pip install -e '.[dev]'")
        sys.exit(1) 