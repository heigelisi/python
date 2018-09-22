#如果读取时报错xlrd.compdoc.CompDocError: Workbook corruption: seen[3] == 4
解决办法是打开第三方库xlrd/compdoc.py 注释掉426行位置抛出的异常



# 读写2003 excel
import xlrd
import xlwt
# 读写2007 excel
import openpyxl



import xlrd

workbook = xlrd.open_workbook('X站论坛.xlsx')

#总行数
table = workbook.sheets()[0]
count = table.nrows

print(workbook.sheet_by_index(0))
booksheet = workbook.sheet_by_index(0)  #或用名称取sheet
# print(booksheet)

#读单元格数据  
cell_11 = booksheet.cell_value(0,0)  
cell_21 = booksheet.cell_value(1,1)  
#读一行数据  

row_3 = booksheet.row_values(1)  #读取第一行
row_3 = booksheet.row_values(2,2)  #读取第二行 跳过两列
print(row_3)  