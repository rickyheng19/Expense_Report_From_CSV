from datetime import datetime
from pathlib import Path
import pandas as pd
import calendar
import os

#Open containing folder first in vs
#Name file as last month
today = datetime.now()
lastMonth = today.month - 1 if today.month > 1 else 12
lastYear = today.year if today.month > 1 else today.year - 1
lastMonthName  = f"{calendar.month_name[lastMonth]} {lastYear} Expense Report.csv"

#Make master expense sheet
header = ["Transaction Date", "Description", "Category", "Amount"]
newFile = pd.DataFrame(columns=header)

#Make Category to ignore and change
categoryToIgnore = ['ACCT_XFER', "LOAN_PMT"]
categoryToChangeBills = ['ACH_DEBIT','LAMIA','YouTubePremium', 'CHATGPT SUBSCR']
categoryToChangeTravel = ['UBER 866']
categoryToChangeShopping = ['MISC_DEBIT']

# Method to filter rows
def change_category(row):
    if any(keyword in row['Description'] for keyword in categoryToChangeBills) or \
       any(keyword in row['Category'] for keyword in categoryToChangeBills):
        return 'Bills & Utilities'
    elif any(keyword in row['Description'] for keyword in categoryToChangeTravel) or \
         any(keyword in row['Category'] for keyword in categoryToChangeTravel):
        return 'Travel'
    elif any(keyword in row['Description'] for keyword in categoryToChangeShopping) or \
         any(keyword in row['Category'] for keyword in categoryToChangeShopping):
        return 'Shopping'
    return row['Category']

#go through each CVS file in folder
directory = Path('..') / 'CSV Bank Statements'
for file in os.scandir(directory):
    if file.is_dir():
        continue
    CSVData = pd.read_csv(file)
    #Removes columns, and Renames the columns in the debit file to match the other cards
    if "Transaction Date" not in CSVData.columns or "Category" not in CSVData.columns:
        if "Posting Date" in CSVData.columns or "Type" in CSVData.columns:
            CSVData = pd.read_csv(file, index_col=False)
            CSVData = CSVData.reset_index(drop=True)
            CSVData = CSVData.drop(columns=['Details','Balance','Check or Slip #'])
            #Pick needed columns 
            CSVData.rename(columns={"Posting Date": "Transaction Date", "Type": "Category"}, inplace=True)
    
    #Filter columns        
    CSVData = CSVData[header]

    #Filter category
    CSVData = CSVData[~CSVData['Category'].isin(categoryToIgnore)]
    # Convert columns to string to avoid TypeError, and change the category
    CSVData['Description'] = CSVData['Description'].fillna('').astype(str)
    CSVData['Category'] = CSVData['Category'].fillna('').astype(str)
    CSVData['Category'] = CSVData.apply(change_category, axis=1)

    #Convert 'amount' column to numeric
    CSVData['Amount'] = pd.to_numeric(CSVData["Amount"], errors='coerce')

    #Only include negative values and add to master expense sheet
    if 'Amount' in CSVData.columns:
        appendRow = CSVData[(CSVData['Amount'] < 0)].copy()
        #Remove negative sign
        appendRow.loc[:, "Amount"] = appendRow['Amount'].abs()
        newFile = pd.concat([newFile, appendRow], ignore_index=True)

#Convert dates to datetime format, and sort column.
newFile['Transaction Date'] = pd.to_datetime(newFile["Transaction Date"])
newFile = newFile.sort_values(by="Category")

#Save file
saveDirectory = Path('..') / lastMonthName
newFile.to_csv(saveDirectory, index=False)