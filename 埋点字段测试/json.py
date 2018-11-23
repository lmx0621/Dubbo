# coding:utf-8
import xlrd
from collections import OrderedDict
import json
import codecs
from datetime import datetime
from xlrd import xldate_as_tuple
import base64
import json
import io
import gzip


#app请求字段
def app(s):
    json_str = json.loads(s)
    List = []
    # 将变量转化为小写,并重新组装变量字典
    for key2, kye3 in json_str.items():

        List.append(key2)
        if isinstance(kye3, list):
            for kye4,key5 in kye3[0].items():
                #print(kye4,key5)
                List.append(kye4)
    return (List)


#eexcel表内字段
def get_excel():
    wb = xlrd.open_workbook(r"test.xls")
    convert_list = []
    #通过索引获取表格
    sh = wb.sheet_by_index(0)
    # 获取表行数
    rows=sh.nrows
    # 获取表列数
    cols = sh.ncols
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
        single = OrderedDict()
        single[row_content[0]] = [row_content[1]]
        convert_list.append(single)
    #print(convert_list)
    j = json.dumps(convert_list, ensure_ascii=False)
    excel = json.loads(j)
    List1 = []
    single1 = OrderedDict()
    for i in range(len(excel)):
        for v, k in excel[i].items():
            single1[v] = excel[i][v]
    List1.append(single1)
    j = json.dumps(List1, ensure_ascii=False)
    excel2 = json.loads(j)
    return excel2


#判断APP内必填字段是否为空
def app2(s):
    json_str = json.loads(s)
    # 将变量转化为小写,并重新组装变量字典
    count=0
    for key2, kye3 in json_str.items():
        if isinstance(kye3, list):
            for kye4,key5 in kye3[0].items():
                #print(kye4,key5)
                for key, key2 in get_excel()[0].items():
                     #print(key,key2[0])
                     if key2[0] == "非空" and kye4 ==key:
                         print("----------------------------------------------------------------------------------------------------------")
                         print("excel表格必填字段：%s,      在APP内显示值不能为空：%s"%(key,key5))
                     # elif key2[0] == "是" and kye4 ==key and key5 !="":
                     #     print("----------------------------------------------------------------------------------------------------------")
                     #     print("excel表格非必填字段：%s,      在APP内不为空：%s"%(key,key5))
                     elif (key2[0] == "是" and kye4 == key) and key5 == "":
                         count += 1
                         print("----------------------------------------------------------------------------------------------------------")
                         print("app字段：%s   value为空：%s" % (key, key5),count)






if __name__=="__main__":
    s = input("请输入请求json字符串:")
    app2(s)
    print("----------------------------------------------------------------------------------------------------------")
    #excel表字段在APP内不存在
    #print(get_excel()[0])
    list0 = []
    for key6,key7 in get_excel()[0].items():
        #print(key6)
        list0.append(key6)
    for t in list0:
        if t not in app(s):
            print("excel表格内字段不存在APP内：%s" %t)

    print("----------------------------------------------------------------------------------------------------------")

    # 取出excel表内非空的字段
    for key, key2 in get_excel()[0].items():
        # print(key,key2[0])
        if key2[0] == "非空":
            print("打印excel表内非空的字段：%s" % key)
            if key not in app(s):
                print("打印不存在app内的key：%s" % key, "xxxxxxxxxxxxxxxxxxxxxxx")


