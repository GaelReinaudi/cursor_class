"""
Auto-track all database tables in Hasura GraphQL Engine.
This script makes all tables available in the GraphQL API with relationships.
Run: python track_tables.py
"""
import requests
import json

HASURA_URL = "http://localhost:8080"
HEADERS = {
    "Content-Type": "application/json"
}

def add_postgres_source():
    """Add Postgres database as a data source in Hasura."""
    payload = {
        "type": "pg_add_source",
        "args": {
            "name": "default",
            "configuration": {
                "connection_info": {
                    "database_url": "postgres://demo:demo@postgres:5432/demo"
                }
            }
        }
    }
    
    response = requests.post(f"{HASURA_URL}/v1/metadata", 
                           headers=HEADERS, 
                           data=json.dumps(payload))
    
    if response.status_code == 200:
        print("✅ Successfully added Postgres data source")
        return True
    else:
        # Check if source already exists
        if "already exists" in response.text:
            print("✅ Postgres data source already exists")
            return True
        else:
            print(f"❌ Failed to add Postgres data source")
            print(f"   Error: {response.text}")
            return False

def track_table(table_name):
    """Track a single table in Hasura."""
    payload = {
        "type": "pg_track_table",
        "args": {
            "source": "default",
            "table": {"name": table_name, "schema": "public"}
        }
    }
    
    response = requests.post(f"{HASURA_URL}/v1/metadata", 
                           headers=HEADERS, 
                           data=json.dumps(payload))
    
    if response.status_code == 200:
        print(f"✅ Successfully tracked table: {table_name}")
        return True
    else:
        print(f"❌ Failed to track table: {table_name}")
        print(f"   Error: {response.text}")
        return False

def create_foreign_key_relationship(table, column, ref_table, ref_column, rel_name):
    """Create a foreign key relationship in Hasura."""
    payload = {
        "type": "pg_create_object_relationship", 
        "args": {
            "source": "default",
            "table": {"name": table, "schema": "public"},
            "name": rel_name,
            "using": {
                "foreign_key_constraint_on": column
            }
        }
    }
    
    response = requests.post(f"{HASURA_URL}/v1/metadata", 
                           headers=HEADERS, 
                           data=json.dumps(payload))
    
    if response.status_code == 200:
        print(f"✅ Created relationship: {table}.{rel_name}")
        return True
    else:
        print(f"⚠️  Relationship {table}.{rel_name} may already exist or failed")
        return False

def create_array_relationship(table, ref_table, ref_column, rel_name):
    """Create an array relationship (one-to-many) in Hasura."""
    payload = {
        "type": "pg_create_array_relationship",
        "args": {
            "source": "default", 
            "table": {"name": table, "schema": "public"},
            "name": rel_name,
            "using": {
                "foreign_key_constraint_on": {
                    "table": {"name": ref_table, "schema": "public"},
                    "column": ref_column
                }
            }
        }
    }
    
    response = requests.post(f"{HASURA_URL}/v1/metadata", 
                           headers=HEADERS, 
                           data=json.dumps(payload))
    
    if response.status_code == 200:
        print(f"✅ Created array relationship: {table}.{rel_name}")
        return True
    else:
        print(f"⚠️  Array relationship {table}.{rel_name} may already exist or failed")
        return False

def main():
    """Track all tables and create relationships."""
    print("🚀 Hasura Table Tracking & Relationship Setup")
    print("===========================================")
    
    # First, add the Postgres data source
    print("\n🔌 Adding Postgres data source...")
    if not add_postgres_source():
        print("❌ Failed to add data source. Exiting.")
        return
    
    # List of all tables to track
    tables = [
        "users",
        "categories", 
        "tasks",
        "task_categories",
        "comments",
        "attachments", 
        "task_history"
    ]
    
    print("\n🏷️ Tracking tables...")
    success_count = 0
    for table in tables:
        if track_table(table):
            success_count += 1
    
    print(f"\n📊 Tracked {success_count}/{len(tables)} tables")
    
    if success_count < len(tables):
        print("⚠️  Some tables failed to track. Check Hasura logs.")
        return
    
    print("\n🔗 Creating relationships...")
    
    # Object relationships (many-to-one)
    relationships = [
        # Tasks relationships
        ("tasks", "assigned_to", "users", "id", "assigned_user"),
        ("tasks", "created_by", "users", "id", "creator"), 
        
        # Categories relationships
        ("categories", "created_by", "users", "id", "creator"),
        
        # Comments relationships  
        ("comments", "task_id", "tasks", "id", "task"),
        ("comments", "user_id", "users", "id", "user"),
        
        # Attachments relationships
        ("attachments", "task_id", "tasks", "id", "task"),
        ("attachments", "uploaded_by", "users", "id", "uploader"),
        
        # Task history relationships
        ("task_history", "task_id", "tasks", "id", "task"),
        ("task_history", "user_id", "users", "id", "user"),
        
        # Task categories relationships
        ("task_categories", "task_id", "tasks", "id", "task"),
        ("task_categories", "category_id", "categories", "id", "category"),
    ]
    
    obj_rel_count = 0
    for table, column, ref_table, ref_column, rel_name in relationships:
        if create_foreign_key_relationship(table, column, ref_table, ref_column, rel_name):
            obj_rel_count += 1
    
    # Array relationships (one-to-many)
    array_relationships = [
        # Users array relationships
        ("users", "tasks", "assigned_to", "assigned_tasks"),
        ("users", "tasks", "created_by", "created_tasks"),
        ("users", "categories", "created_by", "created_categories"),
        ("users", "comments", "user_id", "comments"),
        ("users", "attachments", "uploaded_by", "uploaded_attachments"),
        ("users", "task_history", "user_id", "task_actions"),
        
        # Tasks array relationships
        ("tasks", "comments", "task_id", "comments"),
        ("tasks", "attachments", "task_id", "attachments"),
        ("tasks", "task_history", "task_id", "history"),
        ("tasks", "task_categories", "task_id", "task_categories"),
        
        # Categories array relationships
        ("categories", "task_categories", "category_id", "task_categories"),
    ]
    
    array_rel_count = 0
    for table, ref_table, ref_column, rel_name in array_relationships:
        if create_array_relationship(table, ref_table, ref_column, rel_name):
            array_rel_count += 1
    
    print(f"\n📊 Relationship Summary:")
    print(f"   Object relationships: {obj_rel_count}/{len(relationships)}")
    print(f"   Array relationships: {array_rel_count}/{len(array_relationships)}")
    
    print("\n🎉 SETUP COMPLETE!")
    print("✅ All tables tracked and relationships configured")
    print("🌐 Access Hasura Console: http://localhost:8080/console")
    print("🔍 Try GraphQL queries:")
    print("   • users { id username assigned_tasks { title status } }")
    print("   • tasks { title assigned_user { username } comments { content user { username } } }")
    print("   • categories { name task_categories { task { title } } }")
    
    # Test a simple query
    print("\n🧪 Testing GraphQL query...")
    test_query = {
        "query": "{ users { id username email first_name last_name is_admin } }"
    }
    
    response = requests.post(f"{HASURA_URL}/v1/graphql", 
                           headers=HEADERS,
                           data=json.dumps(test_query))
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            user_count = len(data['data']['users'])
            print(f"✅ GraphQL test successful! Found {user_count} users")
        else:
            print(f"❌ GraphQL test failed: {data}")
    else:
        print(f"❌ GraphQL test failed with status: {response.status_code}")

if __name__ == "__main__":
    main() 