
import xlrd
from collections import OrderedDict
import json
import codecs
from datetime import datetime
from xlrd import xldate_as_tuple
#excel是结果表

def get_excel(excle_path="test.xlsx",test_txt_path="test_sample.txt"):
    wb = xlrd.open_workbook(excle_path)
    convert_list = []
    #通过索引获取表格
    sh = wb.sheet_by_index(0)
    #获取表内容
    title = sh.row_values(0)
    #print(title)
    keys = []
    # 获取表行数
    rows=sh.nrows
    # print(sh.nrows)
    # 获取表列数
    cols = sh.ncols
    #print(cols)
    #for rownum in range(1, sh.nrows):
    for i in range(rows):
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
    #print(row_content)
    #  取出行数对应的值
    #rowvalue = sh.row_values(i)


    #根据按照类型转化后的字典重组
    single = OrderedDict()
    for colnum in range(0, len(row_content)):
        #print(title[colnum],row_content[colnum])
        #return (title[colnum],rowvalue[colnum])
        single[title[colnum]] = row_content[colnum]
    convert_list.append(single)
    excle = json.dumps(convert_list)
    excle_yangben = json.loads(excle)



    #读取测试样本的数据并解析重新组装
    f = open(test_txt_path)
    content = f.read()
    json_str = json.loads(content)
    List = []
    yangben = OrderedDict()
    #将变量转化为小写,并重新组装变量字典
    for key2 in json_str:
        for key3 in json_str[key2].keys():
            yangben[key3.lower()]=json_str[key2][key3]
        List.append(yangben)
    txt = json.dumps(List)
    txt_yangben = json.loads(txt)
    #print(txt_yangben)

    #校验2个文件的值
    for key6 in excle_yangben[0]:
        try:
            #相等的值不打印
            if str(txt_yangben[0][key6]) == str(excle_yangben[0][key6]):
               pass
               #  print('变量名：%s，测试样本中的值："%s"，excel中的值："%s"'%(key6, txt_yangben[0][key6], excle_yangben[0][key6]))
            else:
                #pass
                print('变量名：%s，测试样本中的值："%s"，excel中的值："%s"'%(key6, txt_yangben[0][key6], excle_yangben[0][key6]))

         #打印出在excel中存在，在测试样本13513543518中不存在的变量
        except Exception as e:
            pass
            #print('在测试样本中不存在%s变量' %e)


if __name__=="__main__":
    #get_excel()
    get_excel("C:\\Users\\Administrator\\Desktop\\22222\\76899870310413015.xlsx","C:\\Users\\Administrator\Desktop\\22222\\76899870310413015.txt")
