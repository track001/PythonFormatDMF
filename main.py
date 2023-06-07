# Importing the tkinter module for creating GUI applications
import tkinter as tk

# Importing specific modules from tkinter
# filedialog: Provides dialogs for opening and saving files
# messagebox: Displays various types of message boxes
# Menu: Used to create menus in a tkinter application
from tkinter import filedialog, messagebox, Menu

# Importing the date module from the datetime library
from datetime import date

# Importing the pandas library for data manipulation and analysis
import pandas as pd


def read_death_master_file(file_path):
  df = pd.read_csv(file_path)
  return df


def calculate_age(date_of_birth, date_of_death):
  today = date.today()
  birth_date = pd.to_datetime(date_of_birth)
  death_date = pd.to_datetime(date_of_death)
  if death_date < today:
    age = (death_date - birth_date) // pd.Timedelta(days=365.25)
  else:
    age = (today - birth_date) // pd.Timedelta(days=365.25)
  return int(age)


def display_verified_individuals():
  verified_individuals_text.delete("1.0", tk.END)
  verified_individuals_text.insert(tk.END, "")

  if 'verification' in verified_individuals.columns:
    verified_df = verified_individuals[verified_individuals['verification'] ==
                                       'Verified']
    verified_individuals_text.insert(tk.END,
                                     verified_df.to_string(index=False))
  else:
    verified_individuals_text.insert(tk.END, "No verified individuals found.")


def calculate_age(date_of_birth, date_of_death, reference_date):
  age = reference_date.year - date_of_birth.year
  if reference_date < date_of_birth.replace(year=reference_date.year):
    age -= 1
  return age


def display_age_options(df):
  if 'date_of_birth' in df.columns and 'date_of_death' in df.columns:
    today = date.today()
    df['date_of_birth'] = pd.to_datetime(df['date_of_birth'])
    df['date_of_death'] = pd.to_datetime(df['date_of_death'])
    df['Age'] = df.apply(lambda row: calculate_age(row['date_of_birth'].date(
    ), row['date_of_death'].date(), today),
                         axis=1)
    age_options = df['Age'].unique()
    age_options_text.delete("1.0", tk.END)
    age_options_text.insert(tk.END, "\n".join(str(age) for age in age_options))


def download_csv_from_ntis(url, destination):
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


# Rest of the code remains the same


def open_file_dialog():
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


def fetch_from_ntis():
  menu = Menu(fetch_from_ntis_button, tearoff=0)
  menu.add_command(label="Weekly", command=fetch_weekly)
  menu.add_command(label="Monthly", command=fetch_monthly)

  fetch_from_ntis_button.configure(menu=menu)


def fetch_weekly():
  url = 'https://dmf.ntis.gov/weekly/'
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
  url = 'https://dmf.ntis.gov/monthly/'
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


def save_encrypted_csv():
  today = date.today().strftime("%m%d%Y")
  destination = filedialog.asksaveasfilename(
    defaultextension=".csv",
    filetypes=(("CSV files", "*.csv"), ("All files", "*.*")),
    initialfile=f"VerifiedIndividuals{today}")

  if destination:
    if 'verification' in verified_individuals.columns:
      verified_df = verified_individuals[verified_individuals['verification']
                                         == 'Verified']
      encrypted_df = verified_df.copy()
      encrypted_df['ssn'] = encrypted_df['ssn'].str[:-4] + 'XXXX'
      encrypted_df.to_csv(destination, index=False)
      messagebox.showinfo("Success", "Encrypted CSV file saved successfully!")
    else:
      messagebox.showinfo("Information",
                          "No verified individuals found to save.")


window = tk.Tk()
window.title("Death Master File Viewer")

title_label = tk.Label(window,
                       text="Death Master File Viewer",
                       font=("Arial", 16, "bold"))
title_label.pack(pady=10)

read_from_csv_button = tk.Button(window,
                                 text="Read from CSV",
                                 command=open_file_dialog)
read_from_csv_button.pack(pady=5)

fetch_from_ntis_button = tk.Menubutton(window,
                                       text="Fetch from NTIS",
                                       relief=tk.RAISED,
                                       bd=2)
fetch_from_ntis_button.pack(pady=5)

fetch_from_ntis()

age_options_label = tk.Label(window, text="Age Options:")
age_options_label.pack()

age_options_text = tk.Text(window, height=5, width=80)
age_options_text.pack(pady=10)

view_verified_button = tk.Button(window,
                                 text="View Ages",
                                 command=display_verified_individuals)
view_verified_button.pack(pady=5)

save_encrypted_csv_button = tk.Button(window,
                                      text="Save Encrypted CSV",
                                      command=save_encrypted_csv)
save_encrypted_csv_button.pack(pady=5)

verified_individuals_text = tk.Text(window, height=20, width=100)
verified_individuals_text.pack(pady=10)

window.mainloop()
