from datetime import datetime
from pathlib import Path
import pandas as pd
import calendar
import os

#Name file as last month
today = datetime.now()
lastMonth = today.month - 1 if today.month > 1 else 12
lastYear = today.year if today.month > 1 else today.year - 1
lastMonthName  = f"{calendar.month_name[lastMonth]} {lastYear} Expense Report"

#Make master expense sheet
header = ["Transaction Date", "Description", "Category", "Amount"]
newFile = pd.DataFrame(columns=header)

#go through each CVS file in folder
directory = Path('..') / 'CSV Bank Statements'
for file in os.scandir(directory):
    if file.is_dir():
        continue
    CSVData = pd.read_csv(file)
    if "Transaction Date" not in CSVData.columns or "Category" not in CSVData.columns:
        if "Posting Date" in CSVData.columns or "Type" in CSVData.columns:
            CSVData.rename(columns={"Posting Date": "Transaction Date"}, inplace=True)
            CSVData.rename(columns={"Type": "Category"}, inplace=True)
    filteredData = CSVData[header]
    print(filteredData.head())

