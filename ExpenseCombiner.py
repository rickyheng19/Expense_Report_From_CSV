from datetime import datetime
from pathlib import Path
import pandas as pd
import calendar
import os
import csv

#Name file as last month
today = datetime.now()
lastMonth  = f"{calendar.month_name[today.month - 1]} {today.year} Expense Report"

#Make master expense sheet
header = {"Transaction Date": [], "Description": [], "Category": [], "Amount": []}
newFile = pd.DataFrame(header)

#go through each CVS file in folder
for file in os.scandir():
    if file.is_dir():
        continue
    CSVData = pd.read_csv(file)
    print(CSVData.head())

