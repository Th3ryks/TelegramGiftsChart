import sqlite3
from datetime import datetime
from typing import Optional

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    # Create table for rate limiting
    c.execute('''
        CREATE TABLE IF NOT EXISTS rate_limits (
            user_id INTEGER PRIMARY KEY,
            last_success_time TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def update_last_success(user_id: int) -> None:
    """Update the last successful request time for a user"""
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    c.execute('''
        INSERT OR REPLACE INTO rate_limits (user_id, last_success_time)
        VALUES (?, ?)
    ''', (user_id, datetime.now().timestamp()))
    
    conn.commit()
    conn.close()

def get_last_success_time(user_id: int) -> Optional[float]:
    """Get the last successful request time for a user"""
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    c.execute('SELECT last_success_time FROM rate_limits WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    
    conn.close()
    return result[0] if result else None 