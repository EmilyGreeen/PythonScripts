#!/usr/bin/python3

import pandas as pan
import openpyxl

data = pan.DataFrame([[11,21,31],[12,22,32],[13,23,33]],
                    index=['one','two','three'], columns=['a','b','c'])

print(data)

data.to_excel('pandas.xlsx',sheet_name="pandas")

data2 = data[['a', 'c']]
print(data2)

with pan.ExcelWriter('pandas.xlsx') as writer:
    data.to_excel(writer, sheet_name="padawan")
    data2.to_excel(writer, sheet_name="pandaDeBaviere")