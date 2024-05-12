import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import sqlite3
import re
from PIL import Image

# Database Initialization
conn = sqlite3.connect('hospital.db')
c = conn.cursor()

# Create Doctor Table
c.execute('''CREATE TABLE IF NOT EXISTS doctor
             (id INTEGER PRIMARY KEY,
             name TEXT,
             specialization TEXT,
             duration TEXT)''')

# Create Appointments Table
c.execute('''CREATE TABLE IF NOT EXISTS appointments
             (id INTEGER PRIMARY KEY,
             patient_name TEXT,
             date TEXT,
             gender TEXT,
             doctor_id INTEGER,
             age INTEGER,
             FOREIGN KEY(doctor_id) REFERENCES doctor(id))''')

# Functions
def add_doctor_details():
    add_doctor_window = tk.Toplevel(root)
    add_doctor_window.title("Add Doctor Details")
    add_doctor_window.geometry("300x200")

    def add_doctor():
        name = doctor_name_entry.get()
        specialization = doctor_specialization_entry.get()
        duration = doctor_duration_entry.get()
        c.execute("INSERT INTO doctor (name, specialization, duration) VALUES (?, ?, ?)", (name, specialization, duration))
        conn.commit()
        add_doctor_window.destroy()

    doctor_name_label = tk.Label(add_doctor_window, text="Doctor Name:")
    doctor_name_label.pack()
    doctor_name_entry = tk.Entry(add_doctor_window)
    doctor_name_entry.pack()

    doctor_specialization_label = tk.Label(add_doctor_window, text="Specialization:")
    doctor_specialization_label.pack()
    doctor_specialization_entry = tk.Entry(add_doctor_window)
    doctor_specialization_entry.pack()

    doctor_duration_label = tk.Label(add_doctor_window, text="Duration (eg. 2-4, 18-20):")
    doctor_duration_label.pack()
    doctor_duration_entry = tk.Entry(add_doctor_window)
    doctor_duration_entry.pack()

    add_doctor_button = tk.Button(add_doctor_window, text="Add Doctor", command=add_doctor, bg="red")
    add_doctor_button.pack(pady=10)

def add_appointment_details():
    add_appointment_window = tk.Toplevel(root)
    add_appointment_window.title("Add Appointment Details")
    add_appointment_window.geometry("300x250")

    def add_appointment():
        patient_name = patient_name_entry.get()
        date = date_entry.get()
        age = int(age_entry.get())
        gender = gender_var.get()
        doctor_id = re.findall(r'\d+', doctor_var.get())[0]  # Extracting doctor ID using regular expression
        c.execute("INSERT INTO appointments (patient_name, date, gender, doctor_id, age) VALUES (?, ?, ?, ?, ?)", (patient_name, date, gender, doctor_id, age))
        conn.commit()
        add_appointment_window.destroy()

    patient_name_label = tk.Label(add_appointment_window, text="Patient Name:")
    patient_name_label.pack()
    patient_name_entry = tk.Entry(add_appointment_window)
    patient_name_entry.pack()

    date_label = tk.Label(add_appointment_window, text="Date:")
    date_label.pack()
    date_entry = tk.Entry(add_appointment_window)
    date_entry.pack()

    age_label = tk.Label(add_appointment_window, text="Age:")
    age_label.pack()
    age_entry = tk.Entry(add_appointment_window)
    age_entry.pack()

    gender_label = tk.Label(add_appointment_window, text="Gender:")
    gender_label.pack()
    gender_var = tk.StringVar(add_appointment_window)
    gender_var.set("Male")
    gender_dropdown = ttk.Combobox(add_appointment_window, textvariable=gender_var, values=["Male", "Female", "Other"])
    gender_dropdown.pack()

    c.execute("SELECT id, name FROM doctor")
    doctors = c.fetchall()
    doctor_var = tk.StringVar(add_appointment_window)
    doctor_dropdown = ttk.Combobox(add_appointment_window, textvariable=doctor_var, values=[f"{doctor[0]} - {doctor[1]}" for doctor in doctors])
    doctor_dropdown.pack()

    add_appointment_button = tk.Button(add_appointment_window, text="Add Appointment", command=add_appointment, bg="green")
    add_appointment_button.pack(pady=10)

def show_appointments():
    appointments_window = tk.Toplevel(root)
    appointments_window.title("Appointments")

    c.execute("SELECT * FROM appointments")
    appointments = c.fetchall()
    for i, appointment in enumerate(appointments):
        tk.Label(appointments_window, text=f"Appointment {i+1}: {appointment}").pack()

# Tkinter App Initialization
root = tk.Tk()
root.title("Hospital Management System")
root.attributes('-fullscreen', True)  # Make window full-screen

# Convert image to supported format
image = Image.open("bg2.jpeg")
image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))  # Resize image to fit full screen
image.save("background_image.gif")

# Load background image
background_image = PhotoImage(file="background_image.gif")

# Set background image on root window
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Buttons
add_doctor_button = tk.Button(root, text="Add Doctor Details", command=add_doctor_details, bg="red")
add_doctor_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

add_appointment_button = tk.Button(root, text="Add Appointment Details", command=add_appointment_details, bg="green")
add_appointment_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

show_appointments_button = tk.Button(root, text="Show Appointments", command=show_appointments, bg="orange")
show_appointments_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

root.mainloop()

# Closing the database connection
conn.close()
