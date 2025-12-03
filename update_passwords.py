#!/usr/bin/env python3
"""
Script to update existing user passwords with proper hashing
Run this after implementing authentication to hash the existing passwords
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

def update_passwords():
    try:
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        
        # Define user passwords (for demo purposes)
        user_passwords = {
            'admin': 'admin123',
            'scout_john': 'scout123',
            'scout_jane': 'scout123',
            'user_mike': 'user123',
            'user_sarah': 'user123'
        }
        
        print("Updating user passwords with proper hashing...")
        
        for username, plain_password in user_passwords.items():
            hashed_password = generate_password_hash(plain_password)
            
            cursor.execute('''UPDATE users SET password = %s WHERE username = %s''',
                          (hashed_password, username))
            
            print(f"✓ Updated password for user: {username}")
        
        connection.commit()
        print(f"\n✅ Successfully updated passwords for {len(user_passwords)} users!")
        print("\nDemo login credentials:")
        print("- admin / admin123 (Administrator)")
        print("- scout_john / scout123 (Scout)")
        print("- scout_jane / scout123 (Scout)")
        print("- user_mike / user123 (User)")
        print("- user_sarah / user123 (User)")
        
    except Exception as e:
        print(f"❌ Error updating passwords: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

if __name__ == "__main__":
    update_passwords()