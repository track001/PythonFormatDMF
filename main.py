import tkinter as tk  # GUI library
from tkinter import filedialog, messagebox, Menu  # Specific components from tkinter
from datetime import date  # Date-related functionality
import pandas as pd  # Data manipulation library
import time  # Time-related functionality
import os  # Operating system-related functionality
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # Cryptography-related functionality
from cryptography.hazmat.backends import default_backend  # Cryptography backend
from cryptography.hazmat.primitives import padding  # Padding for encryption
import urllib.request  # For making HTTP requests and downloading files

# Retrieve the password from the secret
password = os.environ.get("PASSWORD")

# Global variables
last_activity_time = time.time()
is_authenticated = False


# Function to check the password
def check_password():
  global is_authenticated
  entered_password = password_entry.get()
  if entered_password == password:
    is_authenticated = True
    password_window.destroy()
  else:
    messagebox.showerror("Authentication Failed", "Incorrect password.")


# Create a password entry window
password_window = tk.Tk()
password_window.title("Login")

# Add a label and entry field for the password
password_label = tk.Label(password_window, text="Password:")
password_label.pack()
password_entry = tk.Entry(password_window, show="*")
password_entry.pack()

# Add a button to check the password
password_button = tk.Button(password_window,
                            text="Enter",
                            command=check_password)
password_button.pack()

# Run the password entry window
password_window.mainloop()

# Only proceed if the user is authenticated
if is_authenticated:

  # Read the Death Master File from the specified file path and return it as a pandas DataFrame.
  def read_death_master_file(file_path):
    return pd.read_csv(file_path)

  # Calculate the age of a person based on their date of birth, date of death, and a reference date.
  def calculate_age(date_of_birth, date_of_death, reference_date=date.today()):
    age = reference_date.year - date_of_birth.year
    if reference_date < date_of_birth.replace(year=reference_date.year):
      age -= 1
    return age

  def display_verified_individuals():
    """
    Display the information of verified individuals.

    This function clears the text in `verified_individuals_text` widget, retrieves verified individuals from the
    `verified_individuals` DataFrame, and displays the information in the `verified_individuals_text` widget.
    It also updates the `verified_label` to show the count of verified individuals out of the total count.
    If no verified individuals are found, it displays an appropriate message.
    """
    verified_individuals_text.delete("1.0", tk.END)
    verified_individuals_text.insert(tk.END, "")

    if 'verified_individuals' in globals():
      if 'verification' in verified_individuals.columns:
        verified_df = verified_individuals[verified_individuals['verification']
                                           == 'Verified']
        verified_individuals_text.insert(tk.END,
                                         verified_df.to_string(index=False))
        verified_count = len(verified_df)
        total_count = len(verified_individuals)
        verified_label.config(
          text=f"Verified: {verified_count}/{total_count} people")
      else:
        verified_individuals_text.insert(tk.END,
                                         "No verified individuals found.")
        verified_label.config(text="Verified: 0/0 people")
    else:
      verified_individuals_text.insert(tk.END,
                                       "No verified individuals found.")
      verified_label.config(text="Verified: 0/0 people")

  def display_age_options(df):
    """
    Display the unique age options based on the date of birth and date of death columns in the given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the date of birth and date of death columns.

    This function checks if the 'date_of_birth' and 'date_of_death' columns exist in the DataFrame.
    If present, it calculates the age for each row based on the current date (today) using the 'calculate_age()' function.
    The unique age options are extracted from the 'Age' column and displayed in the 'age_options_text' widget.
    The existing text in the widget is cleared before inserting the new options.

    Note:
        The 'calculate_age()' function used here should be defined separately.

    """
    if 'date_of_birth' in df.columns and 'date_of_death' in df.columns:
      today = date.today()
      df['date_of_birth'] = pd.to_datetime(df['date_of_birth'])
      df['date_of_death'] = pd.to_datetime(df['date_of_death'])
      df['Age'] = df.apply(lambda row: calculate_age(
        row['date_of_birth'].date(), row['date_of_death'].date(), today),
                           axis=1)
      age_options = df['Age'].unique()
      age_options_text.delete("1.0", tk.END)
      age_options_text.insert(tk.END,
                              "\n".join(str(age) for age in age_options))

  def download_csv_from_ntis(url, destination):
    """
    Download a CSV file from the given URL and perform operations on the downloaded file.

    Args:
        url (str): The URL of the CSV file to download.
        destination (str): The local destination path where the CSV file will be saved.

    This function attempts to download the CSV file from the provided URL and saves it to the specified destination.
    It then reads the downloaded file using the `read_death_master_file()` function and assigns the result to the
    `verified_individuals` global variable.
    The age of each individual in the `verified_individuals` DataFrame is calculated using the `calculate_age()` function
    and added as a new 'Age' column.
    If the operations are successful, a success message is displayed using a message box, and the verified individuals
    and age options are displayed using the respective display functions.
    If there is an error parsing the CSV file, an error message is shown with the specific error details.
    If any other exception occurs during the execution, a general error message is displayed.
    """
    try:
      urllib.request.urlretrieve(url, destination)
      global verified_individuals
      verified_individuals = read_death_master_file(destination)
      verified_individuals['Age'] = verified_individuals.apply(
        lambda row: calculate_age(row['date_of_birth'], row['date_of_death']),
        axis=1)
      messagebox.showinfo("Success",
                          "CSV file downloaded and read successfully!")
      display_verified_individuals()
      display_age_options(verified_individuals)
    except pd.errors.ParserError as pe:
      messagebox.showerror("Error", f"Error parsing CSV file: {str(pe)}")
    except Exception as e:
      messagebox.showerror("Error", f"An error occurred: {str(e)}")

  def open_file_dialog():
    """
    Open a file dialog to select a CSV file and perform operations on the selected file.

    This function opens a file dialog that allows the user to select a CSV file.
    If a file is selected, it reads the file using the `read_death_master_file()` function and assigns the result to the
    `verified_individuals` global variable.
    A success message is displayed using a message box if the file is read successfully, and the verified individuals
    and age options are displayed using the respective display functions.
    If any exception occurs during the execution, an error message is displayed with the specific error details.
    If no file is selected, an information message is displayed.
    """
    file_path = filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"),
                                                      ("All files", "*.*")))
    if file_path:
      try:
        global verified_individuals
        verified_individuals = read_death_master_file(file_path)
        messagebox.showinfo("Success", "CSV file read successfully!")
        display_verified_individuals()
        display_age_options(verified_individuals)
      except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    else:
      messagebox.showinfo("Information", "No file selected.")

  # Create a menu for the fetch_from_ntis_button with options to fetch data weekly or monthly.
  def fetch_from_ntis():
    menu = Menu(fetch_from_ntis_button, tearoff=0)
    menu.add_command(label="Weekly", command=fetch_weekly)
    menu.add_command(label="Monthly", command=fetch_monthly)

    fetch_from_ntis_button.configure(menu=menu)

  def fetch_weekly():
    """
    Fetch the weekly data from the NTIS website and download it as a CSV file.

    This function constructs the URL for the weekly data from the NTIS website.
    It generates today's date in the format MMDDYYYY and uses it to generate an initial file name for saving the CSV file.
    A file dialog is opened to prompt the user to select the destination and file name for saving the downloaded CSV file.
    If a destination is selected, the function attempts to download the CSV file from the NTIS website using the
    `download_csv_from_ntis()` function.
    If any exception occurs during the execution, an error message is displayed with the specific error details.
    """
    url = "https://dmf.ntis.gov/weekly/"
    today = date.today().strftime("%m%d%Y")
    destination = filedialog.asksaveasfilename(
      defaultextension=".csv",
      filetypes=(("CSV files", "*.csv"), ("All files", "*.*")),
      initialfile=f"DMFVerificationsWeekly{today}")
    if destination:
      try:
        download_csv_from_ntis(url, destination)
      except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

  def fetch_monthly():
    """
    Fetch the monthly data from the NTIS website and download it as a CSV file.

    This function constructs the URL for the monthly data from the NTIS website.
    It generates today's date in the format MMDDYYYY and uses it to generate an initial file name for saving the CSV file.
    A file dialog is opened to prompt the user to select the destination and file name for saving the downloaded CSV file.
    If a destination is selected, the function attempts to download the CSV file from the NTIS website using the
    `download_csv_from_ntis()` function.
    If any exception occurs during the execution, an error message is displayed with the specific error details.
    """
    url = "https://dmf.ntis.gov/monthly/"
    today = date.today().strftime("%m%d%Y")
    destination = filedialog.asksaveasfilename(
      defaultextension=".csv",
      filetypes=(("CSV files", "*.csv"), ("All files", "*.*")),
      initialfile=f"DMFVerificationsMonthly{today}")
    if destination:
      try:
        download_csv_from_ntis(url, destination)
      except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

  def save_encrypted_csv(destination):
    """
    Save the verified individuals' data as an encrypted CSV file.

    Args:
        destination (str): The destination path where the encrypted CSV file will be saved.

    This function checks if a destination is provided. If so, it verifies the presence of the "verification" column
    in the `verified_individuals` DataFrame. If the column exists, it filters the DataFrame to include only the
    "Verified" individuals and creates a copy called `encrypted_df`.
    A key is generated using `os.urandom(32)` to be used for AES encryption.
    The function initializes a cipher with the AES algorithm and ECB mode.
    The SSN (Social Security Number) is encrypted by splitting it into two parts, padding the first part, and encrypting
    it using the AES cipher. The encrypted SSN is then concatenated with the second part of the original SSN.
    The function saves the modified `encrypted_df` DataFrame as a CSV file at the provided destination.
    A success message is displayed using a message box if the file is saved successfully.
    If no "verification" column is found in the `verified_individuals` DataFrame, an information message is displayed.
    """
    if destination:
      if "verification" in verified_individuals.columns:
        verified_df = verified_individuals[verified_individuals["verification"]
                                           == "Verified"]
        encrypted_df = verified_df.copy()
        backend = default_backend()
        key = os.urandom(32)
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)

        encrypted_ssn_list = []
        for ssn in encrypted_df["ssn"]:
          # Split the SSN into two parts: first 5 digits and last 4 digits
          ssn_first_part = ssn[:5]
          ssn_last_part = ssn[5:]

          # Pad the first part of the SSN to the block length (16 bytes) using PKCS7 padding
          ssn_first_part_bytes = ssn_first_part.encode()
          padder = padding.PKCS7(128).padder()
          padded_data = padder.update(ssn_first_part_bytes) + padder.finalize()

          encryptor = cipher.encryptor()  # Create a new encryptor for each SSN
          encrypted_ssn_first_part = encryptor.update(
            padded_data) + encryptor.finalize()
          encrypted_ssn = encrypted_ssn_first_part.hex(
          ) + ssn_last_part  # Concatenate

          encrypted_ssn_list.append(
            encrypted_ssn)  # Add encrypted SSN to the list

        encrypted_df[
          "ssn"] = encrypted_ssn_list  # Update the "ssn" column in the DataFrame
        encrypted_df.to_csv(
          destination,
          index=False)  # Save the encrypted DataFrame to a CSV File
        messagebox.showinfo("Success",
                            "Encrypted CSV file saved successfully!")
      else:
        messagebox.showinfo("Information",
                            "No verified individuals found to save.")

  def save_encrypted_csv_dialog():
    """
    Prompt the user to select a destination and save the verified individuals' data as an encrypted CSV file.

    This function generates today's date in the format MMDDYYYY and uses it to generate an initial file name for
    saving the encrypted CSV file.
    A file dialog is opened to prompt the user to select the destination and file name for saving the encrypted CSV file.
    If a destination is selected, the function calls the `save_encrypted_csv()` function, passing the destination as
    an argument.
    """
    today = date.today().strftime("%m%d%Y")
    destination = filedialog.asksaveasfilename(
      defaultextension=".csv",
      filetypes=(("CSV files", "*.csv"), ("All files", "*.*")),
      initialfile=f"VerifiedIndividuals{today}")
    save_encrypted_csv(destination)

  # GUI setup
window = tk.Tk()
window.title("Death Master Encrypter")

# Title label
title_label = tk.Label(window, text="File Viewer", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Read from CSV button
read_from_csv_button = tk.Button(window,
                                 text="Read from CSV",
                                 command=open_file_dialog)
read_from_csv_button.pack(pady=5)

# Fetch from NTIS button
fetch_from_ntis_button = tk.Menubutton(window,
                                       text="Fetch from NTIS",
                                       relief=tk.RAISED,
                                       bd=2)
fetch_from_ntis_button.pack(pady=5)

fetch_from_ntis()  # Fetch options for the Fetch from NTIS button

# Create a label widget to display the verified count
verified_label = tk.Label(window, text="Verified: 0/0 people")
verified_label.pack(pady=10)

# Create a label widget for Age Options
age_options_label = tk.Label(window, text="Age Options:")
age_options_label.pack()

# Create a label widget for Age Options
age_options_text = tk.Text(window, height=5, width=80)
age_options_text.pack(pady=10)

# Create a button to View Verified
view_verified_button = tk.Button(window,
                                 text="View Ages",
                                 command=display_verified_individuals)
view_verified_button.pack(pady=5)

# Save Encrypted CSV button
save_encrypted_csv_button = tk.Button(window,
                                      text="Save Encrypted CSV",
                                      command=save_encrypted_csv_dialog)
save_encrypted_csv_button.pack(pady=5)

# Verified Individuals text box
verified_individuals_text = tk.Text(window, height=20, width=100)
verified_individuals_text.pack(pady=10)

window.mainloop()
