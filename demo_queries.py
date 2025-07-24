"""
Demonstration queries for the demo database schema.
Shows various relationships and advanced SQL features.
"""
import psycopg2
import sys
from datetime import datetime

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

def run_query(cursor, title, query, headers=None):
    """Run a query and display formatted results."""
    print(f"\n🔍 {title}")
    print("=" * len(title))
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    if headers:
        print(f"{'  '.join(f'{h:<15}' for h in headers)}")
        print("-" * (16 * len(headers)))
    
    for row in results:
        formatted_row = []
        for item in row:
            if isinstance(item, datetime):
                formatted_row.append(item.strftime('%Y-%m-%d %H:%M'))
            elif item is None:
                formatted_row.append('NULL')
            else:
                formatted_row.append(str(item))
        
        if headers:
            print(f"{'  '.join(f'{item:<15}' for item in formatted_row)}")
        else:
            print(f"  {' | '.join(formatted_row)}")
    
    print(f"📊 Found {len(results)} record(s)")

def main():
    """Run demonstration queries."""
    print("🎯 Database Schema Demonstration")
    print("================================")
    
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        # 1. Show all users with their role status
        run_query(
            cursor,
            "Users Overview",
            """
            SELECT 
                username,
                CONCAT(first_name, ' ', last_name) as full_name,
                email,
                CASE WHEN is_admin THEN 'Admin' ELSE 'User' END as role,
                CASE WHEN is_active THEN 'Active' ELSE 'Inactive' END as status
            FROM users 
            ORDER BY is_admin DESC, username;
            """,
            ['Username', 'Full Name', 'Email', 'Role', 'Status']
        )
        
        # 2. Task assignment overview with workload
        run_query(
            cursor,
            "Task Assignment & Workload",
            """
            SELECT 
                u.username,
                COUNT(t.id) as total_tasks,
                COUNT(CASE WHEN t.status = 'pending' THEN 1 END) as pending,
                COUNT(CASE WHEN t.status = 'in_progress' THEN 1 END) as in_progress,
                COUNT(CASE WHEN t.status = 'completed' THEN 1 END) as completed
            FROM users u
            LEFT JOIN tasks t ON u.id = t.assigned_to
            GROUP BY u.id, u.username
            ORDER BY total_tasks DESC;
            """,
            ['User', 'Total', 'Pending', 'In Progress', 'Completed']
        )
        
        # 3. Tasks with categories and priorities
        run_query(
            cursor,
            "Tasks by Category & Priority",
            """
            SELECT 
                t.title,
                t.priority,
                t.status,
                STRING_AGG(c.name, ', ') as categories,
                u.username as assigned_to
            FROM tasks t
            LEFT JOIN task_categories tc ON t.id = tc.task_id
            LEFT JOIN categories c ON tc.category_id = c.id
            LEFT JOIN users u ON t.assigned_to = u.id
            GROUP BY t.id, t.title, t.priority, t.status, u.username
            ORDER BY 
                CASE t.priority 
                    WHEN 'urgent' THEN 1 
                    WHEN 'high' THEN 2 
                    WHEN 'medium' THEN 3 
                    WHEN 'low' THEN 4 
                END;
            """,
            ['Title', 'Priority', 'Status', 'Categories', 'Assigned To']
        )
        
        # 4. Comment activity by task
        run_query(
            cursor,
            "Comment Activity & Collaboration",
            """
            SELECT 
                t.title,
                COUNT(co.id) as comment_count,
                COUNT(DISTINCT co.user_id) as unique_commenters,
                MAX(co.created_at) as last_comment
            FROM tasks t
            LEFT JOIN comments co ON t.id = co.task_id
            GROUP BY t.id, t.title
            HAVING COUNT(co.id) > 0
            ORDER BY comment_count DESC;
            """,
            ['Task', 'Comments', 'Commenters', 'Last Comment']
        )
        
        # 5. Category usage statistics
        run_query(
            cursor,
            "Category Usage Statistics",
            """
            SELECT 
                c.name,
                c.color,
                COUNT(tc.task_id) as task_count,
                ROUND(COUNT(tc.task_id) * 100.0 / 
                      (SELECT COUNT(*) FROM task_categories), 2) as percentage
            FROM categories c
            LEFT JOIN task_categories tc ON c.id = tc.category_id
            GROUP BY c.id, c.name, c.color
            ORDER BY task_count DESC;
            """,
            ['Category', 'Color', 'Tasks', 'Percentage']
        )
        
        # 6. Advanced: Task timeline with durations
        run_query(
            cursor,
            "Task Timeline & Duration Analysis",
            """
            SELECT 
                t.title,
                t.created_at::date as created_date,
                t.due_date::date as due_date,
                CASE 
                    WHEN t.due_date IS NOT NULL 
                    THEN EXTRACT(days FROM t.due_date - t.created_at)
                    ELSE NULL 
                END as days_allocated,
                t.estimated_hours,
                creator.username as created_by,
                assignee.username as assigned_to
            FROM tasks t
            LEFT JOIN users creator ON t.created_by = creator.id
            LEFT JOIN users assignee ON t.assigned_to = assignee.id
            ORDER BY t.created_at DESC;
            """,
            ['Title', 'Created', 'Due Date', 'Days', 'Est Hours', 'Creator', 'Assignee']
        )
        
        # 7. Database statistics
        run_query(
            cursor,
            "Database Statistics",
            """
            SELECT 
                'Users' as table_name, COUNT(*) as record_count FROM users
            UNION ALL
            SELECT 'Tasks', COUNT(*) FROM tasks
            UNION ALL  
            SELECT 'Categories', COUNT(*) FROM categories
            UNION ALL
            SELECT 'Comments', COUNT(*) FROM comments
            UNION ALL
            SELECT 'Task-Categories', COUNT(*) FROM task_categories
            ORDER BY record_count DESC;
            """,
            ['Table', 'Records']
        )
        
        print("\n✅ Database demonstration complete!")
        print("\n🎯 Schema Features Demonstrated:")
        print("  ✓ UUID primary keys with auto-generation")
        print("  ✓ Foreign key relationships with cascading deletes")
        print("  ✓ Many-to-many relationships (tasks ↔ categories)")
        print("  ✓ One-to-many relationships (users → tasks → comments)")
        print("  ✓ Check constraints for data validation")
        print("  ✓ Indexes for query performance")
        print("  ✓ Automatic timestamp updates with triggers")
        print("  ✓ Complex queries with JOINs and aggregations")
        
    except Exception as e:
        print(f"❌ Query execution failed: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main() 