# migrate_to_supabase.py
import sqlite3
from database import supabase
from pathlib import Path

def migrate_data():
    """Migrate data from SQLite to Supabase"""
    # Connect to SQLite database
    sqlite_db = Path(__file__).parent / 'data' / 'assessment.db'
    
    if not sqlite_db.exists():
        print("No SQLite database found to migrate")
        return
    
    conn = sqlite3.connect(sqlite_db)
    c = conn.cursor()
    
    try:
        # Migrate users
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        
        for user in users:
            user_id, email, profession, created_at = user
            
            # Insert into Supabase
            supabase.table('users').insert({
                'id': user_id,
                'email': email,
                'profession': profession,
                'created_at': created_at
            }).execute()
        
        print(f"Migrated {len(users)} users")
        
        # Migrate results
        c.execute("SELECT * FROM results")
        results = c.fetchall()
        
        for result in results:
            result_id, user_id, analytical_score, communication_score, created_at = result
            
            # Insert into Supabase
            supabase.table('results').insert({
                'id': result_id,
                'user_id': user_id,
                'analytical_score': analytical_score,
                'communication_score': communication_score,
                'created_at': created_at
            }).execute()
        
        print(f"Migrated {len(results)} results")
        
    except Exception as e:
        print(f"Error during migration: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_data()