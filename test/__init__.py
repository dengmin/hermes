import xlrd
book = xlrd.open_workbook("/Users/dengmin/Downloads/1月份考试分析.xlsx",encoding_override='utf-8')
print("The number of worksheets is {0}".format(book.nsheets))
print("Worksheet name(s): {0}".format(book.sheet_names()))
sh = book.sheet_by_index(0)
for i in range(sh.nrows):
    if i in(0, 1): continue
    print(i, sh.row_values(i))