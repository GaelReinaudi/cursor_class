# Database Demo Setup

## 🗄️ Database Schema Overview

A comprehensive task management database with **7 tables** and multiple relationships demonstrating real-world database design patterns.

### 📊 Entity Relationship Diagram

```mermaid
erDiagram
    users {
        uuid id PK
        varchar username UK
        varchar email UK
        varchar password_hash
        varchar first_name
        varchar last_name
        boolean is_active
        boolean is_admin
        timestamp created_at
        timestamp updated_at
        timestamp last_login
    }

    categories {
        uuid id PK
        varchar name UK
        text description
        varchar color
        uuid created_by FK
        timestamp created_at
        timestamp updated_at
    }

    tasks {
        uuid id PK
        varchar title
        text description
        varchar status
        varchar priority
        timestamp due_date
        timestamp completed_at
        decimal estimated_hours
        decimal actual_hours
        uuid assigned_to FK
        uuid created_by FK
        timestamp created_at
        timestamp updated_at
    }

    task_categories {
        uuid task_id FK
        uuid category_id FK
        timestamp created_at
    }

    comments {
        uuid id PK
        uuid task_id FK
        uuid user_id FK
        text content
        boolean is_internal
        timestamp created_at
        timestamp updated_at
    }

    attachments {
        uuid id PK
        uuid task_id FK
        uuid uploaded_by FK
        varchar filename
        integer file_size
        varchar mime_type
        varchar file_path
        timestamp created_at
    }

    task_history {
        uuid id PK
        uuid task_id FK
        uuid user_id FK
        varchar action
        jsonb old_values
        jsonb new_values
        timestamp created_at
    }

    %% Relationships
    users ||--o{ tasks : "assigned_to"
    users ||--o{ tasks : "created_by"
    users ||--o{ categories : "created_by"
    users ||--o{ comments : "user_id"
    users ||--o{ attachments : "uploaded_by"
    users ||--o{ task_history : "user_id"
    
    tasks ||--o{ task_categories : "task_id"
    categories ||--o{ task_categories : "category_id"
    
    tasks ||--o{ comments : "task_id"
    tasks ||--o{ attachments : "task_id"
    tasks ||--o{ task_history : "task_id"

    %% Styling
    classDef primaryEntity fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef relationshipEntity fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef auditEntity fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    
    class users,tasks,categories primaryEntity
    class task_categories relationshipEntity
    class comments,attachments,task_history auditEntity
```

### 📋 Tables & Relationships

#### **Core Entities**
- **`users`** - User accounts and authentication
- **`tasks`** - Main task management with status, priority, dates
- **`categories`** - Task categorization with colors
- **`comments`** - Task discussions and collaboration

#### **Relationship Tables**
- **`task_categories`** - Many-to-many: tasks ↔ categories
- **`attachments`** - File uploads linked to tasks
- **`task_history`** - Audit trail with JSONB change tracking

### 🔗 Relationship Types Demonstrated

| Relationship | Example | Type |
|-------------|---------|------|
| One-to-Many | `users` → `tasks` (assigned_to) | Foreign Key |
| One-to-Many | `users` → `tasks` (created_by) | Foreign Key |
| One-to-Many | `tasks` → `comments` | Foreign Key |
| Many-to-Many | `tasks` ↔ `categories` | Junction Table |
| One-to-Many | `tasks` → `attachments` | Foreign Key |
| One-to-Many | `tasks` → `task_history` | Foreign Key |

### ⚡ Advanced Features

- **UUID Primary Keys** with `uuid-ossp` extension
- **Check Constraints** for data validation (status, priority)
- **Performance Indexes** on frequently queried columns
- **Auto-Updating Timestamps** via triggers
- **Cascading Deletes** for data integrity
- **JSONB Columns** for flexible audit logging

## 🚀 Quick Commands

### Start Services
```bash
# Start Postgres
docker-compose up -d postgres

# Verify connection
python db_health.py
```

### Health Checks
```bash
# Basic connectivity
python db_health.py

# Full schema validation
python db_health_enhanced.py
```

### Explore Data
```bash
# Interactive queries
python demo_queries.py

# Direct psql access
PGPASSWORD=demo psql -h localhost -p 5432 -U demo -d demo
```

## 📊 Sample Data

### Users (4 records)
- **admin** (Admin User) - Administrator
- **john_doe** (John Doe) - Developer  
- **jane_smith** (Jane Smith) - Designer
- **bob_wilson** (Bob Wilson) - DevOps

### Tasks (5 records)
- Authentication implementation (John, High Priority, In Progress)
- Landing page design (Jane, Medium Priority, Pending)
- Navbar bug fix (Bob, Urgent Priority, Pending)
- API documentation (John, Low Priority, Completed)
- CI/CD pipeline setup (Bob, High Priority, In Progress)

### Categories (6 options)
- Development (#e74c3c)
- Design (#9b59b6)  
- Testing (#f39c12)
- Documentation (#2ecc71)
- Bug Fixes (#e67e22)
- Research (#3498db)

## 🎯 Educational Value

This schema demonstrates:
- ✅ Modern database design patterns
- ✅ Performance optimization techniques
- ✅ Data integrity enforcement
- ✅ Flexible audit tracking
- ✅ Complex query relationships
- ✅ Real-world application structure

Perfect for learning SQL, testing ORMs, or building GraphQL APIs! 