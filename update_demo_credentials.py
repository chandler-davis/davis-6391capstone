#!/usr/bin/env python3
"""
Script to update demo credentials to match the login page
"""

import pymysql
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection
config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', 3306))
}

def update_demo_credentials():
    try:
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        
        # Update admin user to have username "admin123" and password "scout123"
        hashed_password = generate_password_hash('scout123')
        
        # First, update the existing admin user
        cursor.execute('''UPDATE users SET username = %s, password = %s WHERE username = %s''',
                      ('admin123', hashed_password, 'admin'))
        
        print("✓ Updated demo credentials:")
        print("  Username: admin123")
        print("  Password: scout123")
        
        connection.commit()
        print("\n✅ Demo credentials updated successfully!")
        
    except Exception as e:
        print(f"❌ Error updating demo credentials: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

if __name__ == "__main__":
    update_demo_credentials()