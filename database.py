# data_analytics_profiler_db.py
import sqlite3
import os
from pathlib import Path
from datetime import datetime

def init_db():
    """Initialize database and create necessary tables"""
    # Create data directory if it doesn't exist
    data_dir = Path('./data')
    data_dir.mkdir(exist_ok=True)
    
    # Connect to database (this will create it if it doesn't exist)
    conn = sqlite3.connect('./data/assessment.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            profession TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            analytical_score REAL,
            communication_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_user_id_by_email(email):
    """Get existing user ID or create new user"""
    conn = get_db()
    c = conn.cursor()
    try:
        # Try to get existing user
        c.execute('SELECT id FROM users WHERE email = ?', (email,))
        result = c.fetchone()
        if result:
            return result[0]
        return None
    finally:
        conn.close()

def save_user(email, profession):
    """Save user and return user_id (either existing or new)"""
    # First check if user exists
    existing_id = get_user_id_by_email(email)
    if existing_id:
        return existing_id
        
    # If not, create new user
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (email, profession) VALUES (?, ?)', 
                 (email, profession))
        conn.commit()
        return c.lastrowid
    except Exception as e:
        print(f"Error saving user: {e}")
        return None
    finally:
        conn.close()

def save_results(user_id, analytical_score, communication_score):
    """Save assessment results"""
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO results 
            (user_id, analytical_score, communication_score, created_at)
            VALUES (?, ?, ?, ?)
        ''', (user_id, analytical_score, communication_score, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
    except Exception as e:
        print(f"Error saving results: {e}")
    finally:
        conn.close()

def get_db():
    """Get database connection"""
    return sqlite3.connect('./data/assessment.db')

def get_all_results():
    """Get all results with user information"""
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute('''
            SELECT 
                users.email,
                users.profession,
                results.analytical_score,
                results.communication_score,
                results.created_at
            FROM results
            JOIN users ON results.user_id = users.id
            ORDER BY results.created_at DESC
        ''')
        return c.fetchall()
    finally:
        conn.close()