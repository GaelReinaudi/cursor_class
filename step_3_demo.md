# Step 3 Demo: Detective-Style Debugging

## Setup
- Script with silent failures (`scripts/name_formatter.py`)
- Code that "works" but has hidden bugs masked by bad exception handling
- Perfect for demonstrating systematic debugging with comprehensive logging

## Demo Flow

### 1. Initial Investigation Request
**Action**: Open chat and paste this prompt:

```
Run this script. It misearably fails and I want you to investigate, like Sherlock Holmes.
Add log lines all over so that you can follow in the terminal.
```

**Expected**: Cursor will:
- Run the script and discover silent failures
- Add comprehensive logging throughout all functions
- Transform the script into a fully instrumented debugging tool
- Uncover the real bug hidden by bad exception handling

### 2. The Investigation Results
**What Cursor Discovers**:
- Script was silently failing on single names ("Alice", "Charlie")
- IndexError when trying to access `components[1]` for single names
- Bad catch-all exception handler (`except: pass`) was masking all errors

**Terminal Output Shows**:
```
🎯 Testing: 'Alice'
❌ [apply_formatting_rules] ERROR: Missing last name! Only 1 components available
❌ [apply_formatting_rules] This is the BUG - no bounds checking!
❌ CAUGHT EXCEPTION: list index out of range
```

### 3. Fix Implementation
**Expected**: Cursor automatically:
- Adds bounds checking in `apply_formatting_rules()`
- Handles single names gracefully ("Alice" → "A.")
- Updates validation patterns for both single and full names
- Fixes the core IndexError bug

### 4. Clean Up After Investigation
**Action**: Once bug is fixed, paste:

```
good, cleanup abit the prints since the case is closed
```

**Expected**: Cursor removes verbose debug logging and creates clean, production-ready output:
```
📝 Name Formatter - Testing Suite
========================================
✅ 'Alice' → 'A.'
✅ 'Bob Smith' → 'B. Smith'
✅ 'Charlie' → 'C.'
✅ 'Diana Prince' → 'D. Prince'
```

## Key Points to Highlight
- Cursor acts like a detective, methodically adding logging everywhere
- Discovers bugs hidden by bad exception handling
- Fixes bounds checking issues and edge cases
- Transitions from debugging mode to production-ready code
- Handles the complete debugging lifecycle: investigate → fix → clean up

## The Detective Process
1. **Evidence Gathering**: Comprehensive logging added to every function
2. **Crime Scene Analysis**: Traces execution flow step-by-step
3. **Smoking Gun Found**: IndexError on `components[1]` access
4. **Case Solved**: Proper bounds checking + graceful single-name handling
5. **Clean Up**: Professional output with verbose logs removed

## Extra Fun Trick

```
Make this Sherlock Holmes thing a rule in the Cursor rules when investigating.
```

