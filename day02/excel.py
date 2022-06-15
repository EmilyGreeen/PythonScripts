#!/usr/bin/python3

import xlrd

path = ("~/Python/Classeur1.xlsx")

wb = xlrd.open_workbook(path)
sheet = wb.sheet_by_index(0)

print(sheet.nrows)
print(sheet.ncols)

for i in range(sheet.nrows):
    print(sheet.row_values(i))
print()
    

import xlsxwriter

houses = (
    ["12 flower road","poltergeist"],
    ["1008 mistery boulevard","banshee"],
    ["Bowley Manor","???"],
    ["206 beach avenue","bloat"]
)

row = 0
col = 0

workbook = xlsxwriter.Workbook('Houses.xlsx')
worksheet = workbook.add_worksheet()

for addr, ghost in (houses):
    worksheet.write(row, col,     addr)
    worksheet.write(row, col + 1, ghost)
    row += 1
    
workbook.close()


wb = xlrd.open_workbook('Houses.xlsx')
sheet = wb.sheet_by_index(0)

for i in range(sheet.nrows):
    print(sheet.row_values(i))