# coding:utf-8
import json
import configparser
import jsonpath as jsonpath
import time

import os

# aaa = json.loads(aaa)

def hive(table_name,num):
    list_a =[]
    from pyhive import hive
    conn = hive.Connection(host='10.0.4.142', port=10000, username='hadoop', database='provider_api_db', auth='LDAP',password='DUMMY')
    cursor = conn.cursor()
    cursor.execute('select * from {} limit 1000'.format(table_name))
    for result in cursor.fetchall():
        list_a.append(result[num])
    return (list_a)


#读取json
def open_json_file():
    file = open('test-data-2018-11-15.json','rb')
    content = file.read()
    jsontr = json.loads(content)
    return (jsontr)

#接口和对应的json统一dict内
def method():
    method_key = []
    jsonstr = {}
    for i in range(len(open_json_file())):
        #print(open_json_file()[i])
        #jsonpath获取接口
        method_vaule = jsonpath.jsonpath(open_json_file()[i],"$..method")
        method_vaule1 = method_vaule[0].split('.')
        #按照a_b格式组装
        method_name = method_vaule1[0]+'_'+method_vaule1[1]
        #接口名和字符串都放到list
        method_key.append(method_name)
        method_key.append(open_json_file()[i])
    #list转化为dict
    for a in range(0,len(method_key),2):
        jsonstr[method_key[a]] =method_key[a+1]
    return jsonstr





def paser():
    # print("正在校验{}表字段".format(table_name))
    # cf = configparser.ConfigParser()
    # cf.read("config.ini")
    # fields_table_param = cf.get("fields", table_name).strip(',').split(',')
    # root = cf.get(table_name, "root")
    # optionalRoots_request = cf.get(table_name, "a")
    # optionalRoots_response = cf.get(table_name, "b")

    for key, value in method().items():
        # 判断ini文件是否存在
        if os.path.exists('%s.ini' % key):
            # print(key)
            conf = configparser.ConfigParser()
            conf.read('%s.ini' % key)
            # 显示颜色格式：\033[显示方式;字体色;背景色m......[\033[0m]
            print("\033[1;33;44m.........................................打开文件{}.ini.........................................\033[0m".format(key))
            # 读取配置文件
            table_list = conf.get("table_list", "table_list").strip(',').split(',')
            for table_name in table_list:
                print("\033[1;31;46m------------------正在校验{}表字段------------------\033[0m".format(table_name))
                #获取表字段
                fields_table_param = conf.get('fields', table_name).split(',')
                #获取配置文件下需要测试表的节点
                root = conf.get(table_name, "root")
                optionalRoots_request = conf.get(table_name, "a")
                optionalRoots_response = conf.get(table_name, "b")

                for i in range(len(fields_table_param)):
                    # print(i)
                    #从json中获取该节点下相应字段的值
                    root_value = jsonpath.jsonpath(value, "$..{}..{}".format(root, fields_table_param[i]))
                    optionalRoots_response_value = jsonpath.jsonpath(value, "$..{}..{}".format(optionalRoots_response, fields_table_param[i]))
                    optionalRoots_request_value = jsonpath.jsonpath(value, "$..{}..{}".format(optionalRoots_request, fields_table_param[i]))
                    hive_value = hive(table_name, i)
                    #判断root节点下能否取到值，取到值就进行校验，取不到值，就执行elif
                    if root_value:
                        for j in root_value:
                            if j in hive_value:
                                print("{} 字段测试通过".format(fields_table_param[i]))
                            else:
                                print(fields_table_param[i], root_value, hive_value)
                    #过滤idCard和mobile
                    elif fields_table_param[i] == "idCard" or fields_table_param[i] == "mobile":
                        print("******{} 字段为加密字段******".format(fields_table_param[i]))
                    #root节点取不到值，就执行下面步骤
                    elif optionalRoots_response_value:
                        for j in optionalRoots_response_value:
                            if j in hive_value:
                                print("{} 字段测试通过".format(fields_table_param[i]))
                            else:
                                print(fields_table_param[i], optionalRoots_response_value, hive_value)
                    #如果字段为queryTime，将时间戳转化为年月日时分秒，然后转化成unicod编码格式
                    # elif fields_table_param[i] == "queryTime":
                    #     queryTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(optionalRoots_request_value[0] / 1000))
                    #     if queryTime in hive_value[0].encode("utf-8"):
                    #         print("{} 字段测试通过".format(fields_table_param[i]))
                    #     else:
                    #         print(fields_table_param[i], queryTime, hive_value[0].encode("utf-8"))
                    # root节点和optionalRoots_response节点都取不到值，就执行下面步骤
                    elif optionalRoots_request_value:
                        for j in optionalRoots_request_value:
                            if j in hive_value:
                                print("{} 字段测试通过".format(fields_table_param[i]))
                            else:
                                print(fields_table_param[i], optionalRoots_request_value, hive_value)
                    #其他字段为空则默认通过
                    else:
                        if "None" in str(hive_value):
                            print("{} 字段测试通过".format(fields_table_param[i]))
                        else:
                            print(fields_table_param[i], "None", hive_value)

                print("\n\n")
        else:
            print("\033[1;35;43m#####################{}.ini文件不存在，请检查#####################\033[0m".format(key))
if __name__=="__main__":
    # cf = configparser.ConfigParser()
    # cf.read("config.ini")
    # table_list = cf.get("table_list", "table_list").strip(',').split(',')
    # for i in  table_list:
    #     paser(i)
    paser()
