import sqlite3

# Database Initialization
conn = sqlite3.connect('hospital.db')
c = conn.cursor()

# Function to print doctor table
def print_doctor_table():
    c.execute("SELECT * FROM doctor")
    rows = c.fetchall()
    print("Doctor Table:")
    print("ID\tName\tSpecialization\tDuration")
    for row in rows:
        print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}")

# Function to print appointments table
def print_appointments_table():
    c.execute("SELECT * FROM appointments")
    rows = c.fetchall()
    print("\nAppointments Table:")
    print("ID\tPatient Name\tDate\tAge\tGender\tDoctor ID")
    for row in rows:
        print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}")

# Call the functions
print_doctor_table()
print_appointments_table()

# Closing the database connection
conn.close()
