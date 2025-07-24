# Step 2 Demo: Multi-File Context & Self-Docs

## Setup
- Full-stack project with `backend/`, `frontend/`, and `tests/` folders
- Multiple interconnected files (Python API + React frontend)
- Perfect for demonstrating Cursor's codebase understanding

## Demo Flow

### 1. Show Cursor Knows Your Codebase
**Action**: Open chat and paste:

```
Explore and the explain how this application works. What does the backend do, how does the frontend connect to it, and what's the overall architecture?
```

**Expected**: Cursor analyzes all files and explains the full-stack architecture without needing to specify files

### 2. Ask Cursor to Map the Whole Repo
**Action**: Paste this prompt:

```
Now explore more, in order to create a Mermaid diagram showing the structure and relationships of this codebase. Include the file organization, data flow between frontend and backend, and how the components connect. Also include the approximate line number of the class and functions you discovered. Put all this in a architecture.md at the root of the project.
```

```
It is all unreadable . light text on light background... come on! And I want more details of the structure !
```

**Expected**: Cursor generates a comprehensive architecture.md file showing:
- Folder structure
- API endpoints
- React component flow
- Data relationships

### 3. Multi-File Edit Request
**Action**: Test Cursor's multi-file awareness:

```
I want to add a "priority" field to tasks (high, medium, low). Update the backend Task class, API endpoints, frontend interface, and tests. Show me exactly what changes are needed across all files. Refer to the architecture.md file for the exact location of the code to changes and plan accordingly.
```

**Expected**: Cursor identifies and proposes changes across:
- `backend/tasks.py` (Task class)
- `backend/main.py` (API responses)  
- `frontend/src/App.jsx` (UI for priority)
- `tests/test_tasks.py` (test updates)

### 4. Update .cursorrules for Living Documentation
**Action**: Add to `.cursorrules`:

```
When making changes to this codebase:
- Always update the architecture diagram when structure changes
- Keep API documentation in sync with endpoints
- Ensure frontend and backend changes are coordinated
- Update tests to reflect new functionality
```

### 5. Test the "Keep-Map-Updated" Rule
**Action**: Ask Cursor to implement the priority feature:

```
Implement the priority feature we discussed. Make all the necessary changes and update the architecture diagram to reflect the new data flow.
```

**Expected**: Cursor:
1. Makes coordinated changes across all files
2. Updates the Mermaid diagram automatically
3. Ensures consistency between frontend and backend

## Key Points to Highlight
- Cursor understands file relationships without explicit context
- Can visualize complex architectures instantly
- Coordinates changes across multiple languages/frameworks
- Maintains documentation automatically with proper rules
- Treats the entire codebase as connected, not isolated files

## Advanced Trick
**Action**: Show Cursor's investigation skills:

```
Is there any inconsistency or potential bug in how the frontend and backend handle task data? Check the data formats and API contracts.
```

This demonstrates Cursor can audit cross-file compatibility! 