import tkinter as tk
from tkinter import filedialog, messagebox, Menu
from datetime import date
import pandas as pd
import urllib.request


def read_death_master_file(file_path):
    df = pd.read_csv(file_path)
    return df


def filter_by_age(age):
    today = pd.Timestamp.now().normalize()
    filtered_df = verified_individuals[
        ((today - pd.to_datetime(verified_individuals['date_of_birth'], errors='coerce')).dt.days / 365.25 <= age)
        & (verified_individuals['date_of_death'].isnull()
           | ((today - pd.to_datetime(verified_individuals['date_of_death'], errors='coerce')).dt.days / 365.25 <= age))
    ]
    preview_filtered_individuals(filtered_df)


def preview_filtered_individuals(df):
    verified_individuals_text.delete("1.0", tk.END)
    verified_individuals_text.insert(tk.END, df.to_string(index=False))


def display_verified_individuals():
    today = pd.Timestamp.now().normalize()
    verified_individuals['date_of_birth'] = pd.to_datetime(verified_individuals['date_of_birth'], errors='coerce')
    verified_individuals['date_of_death'] = pd.to_datetime(verified_individuals['date_of_death'], errors='coerce')
    verified_individuals['Age'] = ((today - verified_individuals['date_of_birth']).dt.days / 365.25).astype(int)
    verified_individuals_text.delete("1.0", tk.END)
    verified_individuals_text.insert(tk.END, verified_individuals.to_string(index=False))

    age_options = verified_individuals['Age'].unique()
    age_options_text.delete("1.0", tk.END)
    age_options_text.insert(tk.END, "\n".join(str(age) for age in age_options))


def download_csv_from_ntis(url, destination):
    try:
        urllib.request.urlretrieve(url, destination)
        global verified_individuals
        verified_individuals = read_death_master_file(destination)
        messagebox.showinfo("Success", "CSV file downloaded and read successfully!")
        display_verified_individuals()
    except pd.errors.ParserError as pe:
        messagebox.showerror("Error", f"Error parsing CSV file: {str(pe)}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    if file_path:
        try:
            global verified_individuals
            verified_individuals = read_death_master_file(file_path)
            messagebox.showinfo("Success", "CSV file read successfully!")
            display_verified_individuals()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


def fetch_from_ntis():
    menu = Menu(fetch_from_ntis_button, tearoff=0)
    menu.add_command(label="Weekly", command=fetch_weekly)
    menu.add_command(label="Monthly", command=fetch_monthly)

    fetch_from_ntis_button.configure(menu=menu)


def fetch_weekly():
    url = 'https://dmf.ntis.gov/weekly/'
    today = date.today().strftime("%m%d%Y")
    destination = filedialog.asksaveasfilename(defaultextension=".csv",
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
    destination = filedialog.asksaveasfilename(defaultextension=".csv",
                                               filetypes=(("CSV files", "*.csv"), ("All files", "*.*")),
                                               initialfile=f"DMFVerificationsMonthly{today}")
    if destination:
        try:
            download_csv_from_ntis(url, destination)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


window = tk.Tk()
window.title("Death Master File Viewer")

title_label = tk.Label(window, text="Death Master File Viewer", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

read_from_csv_button = tk.Button(window, text="Read from CSV", command=open_file_dialog)
read_from_csv_button.pack(pady=5)

fetch_from_ntis_button = tk.Menubutton(window, text="Fetch from NTIS", relief=tk.RAISED, bd=2)
fetch_from_ntis_button.pack(pady=5)

fetch_from_ntis()

age_label = tk.Label(window, text="Filter by Age:")
age_label.pack()

age_entry = tk.Entry(window, width=10)
age_entry.pack()


def filter_button_callback():
    age = age_entry.get()
    if age.isdigit():
        filter_by_age(int(age))
    else:
        messagebox.showerror("Error", "Please enter a valid age (numeric value).")


filter_button = tk.Button(window, text="Filter", command=filter_button_callback)
filter_button.pack(pady=5)

view_all_button = tk.Button(window, text="View All", command=display_verified_individuals)
view_all_button.pack(pady=5)

age_options_label = tk.Label(window, text="Age Options:")
age_options_label.pack()

age_options_text = tk.Text(window, height=5, width=80)
age_options_text.pack(pady=10)

verified_individuals_text = tk.Text(window, height=20, width=100)
verified_individuals_text.pack(pady=10)

window.mainloop()
