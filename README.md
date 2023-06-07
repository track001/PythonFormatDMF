# Death Master File Viewer

The Death Master File Viewer is a graphical user interface (GUI) application built in Python that allows users to view and analyze data from the Death Master File (DMF). The DMF contains information about deceased individuals in the United States. (It is both GUI and CLI functional.)

## Features

- Read data from a CSV file containing DMF records.
- Fetch DMF data from the NTIS website on a weekly or monthly basis.
- Display verified individuals' information.
- Calculate and display age options based on date of birth and date of death.
- Save an encrypted version of the verified individuals' CSV file.

# Encryption of SSN
The Death Master Encrypter implements a basic encryption scheme to protect sensitive information, specifically the Social Security Numbers (SSN). The encryption process involves replacing the first 5 digits of the SSN with asterisks (*) while preserving the last 4 digits. This provides a level of obfuscation to protect the privacy of individuals' SSNs.

<br> **Disclaimer:** When saving the encrypted data, please be aware that the encryption process is irreversible. To ensure the permanency of the encrypted data and prevent the retrieval of the original SSNs, it is recommended to create a new CSV file to store the encrypted data. Please exercise caution and securely delete the original file, including permanently deleting it from the recycle bin or trash folder on your operating system. If you need to access the data again, it is advised to redownload it from the NTIS website.

# Handling Type Mismatch Issue
One potential issue with the encryption process is a type mismatch between bytes and strings. The error occurs when attempting to concatenate the encrypted portion of the SSN (bytes) with the remaining part (string). To address this, the application now converts the remaining part of the SSN to bytes using the .encode() method before concatenating. This ensures that both the encrypted portion and the remaining part are of the same data type, allowing for successful concatenation.

## Installation

1. Clone the repository:

```shell```
git clone [https://github.com/your-username/your-repo.git](https://github.com/track001/PythonFormatDMF)
<br>- Install the required dependencies. Ensure you have Python and pip installed, and then run:
<br>```shell```
pip install pandas tkinter
<br>Usage:
<br>- Run the dmf_viewer.py script:
<br>```shell```
python dmf_viewer.py
<br>- Use the GUI interface to perform the following actions:
<br>- Read data from a CSV file: Click on the "Read from CSV" button and select a CSV file containing DMF records.
<br>- Fetch data from NTIS: Click on the "Fetch from NTIS" button and choose either the weekly or monthly option to download the DMF data from the NTIS website.
<br>- View verified individuals: Click on the "View Ages" button to display the ages of the individuals' in the "preview" text area.
<br> - View age options: The unique age options based on date of birth and date of death will be displayed in the "Age Options" section.
<br>- Save encrypted CSV: Click on the "Save Encrypted CSV" button to save an encrypted version of the verified individuals' CSV file.

# Disclaimer
- No data here is sensitive information, meaning the CSV's are generated randomly to create "people" to test the filtering/verification file viewer.
- If you don't have the certification through the NTIS and subsequent ACAB, you won't be able to "Fetch from NTIS" for the most recently uploaded "Weekly" or "Monthly" options.
- The code is running these links and for now, pulls HTML elements off the webpage due to lack of certification:
  - Weekly: https://dmf.ntis.gov/weekly/.
  - Monthly: https://dmf.ntis.gov/monthly/.

# Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

# License
This project is licensed under the MIT License.