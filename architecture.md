# Architecture Overview

This document provides a comprehensive view of the cursor_class codebase structure, relationships, and data flow.

## 🏗️ **Codebase Structure & Component Map**

```mermaid
graph TB
    subgraph "🎯 Main Task Management Application"
        subgraph "Backend (FastAPI)"
            BE_MAIN["📄 backend/main.py<br/>Lines: 1-51<br/>────────────<br/>FastAPI app (L8)<br/>TaskCreate model (L12)<br/>get_tasks() (L16)<br/>create_task() (L22)<br/>complete_task() (L28)<br/>delete_task() (L35)<br/>root() (L42)"]
            
            BE_TASKS["📄 backend/tasks.py<br/>Lines: 1-70<br/>────────────<br/>Task class (L5-20)<br/>  - __init__ (L8)<br/>  - mark_completed (L14)<br/>TaskManager class (L23-70)<br/>  - add_task (L30)<br/>  - list_tasks (L36)<br/>  - get_task (L40)<br/>  - complete_task (L46)<br/>  - remove_task (L52)<br/>  - get_pending_tasks (L58)<br/>  - get_completed_tasks (L62)"]
        end
        
        subgraph "Frontend (React)"
            FE_APP["📄 frontend/src/App.jsx<br/>Lines: 1-164<br/>────────────<br/>App component (L3)<br/>fetchTasks() (L7)<br/>addTask() (L14)<br/>completeTask() (L29)<br/>deleteTask() (L41)<br/>useState hooks (L4-5)<br/>useEffect (L55)"]
            
            FE_INDEX["📄 frontend/src/index.jsx<br/>Lines: 1-10<br/>────────────<br/>React entry point<br/>ReactDOM.render (L6)"]
            
            FE_HTML["📄 frontend/public/index.html<br/>Lines: 1-17<br/>────────────<br/>HTML template<br/>Root div (L15)"]
        end
        
        subgraph "Tests"
            TEST_TASKS["📄 tests/test_tasks.py<br/>Lines: 1-121<br/>────────────<br/>TestTask class (L6)<br/>  - test_task_creation (L9)<br/>  - test_mark_completed (L16)<br/>  - test_task_repr (L22)<br/>TestTaskManager class (L30)<br/>  - test_add_task (L35)<br/>  - test_list_tasks (L42)<br/>  - test_get_task (L50)<br/>  - test_complete_task (L60)<br/>  - test_remove_task (L70)<br/>  - test_get_pending_tasks (L80)<br/>  - test_get_completed_tasks (L90)<br/>  - test_sequential_ids (L100)"]
        end
    end
    
    subgraph "🧮 Calculator Module (Demo/Tutorial)"
        CALC["📄 calculator.py<br/>Lines: 1-189<br/>────────────<br/>Calculator class (L5-49)<br/>  - add/subtract/multiply/divide (L11-26)<br/>  - power/square_root (L27-35)<br/>  - memory operations (L37-49)<br/>factorial() (L52)<br/>is_prime() (L59)<br/>fibonacci_sequence() (L72)<br/>calculate_average() (L87)<br/>find_gcd() (L93)<br/>StatisticsCalculator class (L101-149)<br/>  - median/mode/variance/std_dev<br/>convert_temperature() (L152)"]
        
        TEST_CALC["📄 test_calculator.py<br/>Lines: 1-384<br/>────────────<br/>TestCalculator class (L10)<br/>TestFactorial class (L85)<br/>TestIsPrime class (L96)<br/>TestFibonacciSequence class (L113)<br/>TestCalculateAverage class (L128)<br/>TestFindGCD class (L141)<br/>TestStatisticsCalculator class (L154)<br/>TestConvertTemperature class (L217)<br/>TestEdgeCases class (L294)"]
    end
    
    subgraph "👤 User Management (Stub/Demo)"
        USER_MGR["📄 user_manager.py<br/>Lines: 1-41<br/>────────────<br/>UserManager class (L3)<br/>  - add_user() (L7)<br/>  - hash_password() (L18)<br/>  - authenticate_user() (L21)<br/>  - get_user_by_id() (L24)<br/>  - update_user_email() (L27)<br/>  - delete_user() (L30)<br/>  - list_active_users() (L33)<br/>  - generate_session_token() (L36)<br/>  - validate_email() (L39)"]
    end
    
    subgraph "📋 Configuration & Docs"
        REQ["📄 requirements.txt<br/>────────────<br/>fastapi==0.104.1<br/>uvicorn[standard]==0.24.0<br/>pytest==7.4.3<br/>pydantic==2.5.0"]
        
        PKG["📄 frontend/package.json<br/>────────────<br/>react: ^18.2.0<br/>react-dom: ^18.2.0<br/>react-scripts: 5.0.1"]
        
        DOCS["📄 Documentation<br/>────────────<br/>README.md<br/>plan.md (tutorial plan)<br/>step_0_demo.md<br/>step_1_demo.md<br/>step_2_demo.md"]
    end
    
    %% Relationships
    BE_MAIN --> BE_TASKS
    FE_INDEX --> FE_APP
    FE_HTML --> FE_INDEX
    TEST_TASKS --> BE_TASKS
    TEST_TASKS --> BE_MAIN
    TEST_CALC --> CALC
    
    %% Styling
    classDef backend fill:#e1f5fe
    classDef frontend fill:#f3e5f5
    classDef tests fill:#e8f5e8
    classDef config fill:#fff3e0
    classDef demo fill:#fce4ec
    
    class BE_MAIN,BE_TASKS backend
    class FE_APP,FE_INDEX,FE_HTML frontend
    class TEST_TASKS,TEST_CALC tests
    class REQ,PKG,DOCS config
    class CALC,USER_MGR demo
```

## 🔄 **Data Flow & API Communication**

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant FE as 🎨 React Frontend<br/>(App.jsx)
    participant API as 🔧 FastAPI Backend<br/>(main.py)
    participant TM as 📋 TaskManager<br/>(tasks.py)
    participant T as 📝 Task Objects<br/>(in-memory)
    
    Note over U,T: Application Startup
    U->>FE: Opens browser
    FE->>FE: useEffect() triggers (L55)
    FE->>API: GET /tasks (L7-13)
    API->>TM: manager.list_tasks() (L18)
    TM->>T: Return task list
    TM-->>API: List[Task] objects
    API-->>FE: JSON task array
    FE->>FE: setTasks(data) (L12)
    FE-->>U: Display task list
    
    Note over U,T: Adding a Task
    U->>FE: Types task description
    U->>FE: Clicks "Add Task" or presses Enter
    FE->>FE: addTask() function (L14-28)
    FE->>API: POST /tasks {desc: "task"} (L17-24)
    API->>API: TaskCreate validation (L12)
    API->>TM: manager.add_task(desc) (L25)
    TM->>TM: Create Task instance (L30-33)
    TM->>T: Add to tasks list
    TM-->>API: Return new Task object
    API-->>FE: JSON task object (L26)
    FE->>FE: fetchTasks() refresh (L26)
    FE-->>U: Updated task list
    
    Note over U,T: Completing a Task
    U->>FE: Clicks "Complete" button
    FE->>FE: completeTask(id) (L29-40)
    FE->>API: PUT /tasks/{id} (L32-36)
    API->>TM: manager.complete_task(id) (L31)
    TM->>TM: Find task by ID (L46-51)
    TM->>T: task.mark_completed() (L14)
    TM-->>API: Boolean success (L50)
    API-->>FE: {status: "success"} (L34)
    FE->>FE: fetchTasks() refresh (L37)
    FE-->>U: Task marked with strikethrough
    
    Note over U,T: Deleting a Task
    U->>FE: Clicks "Delete" button
    FE->>FE: deleteTask(id) (L41-53)
    FE->>API: DELETE /tasks/{id} (L44-48)
    API->>TM: manager.remove_task(id) (L39)
    TM->>TM: Find and remove task (L52-57)
    TM->>T: Remove from tasks list
    TM-->>API: Boolean success (L56)
    API-->>FE: {status: "success"} (L40)
    FE->>FE: fetchTasks() refresh (L50)
    FE-->>U: Task removed from list
```

## 🔧 **Component Architecture & Dependencies**

```mermaid
graph LR
    subgraph "💾 Data Layer"
        MEMORY["📦 In-Memory Storage<br/>Python Lists<br/>No Persistence"]
    end
    
    subgraph "🔧 Business Logic"
        TASK_CLS["📋 Task Class<br/>(tasks.py L5-20)<br/>────────────<br/>• id: int<br/>• description: str<br/>• completed: bool<br/>• created_at: datetime<br/>• mark_completed()"]
        
        TASK_MGR["🎯 TaskManager<br/>(tasks.py L23-70)<br/>────────────<br/>• tasks: List[Task]<br/>• _next_id: int<br/>• CRUD operations<br/>• filtering methods"]
    end
    
    subgraph "🌐 API Layer"
        FASTAPI["🚀 FastAPI App<br/>(main.py L8)<br/>────────────<br/>• 5 REST endpoints<br/>• Pydantic validation<br/>• HTTP error handling<br/>• JSON serialization"]
        
        MODELS["📋 Pydantic Models<br/>(main.py L12)<br/>────────────<br/>• TaskCreate<br/>• Request validation<br/>• Type safety"]
    end
    
    subgraph "🎨 Presentation Layer"
        REACT_APP["⚛️ React App<br/>(App.jsx L3-164)<br/>────────────<br/>• Single component<br/>• State management<br/>• HTTP client<br/>• Event handlers<br/>• Conditional rendering"]
        
        DOM["🏠 DOM<br/>(index.html)<br/>────────────<br/>• Root div<br/>• React mounting point"]
    end
    
    subgraph "🧪 Testing Layer"
        UNIT_TESTS["🧪 Unit Tests<br/>(test_tasks.py)<br/>────────────<br/>• Task class tests<br/>• TaskManager tests<br/>• Full coverage<br/>• pytest framework"]
    end
    
    %% Dependencies
    REACT_APP --> FASTAPI
    FASTAPI --> MODELS
    FASTAPI --> TASK_MGR
    TASK_MGR --> TASK_CLS
    TASK_MGR --> MEMORY
    TASK_CLS --> MEMORY
    REACT_APP --> DOM
    UNIT_TESTS --> TASK_CLS
    UNIT_TESTS --> TASK_MGR
    
    %% HTTP Communication
    REACT_APP -.->|"HTTP REST API<br/>GET, POST, PUT, DELETE"| FASTAPI
    
    classDef data fill:#ffecb3
    classDef business fill:#e8f5e8
    classDef api fill:#e1f5fe
    classDef presentation fill:#f3e5f5
    classDef testing fill:#fff3e0
    
    class MEMORY data
    class TASK_CLS,TASK_MGR business
    class FASTAPI,MODELS api
    class REACT_APP,DOM presentation
    class UNIT_TESTS testing
```

## 📊 **File Statistics & Code Distribution**

| Component | Files | Lines | Purpose |
|-----------|-------|-------|---------|
| **Task Management Core** | 4 | 286 | Main application logic |
| - Backend API | 2 | 121 | FastAPI server + business logic |
| - Frontend React | 2 | 174 | User interface |
| **Testing** | 2 | 505 | Test coverage |
| - Task Tests | 1 | 121 | Unit tests for core functionality |
| - Calculator Tests | 1 | 384 | Comprehensive test suite |
| **Demo Components** | 2 | 230 | Tutorial/demo code |
| - Calculator Module | 1 | 189 | Mathematical operations |
| - User Manager | 1 | 41 | Stub implementation |
| **Configuration** | 4 | 111 | Project setup |
| **Documentation** | 4 | 206 | Guides and tutorials |
| **Total** | **16** | **1,338** | Complete codebase |

## 🔗 **Key Integration Points**

### **Frontend ↔ Backend Communication**
- **Protocol**: HTTP REST API
- **Base URL**: `http://localhost:8000`
- **Content-Type**: `application/json`
- **Error Handling**: HTTP status codes + JSON error responses

### **Backend ↔ Data Layer**
- **Storage**: In-memory Python lists (no persistence)
- **Data Models**: Pydantic for validation, Python dataclasses for logic
- **ID Management**: Auto-incrementing integer IDs

### **Testing Integration**
- **Framework**: pytest with comprehensive coverage
- **Test Types**: Unit tests for individual classes and functions
- **Isolation**: Fresh instances for each test method

## 🚀 **Deployment Architecture**

```mermaid
graph TB
    subgraph "Development Environment"
        subgraph "Frontend Server"
            REACT_DEV["React Dev Server<br/>Port: 3000<br/>npm start"]
        end
        
        subgraph "Backend Server"
            FASTAPI_DEV["FastAPI Server<br/>Port: 8000<br/>uvicorn main:app"]
        end
        
        subgraph "Testing"
            PYTEST["pytest<br/>Unit & Integration Tests"]
        end
    end
    
    subgraph "Browser"
        USER_BROWSER["User Browser<br/>http://localhost:3000"]
    end
    
    USER_BROWSER --> REACT_DEV
    REACT_DEV -.->|API Calls| FASTAPI_DEV
    PYTEST --> FASTAPI_DEV
    
    classDef server fill:#e1f5fe
    classDef client fill:#f3e5f5
    classDef test fill:#e8f5e8
    
    class FASTAPI_DEV server
    class REACT_DEV,USER_BROWSER client
    class PYTEST test
```

## 📝 **Architecture Notes**

### **Strengths**
- ✅ Clear separation of concerns between frontend and backend
- ✅ RESTful API design following HTTP conventions
- ✅ Comprehensive test coverage with clean test organization
- ✅ Modern technology stack (FastAPI + React)
- ✅ Type safety with Pydantic models and TypeScript potential

### **Areas for Enhancement**
- 🔄 Add database persistence (currently in-memory only)
- 🔐 Implement authentication and authorization
- 📝 Add input validation on frontend
- 🌐 Environment-based configuration for API URLs
- 📊 Add logging and monitoring capabilities
- 🧪 Add integration tests for full API workflows

### **Educational Value**
This codebase serves as an excellent example for demonstrating:
- Full-stack development patterns
- API design and frontend integration
- Testing strategies and coverage
- Code organization and architectural decisions
- Modern development tooling and frameworks 