"""
Enhanced connectivity and schema validation check for the demo Postgres.
Validates both connection and database schema integrity.
Run: python db_health_enhanced.py
"""
import psycopg2
import sys

def check_connection():
    """Test basic database connectivity."""
    print("🔍 Testing database connection...")
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="demo",
            user="demo",
            password="demo",
            connect_timeout=3,
        )
        print("✅ Database connection successful")
        return conn
    except Exception as exc:
        print(f"❌ Database connection failed: {exc}")
        return None

def check_schema(conn):
    """Validate that required tables and relationships exist."""
    print("\n🔍 Validating database schema...")
    
    cursor = conn.cursor()
    
    # Expected tables
    expected_tables = [
        'users', 'tasks', 'categories', 'comments', 
        'attachments', 'task_categories', 'task_history'
    ]
    
    try:
        # Check if all tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
        """)
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        missing_tables = set(expected_tables) - set(existing_tables)
        if missing_tables:
            print(f"❌ Missing tables: {', '.join(missing_tables)}")
            return False
        
        print(f"✅ All {len(expected_tables)} tables present")
        
        # Check foreign key constraints
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.table_constraints 
            WHERE constraint_type = 'FOREIGN KEY' 
            AND table_schema = 'public'
        """)
        fk_count = cursor.fetchone()[0]
        
        if fk_count < 5:  # We expect at least 5 foreign keys
            print(f"❌ Insufficient foreign key constraints: {fk_count}")
            return False
        
        print(f"✅ Foreign key constraints: {fk_count}")
        
        # Check indexes
        cursor.execute("""
            SELECT COUNT(*) 
            FROM pg_indexes 
            WHERE schemaname = 'public'
            AND indexname NOT LIKE '%_pkey'
        """)
        index_count = cursor.fetchone()[0]
        
        if index_count < 8:  # We expect at least 8 custom indexes
            print(f"❌ Insufficient indexes: {index_count}")
            return False
        
        print(f"✅ Performance indexes: {index_count}")
        
        # Check if UUID extension is loaded
        cursor.execute("""
            SELECT COUNT(*) 
            FROM pg_extension 
            WHERE extname = 'uuid-ossp'
        """)
        uuid_ext = cursor.fetchone()[0]
        
        if uuid_ext == 0:
            print("❌ UUID extension not loaded")
            return False
        
        print("✅ UUID extension loaded")
        
        return True
        
    except Exception as exc:
        print(f"❌ Schema validation failed: {exc}")
        return False
    finally:
        cursor.close()

def check_sample_data(conn):
    """Verify that sample data exists and relationships work."""
    print("\n🔍 Validating sample data and relationships...")
    
    cursor = conn.cursor()
    
    try:
        # Check users
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        if user_count < 4:
            print(f"❌ Insufficient users: {user_count}")
            return False
        
        print(f"✅ Users: {user_count}")
        
        # Check tasks with assignments
        cursor.execute("""
            SELECT COUNT(*) 
            FROM tasks t 
            JOIN users u ON t.assigned_to = u.id
        """)
        assigned_tasks = cursor.fetchone()[0]
        
        if assigned_tasks < 3:
            print(f"❌ Insufficient assigned tasks: {assigned_tasks}")
            return False
        
        print(f"✅ Assigned tasks: {assigned_tasks}")
        
        # Check task-category relationships
        cursor.execute("SELECT COUNT(*) FROM task_categories")
        task_cat_relations = cursor.fetchone()[0]
        
        if task_cat_relations < 3:
            print(f"❌ Insufficient task-category relations: {task_cat_relations}")
            return False
        
        print(f"✅ Task-category relations: {task_cat_relations}")
        
        # Check comments
        cursor.execute("""
            SELECT COUNT(*) 
            FROM comments c
            JOIN tasks t ON c.task_id = t.id
            JOIN users u ON c.user_id = u.id
        """)
        comment_count = cursor.fetchone()[0]
        
        if comment_count < 3:
            print(f"❌ Insufficient comments: {comment_count}")
            return False
        
        print(f"✅ Comments with valid relationships: {comment_count}")
        
        return True
        
    except Exception as exc:
        print(f"❌ Sample data validation failed: {exc}")
        return False
    finally:
        cursor.close()

def check_performance(conn):
    """Test query performance with indexes."""
    print("\n🔍 Testing query performance...")
    
    cursor = conn.cursor()
    
    try:
        # Test indexed queries
        import time
        
        # Query that should use indexes
        start_time = time.time()
        cursor.execute("""
            SELECT t.title, u.username, c.name
            FROM tasks t
            JOIN users u ON t.assigned_to = u.id
            JOIN task_categories tc ON t.id = tc.task_id
            JOIN categories c ON tc.category_id = c.id
            WHERE t.status = 'pending' 
            AND t.priority = 'high'
        """)
        results = cursor.fetchall()
        end_time = time.time()
        
        query_time = (end_time - start_time) * 1000  # Convert to ms
        
        if query_time > 100:  # Should be very fast for small dataset
            print(f"⚠️  Query performance concern: {query_time:.2f}ms")
        else:
            print(f"✅ Query performance: {query_time:.2f}ms")
        
        return True
        
    except Exception as exc:
        print(f"❌ Performance test failed: {exc}")
        return False
    finally:
        cursor.close()

def main():
    """Run comprehensive database health check."""
    print("🎯 Enhanced Database Health Check")
    print("=================================")
    
    # Test connection
    conn = check_connection()
    if not conn:
        sys.exit(1)
    
    try:
        # Validate schema
        schema_ok = check_schema(conn)
        if not schema_ok:
            print("\n❌ Schema validation failed")
            sys.exit(1)
        
        # Validate sample data
        data_ok = check_sample_data(conn)
        if not data_ok:
            print("\n❌ Sample data validation failed")
            sys.exit(1)
        
        # Test performance
        perf_ok = check_performance(conn)
        if not perf_ok:
            print("\n❌ Performance test failed")
            sys.exit(1)
        
        print("\n🎉 ALL CHECKS PASSED!")
        print("✅ Database is healthy and ready for use")
        print("\n📊 Summary:")
        print("  • Connection: Working")
        print("  • Schema: Complete with 7 tables")
        print("  • Foreign Keys: Properly configured")
        print("  • Indexes: Optimized for performance")
        print("  • Sample Data: Present and valid")
        print("  • Relationships: All working correctly")
        
    except Exception as exc:
        print(f"\n❌ Health check failed: {exc}")
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    main() 