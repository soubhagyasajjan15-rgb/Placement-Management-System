from flask import Flask, render_template, request, redirect, url_for, session
from database import get_connection
from flask import send_from_directory

import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "placement_management_system_2026"
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "placement123"

USERNAME = "admin"
PASSWORD = "admin123"

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# ---------------- Login ----------------

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:
            return redirect(url_for("dashboard"))
        else:
            return "Invalid Username or Password"

    return render_template("login.html")


# ---------------- Dashboard ----------------

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ---------------- Add Student ----------------

@app.route("/students", methods=["GET", "POST"])
def students():

    if request.method == "POST":

        usn = request.form["usn"]
        name = request.form["name"]
        department = request.form["department"]
        cgpa = request.form["cgpa"]
        email = request.form["email"]
        phone = request.form["phone"]

        conn = get_connection()

        if conn is None:
            return "Database Connection Failed"

        cursor = conn.cursor()

        sql = """
        INSERT INTO students
        (usn, name, department, cgpa, email, phone)
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        values = (
            usn,
            name,
            department,
            cgpa,
            email,
            phone
        )

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("view_students"))

    return render_template("students.html")


# ---------------- View Students ----------------

@app.route("/view_students")
def view_students():

    conn = get_connection()

    if conn is None:
        return "Database Connection Failed"

    cursor = conn.cursor()

    cursor.execute("""
    SELECT usn, name, department, cgpa, email, phone, resume
    FROM students
""")

    students = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "view_students.html",
        students=students
    )

from flask import send_from_directory

@app.route("/view_resume/<usn>")
def view_resume(usn):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT resume FROM students WHERE usn=%s",
        (usn,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result is None or result[0] is None:
        return "Resume not found."

    return send_from_directory("uploads", result[0])

@app.route("/edit_student/<usn>", methods=["GET", "POST"])
def edit_student(usn):

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        department = request.form["department"]
        cgpa = request.form["cgpa"]
        email = request.form["email"]
        phone = request.form["phone"]

        cursor.execute("""
            UPDATE students
            SET
                name=%s,
                department=%s,
                cgpa=%s,
                email=%s,
                phone=%s
            WHERE usn=%s
        """, (name, department, cgpa, email, phone, usn))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("view_students"))

    cursor.execute("""
        SELECT usn, name, department, cgpa, email, phone
        FROM students
        WHERE usn=%s
    """, (usn,))

    student = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("edit_student.html", student=student)
@app.route("/delete_student/<usn>")
def delete_student(usn):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE usn=%s",
        (usn,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("view_students"))
@app.route("/search_student", methods=["GET", "POST"])
def search_student():

    students = []

    if request.method == "POST":

        keyword = request.form["keyword"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT usn, name, department, cgpa, email, phone
            FROM students
            WHERE usn LIKE %s
               OR name LIKE %s
        """, ("%"+keyword+"%", "%"+keyword+"%"))

        students = cursor.fetchall()

        cursor.close()
        conn.close()

    return render_template("search_students.html", students=students)

# ---------------- Company ----------------

@app.route("/companies", methods=["GET", "POST"])
def companies():

    if request.method == "POST":

        company_name = request.form["company_name"]
        job_role = request.form["job_role"]
        package = request.form["package"]
        eligibility_cgpa = request.form["eligibility_cgpa"]
        location = request.form["location"]

        conn = get_connection()

        if conn is None:
            return "Database Connection Failed"

        cursor = conn.cursor()

        sql = """
        INSERT INTO companies
        (company_name, job_role, package, eligibility_cgpa, location)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            company_name,
            job_role,
            package,
            eligibility_cgpa,
            location
        )

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

        return "Company Added Successfully! <br><br><a href='/companies'>Add Another Company</a>"

    return render_template("companies.html")
@app.route("/view_companies")
def view_companies():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            c.company_id,
            c.company_name,
            d.job_role,
            d.package,
            d.eligibility_cgpa,
            d.location
        FROM companies c
        JOIN drives d
        ON c.company_id = d.company_id
    """)

    companies = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "view_companies.html",
        companies=companies
    )

@app.route("/view_company/<int:company_id>")
def view_company(company_id):

    conn = get_connection()

    if conn is None:
        return "Database Connection Failed"

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT company_id, company_name
        FROM companies
        WHERE company_id=%s
    """, (company_id,))

    company = cursor.fetchone()

    cursor.close()
    conn.close()

    if company is None:
        return "Company not found"

    return render_template(
        "company_details.html",
        company=company
    )
       
@app.route("/placement_drives")
def placement_drives():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            d.drive_id,
            c.company_name,
            d.job_role,
            d.package,
            d.eligibility_cgpa,
            d.location,
            d.drive_date
        FROM drives d
        JOIN companies c
            ON d.company_id = c.company_id
    """)

    drives = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("placement_drives.html", drives=drives)
@app.route("/edit_company/<int:company_id>", methods=["GET", "POST"])
def edit_company(company_id):

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        company_name = request.form["company_name"]
        job_role = request.form["job_role"]
        package = request.form["package"]
        eligibility_cgpa = request.form["eligibility_cgpa"]
        location = request.form["location"]

        cursor.execute("""
            UPDATE companies
            SET company_name=%s,
                job_role=%s,
                package=%s,
                eligibility_cgpa=%s,
                location=%s
            WHERE company_id=%s
        """, (
            company_name,
            job_role,
            package,
            eligibility_cgpa,
            location,
            company_id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("view_companies"))

    cursor.execute("""
        SELECT company_id,
               company_name,
               job_role,
               package,
               eligibility_cgpa,
               location
        FROM companies
        WHERE company_id=%s
    """, (company_id,))

    company = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("edit_company.html", company=company)
# 👇 DELETE COMPANY ROUTE

@app.route("/delete_company/<int:company_id>")
def delete_company(company_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM companies WHERE company_id = %s",
        (company_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("view_companies"))

# Drives
@app.route("/drives", methods=["GET", "POST"])
def drives():

    if request.method == "POST":

        company_id = request.form["company_id"]
        drive_date = request.form["drive_date"]
        job_role = request.form["job_role"]
        package = request.form["package"]
        eligibility_cgpa = request.form["eligibility_cgpa"]
        location = request.form["location"]

        conn = get_connection()

        cursor = conn.cursor()

        sql = """
        INSERT INTO drives
        (company_id, drive_date, job_role, package, eligibility_cgpa, location)
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        values = (
            company_id,
            drive_date,
            job_role,
            package,
            eligibility_cgpa,
            location
        )

        cursor.execute(sql, values)

        conn.commit()

        cursor.close()
        conn.close()

        return "Placement Drive Added Successfully!"

    return render_template("drives.html")

@app.route("/view_drives")
def view_drives():

    # Check if student is logged in
    if "student_usn" not in session:
        return redirect(url_for("student_login"))

    conn = get_connection()

    if conn is None:
        return "Database Connection Failed"
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT 
        d.drive_id,
        d.job_role,
        d.package,
        d.cgpa,
        d.location,
        c.company_name
    FROM drives d
    JOIN companies c
    ON d.company_id = c.company_id
""")

    drives = cursor.fetchall()
    drives = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("view_drives.html", drives=drives)

@app.route("/available_drives")
def available_drives():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            d.drive_id,
            d.company_id,
            d.job_role,
            d.package,
            d.eligibility_cgpa,
            d.location,
            d.drive_date,
            c.company_name
        FROM drives d
        JOIN companies c
        ON d.company_id = c.company_id
    """)

    drives = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "available_drives.html",
        drives=drives
    )


@app.route("/view_applications")
def view_applications():

    conn = get_connection()

    if conn is None:
        return "Database Connection Failed"

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            a.application_id,
            a.usn,
            c.company_name,
            d.job_role,
            d.location,
            a.status
        FROM applications a
        JOIN drives d
            ON a.drive_id = d.drive_id
        JOIN companies c
            ON d.company_id = c.company_id
        ORDER BY a.application_id
    """)

    applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "view_applications.html",
        applications=applications
    )

@app.route("/edit_application/<int:application_id>", methods=["GET", "POST"])
def edit_application(application_id):

    conn = get_connection()

    if conn is None:
        return "Database Connection Failed"

    cursor = conn.cursor()

    if request.method == "POST":

        status = request.form["status"]

        cursor.execute("""
            UPDATE applications
            SET status=%s
            WHERE application_id=%s
        """, (status, application_id))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("view_applications"))

    cursor.execute("""
        SELECT application_id, usn, status
        FROM applications
        WHERE application_id=%s
    """, (application_id,))

    application = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "edit_application.html",
        application=application
    )

@app.route("/search_students", methods=["GET", "POST"])
def search_students():

    conn = get_connection()

    if conn is None:
        return "Database Connection Failed"

    cursor = conn.cursor()

    students = []

    if request.method == "POST":

        keyword = "%" + request.form["keyword"] + "%"

        cursor.execute("""
            SELECT usn, name, department, cgpa, email, phone
            FROM students
            WHERE usn LIKE %s
               OR name LIKE %s
               OR department LIKE %s
        """, (keyword, keyword, keyword))

        students = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "search_students.html",
        students=students
    )

@app.route("/search_companies", methods=["GET", "POST"])
def search_companies():

    conn = get_connection()

    if conn is None:
        return "Database Connection Failed"

    cursor = conn.cursor()

    companies = []

    if request.method == "POST":

        keyword = "%" + request.form["keyword"] + "%"

        cursor.execute("""
            SELECT company_id, company_name
            FROM companies
            WHERE company_name LIKE %s
        """, (keyword,))

        companies = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "search_companies.html",
        companies=companies
    )
@app.route("/admin_applications")
def admin_applications():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            a.application_id,
            s.usn,
            s.name,
            s.resume,
            c.company_name,
            d.job_role,
            a.status
        FROM applications a
        JOIN students s
        ON a.usn = s.usn
        JOIN drives d
        ON a.drive_id = d.drive_id
        JOIN companies c
        ON d.company_id = c.company_id
    """)

    applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admin_applications.html",
        applications=applications
    )
@app.route("/update_status/<int:application_id>", methods=["GET", "POST"])
def update_status(application_id):

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        status = request.form["status"]

        cursor.execute("""
            UPDATE applications
            SET status=%s
            WHERE application_id=%s
        """, (status, application_id))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("admin_applications"))

    return """
    <form method='POST'>
        <select name='status'>
            <option>Applied</option>
            <option>Selected</option>
            <option>Rejected</option>
        </select>

        <br><br>

        <input type='submit' value='Update'>
    </form>
    """
@app.route("/apply/<int:drive_id>")
def apply_drive(drive_id):

    usn = session.get("student_usn")
    if not usn:
        return redirect("/student_login")

    conn = get_connection()
    cursor = conn.cursor()

    # Check CGPA eligibility
    cursor.execute("""
        SELECT s.cgpa, d.eligibility_cgpa
        FROM students s
        JOIN drives d
        ON d.drive_id = %s
        WHERE s.usn = %s
    """, (drive_id, usn))

    check = cursor.fetchone()

    if check:
        student_cgpa = check[0]
        required_cgpa = check[1]

        if student_cgpa < required_cgpa:
            cursor.close()
            conn.close()
            return "You are not eligible for this drive."

    # Check if already applied
    cursor.execute("""
        SELECT *
        FROM applications
        WHERE usn = %s AND drive_id = %s
    """, (usn, drive_id))

    existing = cursor.fetchone()

    if existing:
        cursor.close()
        conn.close()
        return "You have already applied for this drive."

    # Insert application
    cursor.execute("""
        INSERT INTO applications(usn, drive_id)
        VALUES(%s, %s)
    """, (usn, drive_id))

    conn.commit()

    cursor.close()
    conn.close()

    return "Application submitted successfully!"
# ---------------- Reports ----------------
@app.route("/reports")
def reports():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM companies")
    total_companies = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM drives")
    total_drives = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications")
    total_applications = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status='Selected'")
    selected = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status='Rejected'")
    rejected = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status='Applied'")
    applied = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return render_template(
        "reports.html",
        total_students=total_students,
        total_companies=total_companies,
        total_drives=total_drives,
        total_applications=total_applications,
        selected=selected,
        rejected=rejected,
        applied=applied
    )
# ---------------- Student Login ----------------
@app.route("/student_login", methods=["GET", "POST"])
def student_login():

    if request.method == "POST":

        usn = request.form["usn"].strip()
        password = request.form["password"].strip()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
    SELECT usn, name, department, cgpa
    FROM students
    WHERE UPPER(usn) = UPPER(%s) 
    AND password = %s
""", (usn, password))

        student = cursor.fetchone()

        print("USN entered:", usn)
        print("Password entered:", password)
        print("Student found:", student)

        cursor.close()
        conn.close()

        if student:
            session["student_usn"] = student[0]
            session["student_name"] = student[1]

            return redirect(url_for("student_dashboard"))

        return render_template(
            "student_login.html",
            error="Invalid USN or Password"
        )

    return render_template("student_login.html")

# ---------------- Student Dashboard ----------------

@app.route("/student_dashboard")
def student_dashboard():

    if "student_usn" not in session:
        return redirect(url_for("student_login"))

    return render_template(
        "student_dashboard.html",
        usn=session["student_usn"],
        name=session["student_name"]
    )

@app.route("/my_applications")
def my_applications():

    usn = session.get("student_usn")

    if not usn:
        return redirect(url_for("student_login"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            c.company_name,
            d.job_role,
            d.location,
            a.status
        FROM applications a
        JOIN drives d
        ON a.drive_id = d.drive_id
        JOIN companies c
        ON d.company_id = c.company_id
        WHERE a.usn = %s
    """, (usn,))

    applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "my_applications.html",
        applications=applications
    )

# ---------------- Student Logout ----------------
@app.route("/student_logout")
def student_logout():
    session.pop("student_usn", None)
    session.pop("student_name", None)
    return redirect(url_for("student_login"))
# ---------------- Student Drives ----------------

@app.route("/student_drives")
def student_drives():

    if "student_usn" not in session:
        return redirect(url_for("student_login"))

    conn = get_connection()
    cursor = conn.cursor()

    # Get student's CGPA
    cursor.execute("""
        SELECT cgpa
        FROM students
        WHERE usn=%s
    """, (session["student_usn"],))

    student = cursor.fetchone()
    cgpa = student[0]

    # Show only eligible drives
    cursor.execute("""
    SELECT 
        d.drive_id,
        c.company_name,
        d.job_role,
        d.package,
        d.eligibility_cgpa,
        d.location,
        d.company_id
    FROM drives d
    JOIN companies c
    ON d.company_id = c.company_id
    WHERE d.eligibility_cgpa <= %s
""", (cgpa,))

    drives = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "student_drives.html",
        drives=drives
    )

# ---------------- Student Profile ----------------

@app.route("/student_profile")
def student_profile():

    if "student_usn" not in session:
        return redirect(url_for("student_login"))

    usn = session.get("student_usn") or session.get("usn")

    conn = get_connection()

    if conn is None:
        return "Database Connection Failed"

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            usn,
            name,
            department,
            cgpa,
            email,
            phone,
            resume
        FROM students
        WHERE usn=%s
    """, (usn,))

    student = cursor.fetchone()

    cursor.close()
    conn.close()

    if student is None:
        return "Student not found"

    return render_template(
        "student_profile.html",
        student=student
    )

@app.route("/company/<int:company_id>")
def company_details(company_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT company_id,
               company_name,
               job_role,
               package,
               eligibility_cgpa,
               location
        FROM companies
        WHERE company_id=%s
    """, (company_id,))

    company = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "company_details.html",
        company=company
    )

# ---------------- One Click Apply ----------------

@app.route("/apply/<int:drive_id>")
def apply(drive_id):

    if "student_usn" not in session:
        return redirect(url_for("student_login"))

    conn = get_connection()
    cursor = conn.cursor()

    # Check if already applied
    cursor.execute("""
        SELECT *
        FROM applications
        WHERE usn=%s AND drive_id=%s
    """, (session["student_usn"], drive_id))

    already = cursor.fetchone()

    if already:
        cursor.close()
        conn.close()
        return "You have already applied for this drive."

    cursor.execute("""
        INSERT INTO applications(usn, drive_id, status)
        VALUES(%s,%s,'Applied')
    """, (session["student_usn"], drive_id))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("my_applications"))

@app.route("/admin_dashboard")
def admin_dashboard():

    conn = get_connection()

    if conn is None:
        return "Database Connection Failed"

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM companies")
    total_companies = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM drives")
    total_drives = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications")
    total_applications = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE status='Selected'
    """)
    selected_students = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return render_template(
        "admin_dashboard.html",
        total_students=total_students,
        total_companies=total_companies,
        total_drives=total_drives,
        total_applications=total_applications,
        selected_students=selected_students
    )

import os
from werkzeug.utils import secure_filename

app.config['UPLOAD_FOLDER'] = 'static/uploads'


@app.route("/upload_resume", methods=["GET", "POST"])
def upload_resume():

    if request.method == "POST":

        usn = request.form["usn"]

        file = request.files["resume"]

        if file:

            filename = secure_filename(file.filename)

            filepath = os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )

            file.save(filepath)

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE students
                SET resume=%s
                WHERE usn=%s
            """, (filename, usn))

            conn.commit()

            cursor.close()
            conn.close()

            return "Resume uploaded successfully"

    return render_template("upload_resume.html")
if __name__ == "__main__":
    app.run(debug=True)