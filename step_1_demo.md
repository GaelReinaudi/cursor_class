# Step 1 Demo: Tests in 5 Minutes

## Setup
- Open `calculator.py` in Cursor
- File should show a comprehensive calculator module with NO existing tests
- Note: This code contains several bugs that the tests will help discover!

## Demo Flow

### 1. Generate Initial Test Suite
**Action**: Open chat and paste this prompt:

```
Create comprehensive pytest tests for the calculator.py module. 
```

**Expected**: Cursor generates `test_calculator.py`

### 2. Make Cursor Run the Tests
**Action**: After tests are generated, paste this prompt:

```
Now run these tests to see if there are any issues with my calculator implementation. Use pytest and show me the results.
```

**Expected**: Cursor will run `pytest test_calculator.py` and discover the bugs!

### 3. Auto-Execution Mode Demo
**Action**: When tests fail, paste this prompt:

Allow the the "Auto-Run" mode of the chat so you don't have to click the button all the time.


### 4. Coverage:
```
I need complete test coverage for all functions and classes. run the coverage and output the coverage in a coverage.txt file.
```

## Key Points to Highlight
- Cursor generates comprehensive tests automatically
- Tests catch bugs we didn't notice in code review
- Cursor can loop until reaching a solution
- Test-driven development prevents production bugs
- `.cursorrules` customizes Cursor's behavior

## Fallback Commands
If auto-execution doesn't work smoothly:
- `pytest test_calculator.py -v` (verbose output)
- `python -m pytest test_calculator.py` (alternative runner)
- `python test_calculator.py` (if made executable)

## Extra 10× Trick
**Action**: After all tests pass, paste:

```
Make test_calculator.py executable by adding a shebang and if __name__ == "__main__" block so I can run it directly with ./test_calculator.py
```

```
### 1. Introduce .cursorrules
**Action**: Create a new file `.cursorrules` in the root directory

**Content to paste in .cursorrules**:
```
You are an expert Python developer focused on writing comprehensive, high-quality code.

When generating tests:
- Use pytest framework
- Create thorough test coverage including edge cases
- Test both success and failure scenarios  
- Include fixtures where appropriate
- Test exception handling explicitly
- Group related tests in test classes when logical

When running tests:
- Always run the tests after creating them
- If tests fail, investigate and fix the issues
- Provide clear explanations of what went wrong
- Note, a failing tst could be a bug in the code or a typo in the test.
```

EXTRA: Ask cursor to edits its own rules