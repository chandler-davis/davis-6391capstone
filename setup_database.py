#!/usr/bin/env python3
import mysql.connector
import os
from pathlib import Path

# Read database configuration from .env file
env_path = Path(__file__).parent / '.env'
db_config = {}

with open(env_path, 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            db_config[key] = value

# Database connection parameters
config = {
    'host': db_config.get('DB_HOST'),
    'user': db_config.get('DB_USER'),
    'password': db_config.get('DB_PASSWORD'),
    'database': db_config.get('DB_NAME'),
    'port': int(db_config.get('DB_PORT', 3306))
}

def execute_sql_file(cursor, filename):
    """Execute SQL commands from a file"""
    print(f"Executing {filename}...")
    
    with open(filename, 'r') as f:
        sql_content = f.read()
    
    # Split by semicolons but handle multi-line statements
    statements = []
    current_statement = ""
    
    for line in sql_content.split('\n'):
        line = line.strip()
        if line and not line.startswith('--'):
            current_statement += line + " "
            if line.endswith(';'):
                statements.append(current_statement.strip())
                current_statement = ""
    
    # Execute each statement
    for statement in statements:
        if statement.strip():
            try:
                cursor.execute(statement)
                print(f"✓ Executed statement")
            except mysql.connector.Error as e:
                print(f"✗ Error executing statement: {e}")
                print(f"Statement: {statement[:100]}...")

def main():
    try:
        # Connect to database
        print("Connecting to database...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        print("✓ Connected successfully!")
        
        # Execute schema.sql
        schema_path = Path(__file__).parent / 'database' / 'schema.sql'
        execute_sql_file(cursor, schema_path)
        
        # Commit schema changes
        connection.commit()
        print("✓ Schema created successfully!")
        
        # Execute seed_data.sql
        seed_path = Path(__file__).parent / 'database' / 'seed_data.sql'
        execute_sql_file(cursor, seed_path)
        
        # Commit seed data changes
        connection.commit()
        print("✓ Seed data inserted successfully!")
        
        # Verify tables were created
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"\n✓ Created {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
            
    except mysql.connector.Error as e:
        print(f"✗ Database error: {e}")
        return False
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("\n✓ Database connection closed")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Database setup completed successfully!")
    else:
        print("\n❌ Database setup failed!")