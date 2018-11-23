import json
from collections import OrderedDict
import time
import xlrd
from datetime import datetime
from xlrd import xldate_as_tuple

def get_excel():
    wb = xlrd.open_workbook(r"query-hive-67811.xlsx")
    convert_list = []
    #通过索引获取表格
    sh = wb.sheet_by_index(0)
    # 获取表行数
    rows=sh.nrows
    # 获取表列数
    cols = sh.ncols
    for i in range(1,rows):
        row_content = []
        for j in range(cols):
            #ctype： 0,empty, 1,string, 2,number, 3,date, 4,boolean, 5,error
            ctype = sh.cell(i, j).ctype  # 表格的数据类型
            #print(sh.cell(i, j),ctype)
            cell = sh.cell_value(i, j)
            if ctype == 2 and cell % 1 == 0:  # 如果是整形
                cell = int(cell)
            elif ctype == 3:
                # 转成datetime对象
                date = datetime(*xldate_as_tuple(cell, 0))
                cell = date.strftime('%Y/%d/%m %H:%M:%S')
            elif ctype == 4:
                cell = True if cell == 1 else False
            row_content.append(cell)
        single = OrderedDict()
        single[row_content[3]] = row_content[5]
        convert_list.append(single)
    #print(convert_list)
    j = json.dumps(convert_list, ensure_ascii=False)
    excel = json.loads(j)
    print(len(excel))


if __name__ == "__main__":
        starttime = time.time()
        get_excel()
        endtime = time.time()
        print("花费%s秒时间"%(endtime - starttime))