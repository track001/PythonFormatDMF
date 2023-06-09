Note/Disclaimer: None of the information in the CSV file is sensitive, it is all randomly generated data to test the formatting of a simulated Death Master File.

## Overview:
- The provided code is a program designed to read a file that simulates the Social Security Administration's Death Master File (DMF) data.
- The program aims to process the DMF records, extract relevant information, and perform various operations on the verified individuals' data.
- When downloading the newly generated CSV (verified_individuals_MMDDYYYY) of verified individuals, it keeps the SSN encrypted using AES encryption except for the last 4 digits to compare against CRM data.
  - Displays a truncated version of the SSN, and concatenates encryption of the first 5 digits with the last 4 digits.
 
## GUI Functionality
1. ![Login](01.LoginSS.JPG) Login screen
3. ![FalseLogin](02.IncorrectLoginSS.JPG) Entering incorrect password
4. ![SuccessLogin](03.LoginSucessSS.JPG) Successful login
5. ![Main](04.MainScreenSS.JPG) Main screen
6. ![SelectCSV](05.SelectFileSS.JPG) Select file (fetch option not shown for NTIS reasons)
7. ![SuccessCSV](06.SuccessCSVSS.JPG) Successful file chosen
8. ![Preview](07.PreviewCSVSS.JPG) Preview the data in the file (all fake data)
9. ![ExampleEncrypted](08.EncryptedCSVSS.JPG) Save file with SSN encrypted
10. ![MakeNew](09.NewCSVSS.JPG) Create new file with encrypted data
11. ![NonEncryptedExample](10.PreviousFileCSVSS.JPG) What the original CSV file looked like before encryption
12. ![EncryptedExample](11.EncryptedFileCSVSS.JPG) What the new CSV file looks like after encryption

Code Breakdown:

#### Importing necessary modules:
- CSV: Enables reading and writing CSV files.
- DateTime and date: Provide date and time functionality.
- os: Provides operating system-related functions (checks if file exists).
- encrypt_ssn(ssn): A function that takes an SSN as input and returns a string with the encrypted SSN. The function replaces the first 5 digits with asterisks and keeps the last 4 digits.
- csv_file_path: Specifies the file path of the simulated Death Master File CSV.
- verified_individuals: A list to store the information of verified individuals.

#### Reading the Death Master File and processing each record:
- The CSV file is opened using open() and read using csv.reader().
- The header row is skipped using next(csv_reader).
- For each row in the CSV, the relevant information (first name, last name, middle initial, date of birth, date of death, SSN, and verification status) is extracted.
- If the verification status is "verified" (case-insensitive), the age is calculated based on the current date and date of birth, the SSN is encrypted using encrypt_ssn(), and the record is added to the verified_individuals list.
- display_verified_individuals(): A function that displays the total number of verified individuals, the available ages in the dataset, and the information of each verified individual (name, age, encrypted SSN, and original SSN). The ages are extracted from the verified_individuals list using a set comprehension.
- filter_by_age(age): A function that filters the verified individuals based on a specified age. It creates a new list, filtered_individuals, containing only the individuals with the specified age. It then displays the total number of individuals at that age and their information.
- download_verified_csv(): A function to download the information of verified individuals as a new CSV file. The CSV filename is generated based on the current date and appended with a lowercase alphabet character to ensure uniqueness. The function writes the header row and the information of each verified individual (encrypted SSN instead of the original SSN) to the CSV file.

#### Main program loop:
- Displays the current date.
- Displays the available options (view all verified individuals, filter by age, download a new CSV with verified individuals, or quit).
- Accepts user input for the option to execute.
- Executes the corresponding action based on the selected option.
- The loop continues until the user chooses to quit.

Notes:
- This code assumes the existence of a simulated Death Master File CSV file with specific columns (first name, last name, middle initial, date of birth, date of death, SSN, and verification status).
- The program processes the verified individuals based on the "verified" status and provides options to view, filter, and download the information.
- The password is not stored as a global variable, i.e. not "hardcoded".
