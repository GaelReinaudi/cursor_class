# Step 0 Demo: Autocomplete & Drop-in Class

## Setup
- Open `user_manager.py` in Cursor
- File should show a basic UserManager class with method stubs

## Demo Flow

### 1. Import Autocomplete
**Action**: Position cursor at the top of the file and start typing:
```
import has
```
**Expected**: Cursor suggests `hashlib` - accept the suggestion

**Action**: Press Enter and start typing:
```
from date
```
**Expected**: Cursor suggests `from datetime import datetime` - accept

### 2. Method Implementation Autocomplete
**Action**: Click inside the `hash_password` method (after the `pass`) and delete `pass`

**Action**: Start typing:
```
return hashlib.sha256(password.encode()).hexdigest()
```
**Expected**: Cursor autocompletes the method call and suggests the full implementation

### 3. Smart Context-Aware Suggestions
**Action**: Go to `validate_email` method, delete `pass` and start typing:
```
import re
return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None
```
**Expected**: Cursor suggests regex patterns for email validation

### 4. Drop-in Class Feature
**Action**: Position cursor after the entire class and press Enter twice

**Prompt to paste in chat**:
```
Add a simple User dataclass with fields: id, username, email, password_hash, created_at, is_active (default True)
```

**Expected**: Cursor generates a complete dataclass that integrates well with the existing UserManager

### 5. Method Completion with Context
**Action**: Go to `authenticate_user` method, delete `pass`

**Action**: Start typing:
```
for user in self.users:
    if user['username'] == username:
```
**Expected**: Cursor suggests the complete authentication logic including password verification

### 6. Auto-import Suggestions
**Action**: Try to use `uuid.uuid4()` in the `generate_session_token` method

**Expected**: Cursor automatically suggests adding `import uuid` at the top

## Key Points to Highlight
- Cursor understands context (knows we're working with user management)
- Suggests realistic, working code (not just syntax)
- Automatically handles imports
- Learns from existing code patterns in the file
- Provides complete implementations, not just snippets

## Fallback if Autocomplete is Slow
If autocomplete suggestions don't appear quickly, use Tab to trigger them or use Ctrl+Space to manually invoke completions. 