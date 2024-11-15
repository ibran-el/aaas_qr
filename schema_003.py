import sqlite3

db = 'aaas_qr_db.db'
def create_database(db_name):
    # """Create a SQLite database and return the connection object."""
    conn = sqlite3.connect(db_name)
    return conn

def create_students_table(conn):
    # """Create the Students table in the database."""
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                admission_no TEXT UNIQUE NOT NULL
            );
        ''')
    print("Students table created.")


def create_attendance_table(conn):
    """Create the Attendance table in the database."""
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Attendance (
                attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                attendance_date DATE NOT NULL,
                rollcall_for TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES Students(student_id)
            );
        ''')
    print("Attendance table created.")

def init_db():
    # Create a new database (or connect to it)
    conn = create_database(db)
    
    # Create tables
    create_students_table(conn)
    create_attendance_table(conn)
    
    # Close the connection
    conn.close()

if __name__ == '__main__':
    init_db()
