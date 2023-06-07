# Death Master File Viewer

The Death Master File Viewer is a graphical user interface (GUI) application built in Python that allows users to view and analyze data from the Death Master File (DMF). The DMF contains information about deceased individuals in the United States. (It is both GUI and CLI functional.)

## Features

- Read data from a CSV file containing DMF records.
- Fetch DMF data from the NTIS website on a weekly or monthly basis.
- Display verified individuals' information.
- Calculate and display age options based on date of birth and date of death.
- Save an encrypted version of the verified individuals' CSV file.

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