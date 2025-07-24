"""
Database schema setup script for the demo database.
Creates all tables, relationships, and sample data as documented in DATABASE_SETUP.md.
Run: python setup_database.py
"""
import psycopg2
import psycopg2.extras
import sys
from datetime import datetime, timedelta
import uuid

def connect_db():
    """Connect to the demo database."""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="demo",
            user="demo",
            password="demo",
            connect_timeout=3,
        )
        return conn
    except Exception as exc:
        print(f"❌ Database connection failed: {exc}")
        sys.exit(1)

def create_extensions(cursor):
    """Create required extensions."""
    print("🔧 Creating database extensions...")
    cursor.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    print("✅ UUID extension created")

def create_tables(cursor):
    """Create all database tables."""
    print("🏗️ Creating database tables...")
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            is_active BOOLEAN DEFAULT TRUE,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        );
    """)
    
    # Categories table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            name VARCHAR(100) UNIQUE NOT NULL,
            description TEXT,
            color VARCHAR(7) NOT NULL,
            created_by UUID REFERENCES users(id) ON DELETE SET NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled')),
            priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
            due_date TIMESTAMP,
            completed_at TIMESTAMP,
            estimated_hours DECIMAL(5,2),
            actual_hours DECIMAL(5,2),
            assigned_to UUID REFERENCES users(id) ON DELETE SET NULL,
            created_by UUID REFERENCES users(id) ON DELETE SET NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Task-Categories junction table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_categories (
            task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
            category_id UUID REFERENCES categories(id) ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (task_id, category_id)
        );
    """)
    
    # Comments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
            user_id UUID REFERENCES users(id) ON DELETE SET NULL,
            content TEXT NOT NULL,
            is_internal BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Attachments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attachments (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
            uploaded_by UUID REFERENCES users(id) ON DELETE SET NULL,
            filename VARCHAR(255) NOT NULL,
            file_size INTEGER,
            mime_type VARCHAR(100),
            file_path VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Task history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_history (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
            user_id UUID REFERENCES users(id) ON DELETE SET NULL,
            action VARCHAR(50) NOT NULL,
            old_values JSONB,
            new_values JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    print("✅ All tables created successfully")

def create_indexes(cursor):
    """Create performance indexes."""
    print("⚡ Creating performance indexes...")
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);",
        "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);",
        "CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active);",
        "CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);",
        "CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);",
        "CREATE INDEX IF NOT EXISTS idx_tasks_assigned_to ON tasks(assigned_to);",
        "CREATE INDEX IF NOT EXISTS idx_tasks_created_by ON tasks(created_by);",
        "CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);",
        "CREATE INDEX IF NOT EXISTS idx_comments_task_id ON comments(task_id);",
        "CREATE INDEX IF NOT EXISTS idx_comments_user_id ON comments(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_attachments_task_id ON attachments(task_id);",
        "CREATE INDEX IF NOT EXISTS idx_task_history_task_id ON task_history(task_id);",
    ]
    
    for index_sql in indexes:
        cursor.execute(index_sql)
    
    print(f"✅ Created {len(indexes)} performance indexes")

def create_triggers(cursor):
    """Create timestamp update triggers."""
    print("🔄 Creating update triggers...")
    
    # Create trigger function
    cursor.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)
    
    # Create triggers for tables with updated_at
    tables_with_updated_at = ['users', 'categories', 'tasks', 'comments']
    for table in tables_with_updated_at:
        cursor.execute(f"""
            CREATE TRIGGER trigger_update_{table}_updated_at
            BEFORE UPDATE ON {table}
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        """)
    
    print("✅ Update triggers created")

def insert_sample_data(cursor):
    """Insert sample data."""
    print("📊 Inserting sample data...")
    
    # Sample users
    users_data = [
        ('admin', 'admin@demo.com', 'hashed_password_1', 'Admin', 'User', True, True),
        ('john_doe', 'john@demo.com', 'hashed_password_2', 'John', 'Doe', True, False),
        ('jane_smith', 'jane@demo.com', 'hashed_password_3', 'Jane', 'Smith', True, False),
        ('bob_wilson', 'bob@demo.com', 'hashed_password_4', 'Bob', 'Wilson', True, False),
    ]
    
    user_ids = []
    for username, email, password, first_name, last_name, is_active, is_admin in users_data:
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, first_name, last_name, is_active, is_admin)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (username, email, password, first_name, last_name, is_active, is_admin))
        user_ids.append(cursor.fetchone()[0])
    
    admin_id, john_id, jane_id, bob_id = user_ids
    
    # Sample categories
    categories_data = [
        ('Development', 'Software development tasks', '#e74c3c', admin_id),
        ('Design', 'UI/UX design work', '#9b59b6', admin_id),
        ('Testing', 'Quality assurance and testing', '#f39c12', admin_id),
        ('Documentation', 'Technical documentation', '#2ecc71', admin_id),
        ('Bug Fixes', 'Bug fixes and maintenance', '#e67e22', admin_id),
        ('Research', 'Research and analysis', '#3498db', admin_id),
    ]
    
    category_ids = []
    for name, description, color, created_by in categories_data:
        cursor.execute("""
            INSERT INTO categories (name, description, color, created_by)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (name, description, color, created_by))
        category_ids.append(cursor.fetchone()[0])
    
    dev_cat, design_cat, test_cat, doc_cat, bug_cat, research_cat = category_ids
    
    # Sample tasks
    now = datetime.now()
    tasks_data = [
        ('Implement user authentication', 'Add JWT-based authentication system', 'in_progress', 'high', 
         now + timedelta(days=7), None, 16.0, None, john_id, admin_id),
        ('Design landing page', 'Create wireframes and mockups for homepage', 'pending', 'medium',
         now + timedelta(days=5), None, 8.0, None, jane_id, admin_id),
        ('Fix navbar bug', 'Navbar not responsive on mobile devices', 'pending', 'urgent',
         now + timedelta(days=2), None, 4.0, None, bob_id, john_id),
        ('Write API documentation', 'Document all REST API endpoints', 'completed', 'low',
         now - timedelta(days=1), now - timedelta(hours=2), 12.0, 10.5, john_id, admin_id),
        ('Setup CI/CD pipeline', 'Configure automated testing and deployment', 'in_progress', 'high',
         now + timedelta(days=10), None, 20.0, None, bob_id, admin_id),
    ]
    
    task_ids = []
    for title, desc, status, priority, due_date, completed_at, est_hours, actual_hours, assigned_to, created_by in tasks_data:
        cursor.execute("""
            INSERT INTO tasks (title, description, status, priority, due_date, completed_at, 
                             estimated_hours, actual_hours, assigned_to, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (title, desc, status, priority, due_date, completed_at, est_hours, actual_hours, assigned_to, created_by))
        task_ids.append(cursor.fetchone()[0])
    
    auth_task, landing_task, navbar_task, doc_task, cicd_task = task_ids
    
    # Task-Category relationships
    task_category_relations = [
        (auth_task, dev_cat),
        (landing_task, design_cat),
        (navbar_task, bug_cat),
        (navbar_task, dev_cat),  # Multiple categories for one task
        (doc_task, doc_cat),
        (cicd_task, dev_cat),
    ]
    
    for task_id, category_id in task_category_relations:
        cursor.execute("""
            INSERT INTO task_categories (task_id, category_id)
            VALUES (%s, %s);
        """, (task_id, category_id))
    
    # Sample comments
    comments_data = [
        (auth_task, john_id, 'Started working on JWT implementation. Looking into popular libraries.', False),
        (auth_task, admin_id, 'Great! Make sure to implement proper refresh token handling.', False),
        (landing_task, jane_id, 'Initial wireframes are ready for review.', False),
        (navbar_task, bob_id, 'Reproduced the issue. CSS media queries need fixing.', False),
        (doc_task, john_id, 'Documentation complete and published to internal wiki.', False),
        (cicd_task, bob_id, 'GitHub Actions workflow configured. Testing deployment pipeline.', False),
    ]
    
    for task_id, user_id, content, is_internal in comments_data:
        cursor.execute("""
            INSERT INTO comments (task_id, user_id, content, is_internal)
            VALUES (%s, %s, %s, %s);
        """, (task_id, user_id, content, is_internal))
    
    # Sample attachments
    attachments_data = [
        (landing_task, jane_id, 'landing_page_wireframe.png', 245760, 'image/png', '/uploads/wireframes/landing_page_wireframe.png'),
        (doc_task, john_id, 'api_documentation.pdf', 1024000, 'application/pdf', '/uploads/docs/api_documentation.pdf'),
    ]
    
    for task_id, uploaded_by, filename, file_size, mime_type, file_path in attachments_data:
        cursor.execute("""
            INSERT INTO attachments (task_id, uploaded_by, filename, file_size, mime_type, file_path)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (task_id, uploaded_by, filename, file_size, mime_type, file_path))
    
    # Sample task history
    history_data = [
        (auth_task, admin_id, 'created', None, {'status': 'pending', 'assigned_to': str(john_id)}),
        (auth_task, john_id, 'status_changed', {'status': 'pending'}, {'status': 'in_progress'}),
        (doc_task, john_id, 'status_changed', {'status': 'in_progress'}, {'status': 'completed'}),
    ]
    
    for task_id, user_id, action, old_values, new_values in history_data:
        cursor.execute("""
            INSERT INTO task_history (task_id, user_id, action, old_values, new_values)
            VALUES (%s, %s, %s, %s, %s);
        """, (task_id, user_id, action, 
              psycopg2.extras.Json(old_values) if old_values else None,
              psycopg2.extras.Json(new_values)))
    
    print("✅ Sample data inserted successfully")

def main():
    """Setup the complete database schema and sample data."""
    print("🚀 Database Setup Script")
    print("========================")
    
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        # Create extensions
        create_extensions(cursor)
        
        # Create tables
        create_tables(cursor)
        
        # Create indexes
        create_indexes(cursor)
        
        # Create triggers
        create_triggers(cursor)
        
        # Insert sample data
        insert_sample_data(cursor)
        
        # Commit all changes
        conn.commit()
        
        print("\n🎉 DATABASE SETUP COMPLETE!")
        print("✅ Schema created with 7 tables")
        print("✅ Foreign key relationships established")
        print("✅ Performance indexes created")
        print("✅ Update triggers configured")
        print("✅ Sample data populated")
        print("\n📊 Ready for Hasura auto-introspection!")
        print("🌐 Access Hasura Console: http://localhost:8080/console")
        
    except Exception as exc:
        print(f"❌ Setup failed: {exc}")
        conn.rollback()
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main() 