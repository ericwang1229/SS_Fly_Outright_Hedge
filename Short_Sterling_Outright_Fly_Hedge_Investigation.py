import pandas as pd
path = r"C:\New folder\L_History.xlsx"
xls = pd.ExcelFile(path)
data = {}
for sheet_name in xls.sheet_names:
    data[sheet_name] = xls.parse(sheet_name)
    data[sheet_name].columns = ['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']
outrights = xls.sheet_names[0:12]
flies = xls.sheet_names[12:]

    
    
