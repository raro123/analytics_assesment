# database.py
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def init_db():
    """
    No need to initialize tables as they're managed in Supabase UI
    or through migrations
    """
    pass

def save_user(email: str, profession: str):
    """Save a new user or get existing user ID"""
    try:
        # Check if user exists
        response = supabase.table('users').select('id').eq('email', email).execute()
        
        if response.data:
            return response.data[0]['id']
            
        # Create new user
        response = supabase.table('users').insert({
            'email': email,
            'profession': profession,
            'created_at': datetime.now().isoformat()
        }).execute()
        
        return response.data[0]['id']
    except Exception as e:
        print(f"Error saving user: {e}")
        return None

def save_results(user_id: int, analytical_score: float, communication_score: float):
    """Save assessment results"""
    try:
        response = supabase.table('results').insert({
            'user_id': user_id,
            'analytical_score': analytical_score,
            'communication_score': communication_score,
            'created_at': datetime.now().isoformat()
        }).execute()
        
        return response.data[0]['id']
    except Exception as e:
        print(f"Error saving results: {e}")
        return None

def get_all_results():
    """Get all results with user information"""
    try:
        response = supabase.table('results').select(
            'users(email, profession), analytical_score, communication_score, created_at'
        ).execute()
        
        # Format data to match existing structure
        return [(
            r['users']['email'],
            r['users']['profession'],
            r['analytical_score'],
            r['communication_score'],
            r['created_at']
        ) for r in response.data]
    except Exception as e:
        print(f"Error fetching results: {e}")
        return []