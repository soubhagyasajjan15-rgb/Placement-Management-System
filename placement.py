import json
import os
import csv

FILE_NAME = "students.json"
COMPANY_FILE = "companies.json"
DRIVE_FILE = "drives.json"

USERNAME = "admin"
PASSWORD = "admin123"


# Load students data
def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except:
            return []
    else:
        return []

def load_file(filename):
    
    if os.path.exists(filename):

        try:
            with open(filename,"r") as file:
                return json.load(file)

        except:
            return []

    return []


# Save students data
def save_data():
    with open(FILE_NAME, "w") as file:
        json.dump(students, file, indent=4)


students = load_data()
companies = load_file(COMPANY_FILE)

drives = load_file(DRIVE_FILE)


# Admin Login
def login():
    print("\n===== Admin Login =====")

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    if username == USERNAME and password == PASSWORD:
        print("\nLogin Successful!")
        return True
    else:
        print("\nInvalid Username or Password!")
        return False



# Add Student
def add_student():

    print("\n===== Add Student =====")

    usn = input("Enter USN: ")

    for student in students:
        if student["usn"] == usn:
            print("USN already exists!")
            return


    while True:
        name = input("Enter Name: ")

        if name.strip() == "":
            print("Name cannot be empty!")
        else:
            break


    while True:
        branch = input("Enter Branch: ")

        if branch.strip() == "":
            print("Branch cannot be empty!")
        else:
            break


    while True:
        try:
            cgpa = float(input("Enter CGPA (0-10): "))

            if cgpa >= 0 and cgpa <= 10:
                break
            else:
                print("CGPA must be between 0 and 10")

        except:
            print("Enter valid CGPA")


    if cgpa >= 7:
        status = "Eligible"
    else:
        status = "Not Eligible"


    student = {
        "usn": usn,
        "name": name,
        "branch": branch,
        "cgpa": cgpa,
        "status": status
    }


    students.append(student)
    save_data()

    print("\nStudent Added Successfully!")



# View Students
def view_students():

    print("\n===== Student Details =====")

    if len(students) == 0:
        print("No Records Found")
        return


    for student in students:

        print("-------------------------")
        print("USN    :", student["usn"])
        print("Name   :", student["name"])
        print("Branch :", student["branch"])
        print("CGPA   :", student["cgpa"])
        print("Status :", student["status"])



# Search Student
def search_student():

    usn = input("\nEnter USN to Search: ")

    for student in students:

        if student["usn"] == usn:

            print("\nStudent Found")
            print("----------------")
            print("USN    :", student["usn"])
            print("Name   :", student["name"])
            print("Branch :", student["branch"])
            print("CGPA   :", student["cgpa"])
            print("Status :", student["status"])

            return


    print("Student Not Found")



# Update Student
def update_student():

    usn = input("\nEnter USN to Update: ")

    for student in students:

        if student["usn"] == usn:

            student["name"] = input("Enter New Name: ")
            student["branch"] = input("Enter New Branch: ")

            while True:
                try:
                    cgpa = float(input("Enter New CGPA: "))

                    if 0 <= cgpa <= 10:
                        break
                    else:
                        print("Invalid CGPA")

                except:
                    print("Enter valid CGPA")


            student["cgpa"] = cgpa


            if cgpa >= 7:
                student["status"] = "Eligible"
            else:
                student["status"] = "Not Eligible"


            save_data()

            print("Student Updated Successfully!")
            return


    print("Student Not Found")



# Delete Student
def delete_student():

    usn = input("\nEnter USN to Delete: ")

    for student in students:

        if student["usn"] == usn:

            students.remove(student)
            save_data()

            print("Student Deleted Successfully!")
            return


    print("Student Not Found")

def save_file(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def add_company():
    company_name = input("Enter Company Name: ")
    role = input("Enter Job Role: ")
    package = input("Enter Package (LPA): ")

    company = {
        "company_name": company_name,
        "role": role,
        "package": package
    }

    companies.append(company)
    save_file(COMPANY_FILE, companies)
    print("Company Added Successfully!")


def view_companies():
    if len(companies) == 0:
        print("No Companies Available")
        return

    print("\n===== Companies =====")

    for company in companies:
        print("----------------------")
        print("Company :", company["company_name"])
        print("Role    :", company["role"])
        print("Package :", company["package"])


def add_drive():
    company = input("Enter Company Name: ")
    date = input("Enter Drive Date: ")
    venue = input("Enter Venue: ")

    drive = {
        "company": company,
        "date": date,
        "venue": venue
    }

    drives.append(drive)
    save_file(DRIVE_FILE, drives)
    print("Placement Drive Added Successfully!")


def view_drives():
    if len(drives) == 0:
        print("No Placement Drives")
        return

    print("\n===== Placement Drives =====")

    for drive in drives:
        print("----------------------")
        print("Company :", drive["company"])
        print("Date    :", drive["date"])
        print("Venue   :", drive["venue"])
def eligible_students():
    
    minimum_cgpa = float(input("Enter Minimum CGPA Required: "))

    found = False

    print("\n===== Eligible Students =====")

    for student in students:

        if student["cgpa"] >= minimum_cgpa:

            print("------------------------")
            print("USN    :", student["usn"])
            print("Name   :", student["name"])
            print("Branch :", student["branch"])
            print("CGPA   :", student["cgpa"])

            found = True

    if not found:
        print("No Eligible Students Found.")

def dashboard():
    
    total_students = len(students)
    total_companies = len(companies)
    total_drives = len(drives)

    eligible = 0
    not_eligible = 0

    for student in students:
        if student["cgpa"] >= 7:
            eligible += 1
        else:
            not_eligible += 1

    print("\n========== Dashboard ==========")
    print("Total Students        :", total_students)
    print("Eligible Students     :", eligible)
    print("Not Eligible Students :", not_eligible)
    print("Total Companies       :", total_companies)
    print("Total Placement Drives:", total_drives)

def export_to_csv():
    
    if len(students) == 0:
        print("No Student Records Found!")
        return

    with open("students_report.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["USN", "Name", "Branch", "CGPA", "Status"])

        for student in students:

            writer.writerow([
                student["usn"],
                student["name"],
                student["branch"],
                student["cgpa"],
                student["status"]
            ])

    print("Student Report Exported Successfully!")
def search_company():
    
    name = input("Enter Company Name: ").lower()

    found = False

    for company in companies:

        if company["company_name"].lower() == name:

            print("\n===== Company Found =====")
            print("Company :", company["company_name"])
            print("Role    :", company["role"])
            print("Package :", company["package"])

            found = True
            break

    if not found:
        print("Company Not Found!")
def delete_company():
    
    name = input("Enter Company Name to Delete: ").lower()

    for company in companies:

        if company["company_name"].lower() == name:

            companies.remove(company)
            save_file(COMPANY_FILE, companies)

            print("Company Deleted Successfully!")
            return

    print("Company Not Found!")
while True:

    print("\n========== Placement Management System ==========")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Add Company")
    print("7. View Companies")
    print("8. Add Placement Drive")
    print("9. View Drives")
    print("10. Exit")
    print("10. Eligible Students")
    print("11. Exit")

    choice = input("Enter Your Choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        search_student()

    elif choice == "4":
        update_student()

    elif choice == "5":
        delete_student()

    elif choice == "6":
        add_company()

    elif choice == "7":
        view_companies()

    elif choice == "8":
        search_company()

    elif choice == "9":
        delete_company()

    elif choice == "10":
        add_drive()

    elif choice == "11":
        view_drives()

    elif choice == "12":
        eligible_students()

    elif choice == "13":
        dashboard()

    elif choice == "14":
        export_to_csv()

    elif choice == "15":
        print("Thank You!")
    break

else:
    print("Invalid Choice!")