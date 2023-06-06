import csv
from datetime import datetime, date
import os
import requests
import tkinter as tk
from tkinter import filedialog, messagebox


# Function to encrypt/mask SSN
def encrypt_ssn(ssn):
  return '*' * 9 + ssn[-4:]


# Function to download the Death Master File CSV from NTIS website
def download_csv_from_ntis(url, destination):
  response = requests.get(url)
  with open(destination, 'wb') as file:
    file.write(response.content)


# Function to display all verified individuals
def display_verified_individuals():
  verified_individuals_text.delete(1.0, tk.END)
  verified_individuals_text.insert(
    tk.END,
    f"Total number of verified individuals: {len(verified_individuals)}\n")
  ages = set([individual[3] for individual in verified_individuals])
  verified_individuals_text.insert(
    tk.END, f"Available ages: {', '.join(str(age) for age in ages)}\n")
  for i, individual in enumerate(verified_individuals):
    verified_individuals_text.insert(
      tk.END,
      f"{i+1}. Name: {individual[0]} {individual[1]}, Age: {individual[3]}, Encrypted SSN: {individual[2]}, Original SSN: {individual[4]}\n"
    )


# Function to filter verified individuals by age
def filter_by_age():
  age = int(age_entry.get())
  filtered_individuals = [
    individual for individual in verified_individuals if individual[3] == age
  ]
  filtered_individuals_text.delete(1.0, tk.END)
  filtered_individuals_text.insert(
    tk.END,
    f"Total number of individuals at age {age}: {len(filtered_individuals)}\n")
  for i, individual in enumerate(filtered_individuals):
    filtered_individuals_text.insert(
      tk.END,
      f"{i+1}. Name: {individual[0]} {individual[1]}, Age: {individual[3]}, Encrypted SSN: {individual[2]}, Original SSN: {individual[4]}\n"
    )


# Function to handle the download button click event
def download_button_click():
  url = 'https://dmf.ntis.gov/weekly/'
  destination = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=(("CSV files", "*.csv"),
                                                        ("All files", "*.*")))
  if destination:
    try:
      download_csv_from_ntis(url, destination)
      messagebox.showinfo("Success", "CSV file downloaded successfully!")
    except Exception as e:
      messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Create the main window
window = tk.Tk()
window.title("NTIS Data")
window.geometry("600x400")

# Create and position the labels, entries, buttons, and text areas

title_label = tk.Label(window, text="NTIS Data", font=("Arial", 16))
title_label.pack(pady=10)

# Options frame
options_frame = tk.Frame(window)
options_frame.pack(pady=10)

# Option 1: View all verified individuals
option1_button = tk.Button(options_frame,
                           text="View all verified individuals",
                           command=display_verified_individuals)
option1_button.grid(row=0, column=0, padx=5)

# Option 2: Filter by age
option2_label = tk.Label(options_frame, text="Filter by age:")
option2_label.grid(row=0, column=1, padx=5)

age_entry = tk.Entry(options_frame, width=5)
age_entry.grid(row=0, column=2, padx=5)

filter_button = tk.Button(options_frame, text="Filter", command=filter_by_age)
filter_button.grid(row=0, column=3, padx=5)

# Option 3: Download a new CSV with verified individuals
download_button = tk.Button(options_frame,
                            text="Download CSV",
                            command=download_button_click)
download_button.grid(row=0, column=4, padx=5)

# Verified individuals text area
verified_individuals_text = tk.Text(window, height=10, width=60)
verified_individuals_text.pack()

# Filtered individuals text area
filtered_individuals_text = tk.Text(window, height=10, width=60)
filtered_individuals_text.pack()

# Quit button
quit_button = tk.Button(window, text="Quit", command=window.quit)
quit_button.pack(pady=10)

# Read the Death Master File from CSV
csv_file_path = 'death_master_file.csv'
verified_individuals = []

with open(csv_file_path, 'r') as file:
  csv_reader = csv.reader(file)
  next(csv_reader)  # Skip the header row
  for row in csv_reader:
    first_name = row[0]
    last_name = row[1]
    middle_initial = row[2]
    date_of_birth = row[3]
    date_of_death = row[4]
    ssn = row[5]
    verification = row[6]
    if verification.strip().lower() == 'verified':
      today = date.today()
      birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
      age = today.year - birth_date.year - ((today.month, today.day) <
                                            (birth_date.month, birth_date.day))
      encrypted_ssn = encrypt_ssn(ssn)
      verified_individuals.append(
        [first_name, last_name, encrypted_ssn, age, ssn])

# Start the GUI event loop
window.mainloop()


# Function to encrypt/mask SSN
def encrypt_ssn(ssn):
  return '*' * 9 + ssn[-4:]


# Function to download the Death Master File CSV from NTIS website
def download_csv_from_ntis(url, destination):
  response = requests.get(url)
  with open(destination, 'wb') as file:
    file.write(response.content)


# File path of the Death Master File CSV
csv_file_path = 'death_master_file.csv'

# List to store verified individuals
verified_individuals = []

# Read the Death Master File from CSV
with open(csv_file_path, 'r') as file:
  csv_reader = csv.reader(file)
  next(csv_reader)  # Skip the header row

  # Process each record in the Death Master File
  for row in csv_reader:
    first_name = row[0]
    last_name = row[1]
    middle_initial = row[2]
    date_of_birth = row[3]
    date_of_death = row[4]
    ssn = row[5]
    verification = row[6]

    # Check if the customer is verified as deceased
    if verification.strip().lower() == 'verified':
      # Calculate the age based on today's date and the date of birth
      today = date.today()
      birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
      age = today.year - birth_date.year - ((today.month, today.day) <
                                            (birth_date.month, birth_date.day))

      # Encrypt the SSN
      encrypted_ssn = encrypt_ssn(ssn)

      # Add the record to the verified individuals list
      verified_individuals.append(
        [first_name, last_name, encrypted_ssn, age, ssn])


# Function to display all verified individuals
def display_verified_individuals():
  print("Total number of verified individuals:", len(verified_individuals))
  ages = set([individual[3] for individual in verified_individuals])
  print("Available ages:", ", ".join(str(age) for age in ages))
  for i, individual in enumerate(verified_individuals):
    print(
      f"{i+1}. Name: {individual[0]} {individual[1]}, Age: {individual[3]}, Encrypted SSN: {individual[2]}, Original SSN: {individual[4]}"
    )


# Function to filter verified individuals by age
def filter_by_age(age):
  filtered_individuals = [
    individual for individual in verified_individuals if individual[3] == age
  ]
  print(
    f"Total number of individuals at age {age}: {len(filtered_individuals)}")
  for i, individual in enumerate(filtered_individuals):
    print(
      f"{i+1}. Name: {individual[0]} {individual[1]}, Age: {individual[3]}, Encrypted SSN: {individual[2]}, Original SSN: {individual[4]}"
    )


# Function to download verified individuals as a new CSV
def download_verified_csv():
  base_filename = f"verified_individuals_{datetime.now().strftime('%m%d%Y')}"
  filename = base_filename + ".csv"
  index = 97  # ASCII value for 'a'
  while os.path.exists(filename):
    filename = f"{base_filename}{chr(index)}.csv"
    index += 1

  with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["First Name", "Last Name", "Encrypted SSN", "Age"])
    for individual in verified_individuals:
      encrypted_ssn = "******" + individual[2][-4:]  # Encrypt the SSN
      writer.writerow(
        [individual[0], individual[1], encrypted_ssn, individual[3]])


# Main program loop
while True:
  # Display the current date
  print("\nToday's date:", date.today().strftime("%m-%d-%Y"))
  print("\nOptions:")
  print("1. View all verified individuals")
  print("2. Filter by age")
  print("3. Download a new CSV with verified individuals")
  print("4. Download weekly or monthly update from NTIS file")
  print("Q. Quit")
  option = input("\nEnter the option number (or 'Q' to quit): ")

  if option == '1':
    display_verified_individuals()
  elif option == '2':
    age = int(input("Enter the age to filter by: "))
    filter_by_age(age)
  elif option == '3':
    # Specify the URL of the Death Master File on the NTIS website
    url = 'https://dmf.ntis.gov/weekly/'
    # Specify the destination path to save the downloaded file
    destination = 'C:\\Users\\schwarzt\\Desktop\\death_master_file.csv'

    download_csv_from_ntis(url, destination)
    print("CSV file downloaded successfully!")
  elif option == '4':
    print("Choose the update frequency:")
    print("1. Weekly")
    print("2. Monthly")
    frequency_option = input("Enter the option number: ")

    if frequency_option == '1':
      # Specify the URL for the weekly update
      url = 'https://dmf.ntis.gov/weekly/'
    elif frequency_option == '2':
      # Specify the URL for the monthly update
      url = 'https://dmf.ntis.gov/monthly/'
    else:
      print("Invalid option. Please try again.")
      continue

    destination = 'C:\\Users\\schwarzt\\Desktop\\death_master_file.csv'
    download_csv_from_ntis(url, destination)
    print("CSV file downloaded successfully!")
  elif option.lower() == 'q':
    break
  else:
    print("Invalid option. Please try again.")
