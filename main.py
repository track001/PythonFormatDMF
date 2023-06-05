import csv
from datetime import datetime, date
import os


# Function to encrypt/mask SSN
def encrypt_ssn(ssn):
  return '*' * 9 + ssn[-4:]


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
  print("Q. Quit")
  option = input("\nEnter the option number (or 'Q' to quit): ")

  if option == '1':
    display_verified_individuals()
  elif option == '2':
    age = int(input("Enter the age to filter by: "))
    filter_by_age(age)
  elif option == '3':
    download_verified_csv()
    print("CSV file downloaded successfully!")
  elif option.lower() == 'q':
    break
  else:
    print("Invalid option. Please try again.")
