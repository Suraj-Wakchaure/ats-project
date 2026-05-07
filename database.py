import sqlite3

DATABASE = 'ats.db'

def get_database():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_database()
    
    conn.execute('''
                 CREATE TABLE IF NOT EXISTS jobs(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 skills_required TEXT NOT NULL    
                 )
                 ''')
    conn.execute('''
                 CREATE TABLE IF NOT EXISTS applications(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 candidate_name TEXT NOT NULL,
                 email TEXT NOT NULL,
                 skills TEXT NOT NULL,
                 score REAL DEFAULT 0,
                 applied_at TEXT,
                 summary TEXT,
                 job_id INTEGER,
                 FOREIGN KEY (job_id) REFERENCES jobs(id)
                 )
                 ''')
    conn.execute('''
                 CREATE TABLE IF NOT EXISTS notifications(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 message TEXT NOT NULL,
                 is_read INTEGER DEFAULT 0,
                 timestamp TEXT,
                 job_id INTEGER,
                 FOREIGN KEY (job_id) REFERENCES jobs(id)  
                 )
                 ''')
    
    conn.commit()
    conn.close()