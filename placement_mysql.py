import mysql.connector


# ================= DATABASE CONNECTION =================

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="placement_db"
    )

    cursor = connection.cursor()

    print("Connected Successfully!")

except Exception as e:
    print("Connection Error:", e)
    exit()


# ================= ADD STUDENT =================

def add_student():

    usn = input("Enter USN: ")
    name = input("Enter Name: ")
    department = input("Enter Department: ")
    cgpa = float(input("Enter CGPA: "))
    email = input("Enter Email: ")
    phone = input("Enter Phone: ")

    query = """
    INSERT INTO students
    (usn,name,department,cgpa,email,phone)
    VALUES (%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(query,
    (usn,name,department,cgpa,email,phone))

    connection.commit()

    print("Student Added Successfully!")


# ================= VIEW STUDENTS =================

def view_students():

    cursor.execute("SELECT * FROM students")

    data = cursor.fetchall()

    print("\n===== Students =====")

    for s in data:
        print("USN:",s[0])
        print("Name:",s[1])
        print("Department:",s[2])
        print("CGPA:",s[3])
        print("Email:",s[4])
        print("Phone:",s[5])
        print("----------------")


# ================= ADD COMPANY =================

def add_company():

    name = input("Enter Company Name: ")
    role = input("Enter Job Role: ")
    package = float(input("Enter Package: "))
    cgpa = float(input("Enter Eligibility CGPA: "))
    location = input("Enter Location: ")


    query = """
    INSERT INTO companies
    (company_name,job_role,package,eligibility_cgpa,location)
    VALUES(%s,%s,%s,%s,%s)
    """

    cursor.execute(query,
    (name,role,package,cgpa,location))

    connection.commit()

    print("Company Added Successfully!")


# ================= VIEW COMPANIES =================

def view_companies():

    cursor.execute("SELECT * FROM companies")

    companies = cursor.fetchall()

    print("\n===== Companies =====")

    for c in companies:

        print("Company ID:",c[0])
        print("Name:",c[1])
        print("Role:",c[2])
        print("Package:",c[3])
        print("CGPA:",c[4])
        print("Location:",c[5])
        print("----------------")


# ================= ADD DRIVE =================

def add_drive():

    company_id = int(input("Enter Company ID: "))
    date = input("Enter Drive Date (YYYY-MM-DD): ")
    role = input("Enter Job Role: ")
    package = float(input("Enter Package: "))
    cgpa = float(input("Enter Eligibility CGPA: "))
    location = input("Enter Location: ")


    query = """
    INSERT INTO drives
    (company_id,drive_date,job_role,package,eligibility_cgpa,location)
    VALUES(%s,%s,%s,%s,%s,%s)
    """


    cursor.execute(query,
    (company_id,date,role,package,cgpa,location))

    connection.commit()

    print("Placement Drive Added Successfully!")


# ================= VIEW DRIVES =================

def view_drives():

    cursor.execute("SELECT * FROM drives")

    drives = cursor.fetchall()

    print("\n===== Placement Drives =====")


    for d in drives:

        print("Drive ID:",d[0])
        print("Company ID:",d[1])
        print("Date:",d[2])
        print("Role:",d[3])
        print("Package:",d[4])
        print("CGPA:",d[5])
        print("Location:",d[6])
        print("----------------")


# ================= APPLY FOR DRIVE =================

def apply_for_drive():

    usn = input("Enter Student USN: ")

    drive_id = int(input("Enter Drive ID: "))


    query = """
    INSERT INTO applications
    (usn,drive_id)
    VALUES(%s,%s)
    """


    cursor.execute(query,(usn,drive_id))

    connection.commit()

    print("Application Submitted Successfully!")


# ================= VIEW APPLICATIONS =================

def view_applications():

    query = """
    SELECT 
    applications.application_id,
    students.name,
    companies.company_name,
    drives.job_role,
    applications.status

    FROM applications

    JOIN students
    ON applications.usn=students.usn

    JOIN drives
    ON applications.drive_id=drives.drive_id

    JOIN companies
    ON drives.company_id=companies.company_id
    """

    cursor.execute(query)

    data=cursor.fetchall()


    print("\n===== Applications =====")


    for a in data:

        print("Application ID:",a[0])
        print("Student:",a[1])
        print("Company:",a[2])
        print("Role:",a[3])
        print("Status:",a[4])
        print("----------------")


# ================= MAIN MENU =================


while True:

    print("\n========== Placement Management System ==========")

    print("1. Add Student")
    print("2. View Students")
    print("3. Add Company")
    print("4. View Companies")
    print("5. Add Drive")
    print("6. View Drives")
    print("7. Apply for Drive")
    print("8. View Applications")
    print("9. Exit")


    choice=input("Enter Your Choice: ")


    if choice=="1":
        add_student()

    elif choice=="2":
        view_students()

    elif choice=="3":
        add_company()

    elif choice=="4":
        view_companies()

    elif choice=="5":
        add_drive()

    elif choice=="6":
        view_drives()

    elif choice=="7":
        apply_for_drive()

    elif choice=="8":
        view_applications()

    elif choice=="9":

        print("Thank You!")
        break

    else:
        print("Invalid Choice")