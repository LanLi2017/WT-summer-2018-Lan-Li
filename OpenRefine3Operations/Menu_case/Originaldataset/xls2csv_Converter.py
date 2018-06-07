import pandas as pd
data_xls = pd.read_excel('Menu-csv.xls')
data_xls.to_csv('Menu-csv.csv', encoding='utf-8')


