from flask import Flask, render_template, request, redirect, make_response
import sqlite3
from schema_003 import init_db, db
from datetime import datetime
import pdfkit
import os

# Install wkhtmltopdf on Debian-based systems
os.system("apt-get update && apt-get install -y wkhtmltopdf")

app = Flask(__name__)
app.config['SERVER_NAME'] = 'aaas-qr.onrender.com'

# Configure PDFKit to use wkhtmltopdf installed on Windows
PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=r'/usr/bin/wkhtmltopdf')

# Home route to display attendance form
@app.route('/')
def home():
    return render_template('index.html')  # Create an HTML form to upload QR


@app.route('/register', methods=['POST'])
def register_student():
    # """Register a new student in the database."""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    admission_no = request.form['admission_no']

    # Insert the new student into the Students table
    conn = sqlite3.connect(db)
    try:
        with conn:
            conn.execute('''
                INSERT INTO Students (first_name, last_name, admission_no) 
                VALUES (?, ?, ?);
            ''', (first_name, last_name, admission_no))
        return f'Student {first_name} {last_name} registered successfully!'
    except sqlite3.IntegrityError:
        return f'Error: admission_no {admission_no} is already registered.'
    finally:
        conn.close()


# Function to mark attendance in database
@app.route('/mark_attendance/<path:admission_no>', methods = ['GET', 'POST'])
def mark_attendance(admission_no):
    # admission_no = str(admission_no)

    # # Split the string at 'STUDENT ID' and get the second part
    # admission_no = admission_no.split('STUDENT ID')[1].strip()  # Using strip() to remove any leading/trailing whitespace

    print(admission_no)

    # """Mark attendance for a student in a specific course."""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    # Get the current date (you might want to adjust this format)
    attendance_date = datetime.now().date()
    print("Form data:", request.form)
    print("Query params:", request.args)
    roll = request.args.get('rollcall_for')

    # Select the student_id using the admission number
    cursor.execute('''
        SELECT student_id 
        FROM Students 
        WHERE admission_no = ?;
    ''', (admission_no,))

    student_record = cursor.fetchone()



 
    # Check if student exists
    if student_record is None:
        return f"No student found with admission number {admission_no}.", 404  # Not found response
    
    student_id = student_record[0]  # Extracting the student_id from the tuple

    # Insert the attendance record
    cursor.execute('''
        INSERT INTO Attendance (student_id, attendance_date, rollcall_for) 
        VALUES (?, ?, ?);
    ''', (student_id, attendance_date, roll))
    
    conn.commit()
    conn.close
    return redirect('/records')  # Redirect to the records page to view attendance



@app.route('/records', methods=['POST', 'GET'])
def view_records():
    """View attendance records with student details."""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    filter_date = ""

    # Get date filter from form submission (if any)
    if request.form.get('filter_date'):
        filter_date = request.form['filter_date']

    print(filter_date + " date")
    
  # Query with or without date filter
    if filter_date != "":
        cursor.execute('''
            SELECT 
                Attendance.attendance_id, 
                Attendance.attendance_date,
                Attendance.rollcall_for, 
                Students.first_name, 
                Students.last_name, 
                Students.admission_no
            FROM Attendance 
            JOIN Students ON Attendance.student_id = Students.student_id
            WHERE Attendance.attendance_date = ?;
        ''', (filter_date,))
    else:
        cursor.execute('''
            SELECT 
                Attendance.attendance_id, 
                Attendance.attendance_date,
                Attendance.rollcall_for, 
                Students.first_name, 
                Students.last_name, 
                Students.admission_no
            FROM Attendance 
            JOIN Students ON Attendance.student_id = Students.student_id;
        ''')

    
    records = cursor.fetchall()
    print(records)
    # conn.close()
    
    # Render the records in the HTML template
    return render_template('records.html', records=records)



@app.route('/records/pdf', methods=['GET', 'POST'])
def view_records_pdf():
    """Generate a PDF of the attendance records with optional date filter."""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Get date filter from form submission (if any)
    filter_date = request.args.get('filter_date')

    # Query with or without date filter
    if filter_date:
        cursor.execute('''
            SELECT 
                Attendance.attendance_id, 
                Attendance.attendance_date,
                Attendance.rollcall_for, 
                Students.first_name, 
                Students.last_name, 
                Students.admission_no
            FROM Attendance 
            JOIN Students ON Attendance.student_id = Students.student_id
            WHERE Attendance.attendance_date = ?;
        ''', (filter_date,))
    else:
        cursor.execute('''
           SELECT 
                Attendance.attendance_id, 
                Attendance.attendance_date,
                Attendance.rollcall_for, 
                Students.first_name, 
                Students.last_name, 
                Students.admission_no
            FROM Attendance 
            JOIN Students ON Attendance.student_id = Students.student_id;
        ''')

    records = cursor.fetchall()
    conn.close()
    
    # Render HTML and convert to PDF
    html = render_template('records.html', records=records, filter_date=filter_date)
    
    pdf = pdfkit.from_string(html, False, configuration=PDFKIT_CONFIG)


    # Create a response with the PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=attendance_records.pdf'
    return response



if __name__ == "__main__":
    init_db()  # Initialize the database
    app.run(debug=True, host='0.0.0.0', port=8000)
